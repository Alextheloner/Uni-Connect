from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from .forms import (
    RegisterForm, LoginForm, ProfileEditForm, VerifyOTPForm,
    PasswordResetRequestForm, PasswordResetConfirmForm,
)
from .models import User, OTPCode
from forum.models import Department
import random
import string
import logging
import smtplib

logger = logging.getLogger(__name__)


def build_otp_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(user, purpose):
    """Create an OTP code and email it to the user.

    Returns True if the message was successfully handed off to the mail
    backend (a real SMTP send when EMAIL_HOST_USER/EMAIL_HOST_PASSWORD are
    configured, or written to sent_emails/ in local development), and False
    if sending failed — e.g. wrong SMTP credentials, the mail server being
    unreachable, or a network timeout. Callers should check this and tell
    the user rather than assuming the email went out.

    If sending fails, the OTP row is removed again so an unusable, never
    delivered code doesn't linger in the database.
    """
    code = build_otp_code()
    expires_at = timezone.now() + timezone.timedelta(minutes=20)
    otp = OTPCode.objects.create(user=user, code=code, purpose=purpose, expires_at=expires_at)

    subject = 'Uni-Connect verification code'
    if purpose == 'email_verification':
        message = f'Hello {user.get_full_name() or user.username},\n\nUse this code to verify your email address: {code}\n\nIf you did not create an account, ignore this message.'
    else:
        message = f'Hello {user.get_full_name() or user.username},\n\nUse this code to reset your password: {code}\n\nThis code expires in 20 minutes. If you did not request a password reset, ignore this message and your password will remain unchanged.'

    try:
        sent_count = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        if sent_count:
            return True
        logger.error('Email backend reported 0 messages sent for %s to %s', purpose, user.email)
        otp.delete()
        return False
    except (smtplib.SMTPException, OSError, ConnectionError) as exc:
        logger.error('Failed to send %s email to %s: %s', purpose, user.email, exc)
        otp.delete()
        return False


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Immediately activate accounts (email verification removed)
            user.is_active = True
            user.save()
            form.save_m2m()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'forum:home')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('forum:home')


@login_required
def profile_view(request, username=None):
    """
    Display either the logged-in user's profile
    or another user's profile.
    """

    if username is None:
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, username=username)

    threads = (
        profile_user.threads
        .filter(is_deleted=False)
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": profile_user,
            "threads": threads,
        },
    )


@login_required
def edit_profile_view(request):
    """
    Edit logged-in user's profile.
    """

    if request.method == "POST":
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:profile")

    else:
        form = ProfileEditForm(instance=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )


def verify_email_view(request):
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp_code = form.cleaned_data['otp_code']
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                messages.error(request, 'No account found with that email address.')
            else:
                otp = OTPCode.objects.filter(user=user, code=otp_code, purpose='email_verification', is_used=False).order_by('-created_at').first()
                if otp and otp.is_valid():
                    otp.is_used = True
                    otp.save()
                    user.is_email_verified = True
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Email verified successfully! You can now log in.')
                    return redirect('accounts:login')
                messages.error(request, 'Invalid or expired verification code.')
    else:
        form = VerifyOTPForm()
    return render(request, 'accounts/verify_email.html', {'form': form})


def resend_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if send_otp_email(user, 'email_verification'):
                messages.success(request, 'Verification code sent to your email!')
            else:
                messages.error(
                    request,
                    "We couldn't send the verification email right now. Please try again shortly."
                )
        else:
            messages.error(request, 'No account found with that email address.')
        return redirect('accounts:verify_email')
    return redirect('accounts:verify_email')


def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()
            if user:
                if send_otp_email(user, 'password_reset'):
                    messages.success(request, 'Check your email for the password reset code.')
                    return redirect('accounts:password_reset_confirm')
                messages.error(
                    request,
                    "We couldn't send the reset email right now. Please try again in a "
                    "moment — if this keeps happening, contact support."
                )
            else:
                messages.error(request, 'No account was found with that email address.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def load_departments(request):
    """AJAX endpoint: return the departments belonging to a given school as
    JSON, so the registration and profile-edit forms can populate the
    department dropdown dynamically without a page reload."""
    school_id = request.GET.get('school')
    departments = Department.objects.none()
    if school_id:
        departments = Department.objects.filter(school_id=school_id).order_by('name')
    data = [{'id': dept.id, 'name': dept.name} for dept in departments]
    return JsonResponse({'departments': data})


def password_reset_confirm_view(request):
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp_code = form.cleaned_data['otp_code']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                messages.error(request, 'No account found for that email.')
            elif new_password1 != new_password2:
                messages.error(request, 'Passwords do not match.')
            else:
                otp = OTPCode.objects.filter(user=user, code=otp_code, purpose='password_reset', is_used=False).order_by('-created_at').first()
                if otp and otp.is_valid():
                    otp.is_used = True
                    otp.save()
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('accounts:login')
                messages.error(request, 'Invalid or expired reset code.')
    else:
        form = PasswordResetConfirmForm()
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})
