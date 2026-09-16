from django.db import migrations


DEFAULT_SCHOOL_NAME = 'University of Nigeria, Nsukka'


def backfill_user_school(apps, schema_editor):
    """Give every pre-existing user a school so filtering keeps working for
    them immediately after the upgrade:
      - if the user already has a department, inherit that department's school
      - otherwise, fall back to the platform's original institution (UNN)
    """
    User = apps.get_model('accounts', 'User')
    School = apps.get_model('forum', 'School')

    default_school = School.objects.filter(name=DEFAULT_SCHOOL_NAME).first()

    users_with_department = User.objects.filter(school__isnull=True, department__isnull=False).select_related('department')
    for user in users_with_department:
        if user.department.school_id:
            user.school_id = user.department.school_id
            user.save(update_fields=['school'])

    if default_school:
        User.objects.filter(school__isnull=True).update(school=default_school)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_school'),
        ('forum', '0004_backfill_default_school'),
    ]

    operations = [
        migrations.RunPython(backfill_user_school, noop_reverse),
    ]
