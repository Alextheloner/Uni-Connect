
import os
import sys
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniconnect.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from forum.models import School, Department, Course, Thread, Reply, Tag, ChatRoom, ChatMessage
from accounts.models import User

tags = {}
for name, color in [('exam', '#f59e0b'), ('assignment', '#6C63FF'), ('lecture', '#10b981'),
                     ('practical', '#ef4444'), ('textbook', '#8b5cf6'), ('project', '#0ea5e9')]:
    t, _ = Tag.objects.get_or_create(name=name, defaults={'color': color})
    tags[name] = t

unn, _ = School.objects.get_or_create(
    name='University of Nigeria, Nsukka',
    defaults={'short_name': 'UNN', 'school_type': 'university', 'state': 'Enugu'},
)

dept_data = [
    ('Computer Science', 'CSC', 'Faculty of Physical Sciences', 'Programming, algorithms, AI, databases and software engineering.', '#6C63FF', 'bi-cpu'),
    ('Mechanical Engineering', 'MEG', 'Faculty of Engineering', 'Thermodynamics, fluid mechanics, machine design.', '#f59e0b', 'bi-gear'),
    ('Medicine & Surgery', 'MED', 'College of Medicine', 'Clinical medicine, surgery, pharmacology.', '#ef4444', 'bi-heart-pulse'),
    ('Economics', 'ECO', 'Faculty of Social Sciences', 'Microeconomics, macroeconomics, econometrics.', '#10b981', 'bi-graph-up'),
    ('Law', 'LAW', 'Faculty of Law', 'Constitutional law, commercial law, criminal law.', '#3b82f6', 'bi-book'),
    ('English & Literary Studies', 'ENG', 'Faculty of Arts', 'Literature, linguistics, creative writing.', '#ec4899', 'bi-pen'),
    ('Mathematics', 'MTH', 'Faculty of Physical Sciences', 'Pure mathematics, applied mathematics, statistics.', '#8b5cf6', 'bi-calculator'),
    ('Physics', 'PHY', 'Faculty of Physical Sciences', 'Classical mechanics, quantum physics, electromagnetism.', '#06b6d4', 'bi-lightning'),
    ('Accountancy', 'ACC', 'Faculty of Business Administration', 'Financial reporting, auditing, taxation.', '#14b8a6', 'bi-calculator-fill'),
]
depts = {}
for name, code, faculty, desc, color, icon in dept_data:
    d, _ = Department.objects.get_or_create(school=unn, code=code, defaults={
        'name': name, 'faculty': faculty, 'description': desc, 'color': color, 'icon': icon
    })
    depts[code] = d

course_data = [
    (depts['CSC'], 'CSC 201', 'Introduction to Computer Science', '200L', 'First Semester', 3),
    (depts['CSC'], 'CSC 301', 'Data Structures and Algorithms', '300L', 'First Semester', 3),
    (depts['CSC'], 'CSC 303', 'Database Management Systems', '300L', 'Second Semester', 3),
    (depts['CSC'], 'CSC 401', 'Operating Systems', '400L', 'First Semester', 3),
    (depts['CSC'], 'CSC 403', 'Computer Networks', '400L', 'Second Semester', 3),
    (depts['CSC'], 'CSC 407', 'Artificial Intelligence', '400L', 'First Semester', 3),
    (depts['CSC'], 'CSC 405', 'Software Engineering', '400L', 'Second Semester', 3),
    (depts['MEG'], 'MEG 201', 'Engineering Mathematics I', '200L', 'First Semester', 3),
    (depts['MEG'], 'MEG 301', 'Thermodynamics', '300L', 'First Semester', 3),
    (depts['MEG'], 'MEG 303', 'Fluid Mechanics', '300L', 'Second Semester', 3),
    (depts['MED'], 'MED 301', 'Anatomy and Physiology', '300L', 'First Semester', 6),
    (depts['MED'], 'MED 401', 'Pharmacology', '400L', 'First Semester', 6),
    (depts['ECO'], 'ECO 201', 'Microeconomics I', '200L', 'First Semester', 3),
    (depts['ECO'], 'ECO 301', 'Macroeconomics', '300L', 'First Semester', 3),
    (depts['MTH'], 'MTH 201', 'Mathematical Methods', '200L', 'First Semester', 3),
    (depts['MTH'], 'MTH 301', 'Real Analysis', '300L', 'First Semester', 3),
    (depts['ACC'], 'ACC 201', 'Financial Accounting I', '200L', 'First Semester', 3),
    (depts['LAW'], 'LAW 301', 'Law of Contract', '300L', 'First Semester', 4),
]
courses = {}
for dept, code, title, level, sem, units in course_data:
    c, _ = Course.objects.get_or_create(department=dept, code=code, defaults={
        'title': title, 'level': level, 'semester': sem, 'units': units
    })
    courses[code] = c

# ---------------------------------------------------------------------------
# 2. Extra accounts (students + lecturers across departments)
# ---------------------------------------------------------------------------
lecturer_data = [
    ('dr.nwachukwu', 'Dr. Ifeoma', 'Nwachukwu', depts['MTH'], 280),
    ('prof.balogun', 'Prof. Tunde', 'Balogun', depts['MEG'], 410),
    ('dr.eze', 'Dr. Grace', 'Eze', depts['ECO'], 300),
]
lecturers = {}
for uname, fname, lname, dept, rep in lecturer_data:
    u, created = User.objects.get_or_create(username=uname, defaults={
        'email': f'{uname}@unn.edu.ng', 'first_name': fname, 'last_name': lname,
        'role': 'lecturer', 'school': unn, 'department': dept, 'reputation': rep,
    })
    if created:
        u.set_password('lecturer123')
        u.save()
    lecturers[uname] = u

student_data = [
    ('tobi_akin', 'Tobi', 'Akinwale', courses['CSC 301'].department, '2021/243100', 95),
    ('fatima_musa', 'Fatima', 'Musa', depts['MED'], '2021/243200', 140),
    ('daniel_okoro', 'Daniel', 'Okoro', depts['MEG'], '2021/243300', 60),
    ('blessing_nnaji', 'Blessing', 'Nnaji', depts['CSC'], '2021/243400', 210),
    ('ibrahim_yusuf', 'Ibrahim', 'Yusuf', depts['LAW'], '2021/243500', 75),
    ('grace_udo', 'Grace', 'Udo', depts['ACC'], '2021/243600', 130),
    ('samuel_afolabi', 'Samuel', 'Afolabi', depts['MTH'], '2021/243700', 88),
    ('chiamaka_igwe', 'Chiamaka', 'Igwe', depts['CSC'], '2021/243800', 165),
]
students = {}
for uname, fname, lname, dept, matric, rep in student_data:
    u, created = User.objects.get_or_create(username=uname, defaults={
        'email': f'{uname}@unn.edu.ng', 'first_name': fname, 'last_name': lname,
        'role': 'student', 'school': unn, 'department': dept, 'matric_number': matric, 'reputation': rep,
    })
    if created:
        u.set_password('student123')
        u.save()
    students[uname] = u

for uname in ['emeka_eze', 'ngozi_obi', 'chidi_nwosu', 'adaeze_onwu', 'kelechi_agu', 'dr.okafor']:
    u = User.objects.filter(username=uname).first()
    if u:
        students[uname] = u

all_students = list(students.values())

def get_student(name):
    return students.get(name)

extra_threads = [
    (courses['CSC 405'], 'blessing_nnaji', 'Agile vs Waterfall — which should I use for my capstone?',
     "My project supervisor wants a methodology section in my report. I've been reading about Agile and Waterfall but I'm not sure which fits a solo/small-group final year project better. Any real experience with this?",
     'open', False, ['project']),
    (courses['CSC 403'], 'tobi_akin', 'TCP vs UDP — simple explanation needed',
     "I get that TCP is reliable and UDP is faster, but I don't fully understand the handshake process or why UDP is used for streaming/gaming. Can someone break it down?",
     'resolved', False, ['lecture']),
    (courses['MEG 301'], 'daniel_okoro', 'Confused about the First Law of Thermodynamics in closed systems',
     "The lecturer's example on energy balance for a piston-cylinder system didn't click for me. Can someone explain with a simpler worked example?",
     'open', False, ['lecture', 'exam']),
    (courses['MED 301'], 'fatima_musa', 'Best way to memorize cranial nerves?',
     "We have a practical exam coming up and I keep mixing up the 12 cranial nerves and their functions. Any mnemonics or study techniques that actually worked for people?",
     'open', False, ['practical', 'exam']),
    (courses['ACC 201'], 'grace_udo', 'Difference between accrual and cash basis accounting?',
     "Our lecturer briefly mentioned this but didn't go deep. For the assignment, do I need to show journal entries under both methods or just explain the concept?",
     'resolved', False, ['assignment']),
    (courses['LAW 301'], 'ibrahim_yusuf', 'Elements of a valid contract — is consideration always required?',
     "I know offer, acceptance, consideration and intention to create legal relations are the main elements, but are there exceptions where consideration isn't needed? Thinking about deeds specifically.",
     'open', False, ['lecture']),
    (courses['MTH 301'], 'samuel_afolabi', 'Struggling with epsilon-delta proofs',
     "I understand the intuition behind limits but writing formal epsilon-delta proofs is really hard for me. Does anyone have a step-by-step approach they follow?",
     'open', True, ['exam']),
    (courses['CSC 407'], 'chiamaka_igwe', 'How do neural networks actually learn? Backpropagation confusion',
     "I understand forward pass but backpropagation and gradient descent together are confusing me. Is there a good way to think about this without getting lost in the calculus?",
     'resolved', False, ['lecture', 'assignment']),
]

created_threads = {}
for course, author_uname, title, content, status, pinned, tag_names in extra_threads:
    author = get_student(author_uname)
    if not author:
        continue
    t, created = Thread.objects.get_or_create(
        title=title,
        defaults={
            'course': course, 'author': author, 'content': content,
            'status': status, 'is_pinned': pinned, 'views': random.randint(20, 140),
        }
    )
    if created:
        for tn in tag_names:
            if tn in tags:
                t.tags.add(tags[tn])
    created_threads[title] = t

# Replies for the new threads
reply_map = [
    ('TCP vs UDP', 'blessing_nnaji',
     "TCP does a 3-way handshake (SYN, SYN-ACK, ACK) before sending data — this guarantees the connection is live on both ends and packets arrive in order, retransmitting if lost. That reliability adds overhead.\n\n"
     "UDP just fires packets with no handshake or guarantee of delivery/order. That's why it's faster and preferred for video calls or gaming — a dropped frame is better than a laggy delayed one.\n\n"
     "Rule of thumb: use TCP when correctness matters more than speed (file transfer, web pages), UDP when speed matters more than perfect delivery (live streaming, VoIP).",
     True, 'dr.okafor'),
    ('accrual and cash basis', 'samuel_afolabi',
     "Cash basis: you record revenue/expenses only when cash actually changes hands. Simple but doesn't match income to the period it was earned in.\n\n"
     "Accrual basis: you record revenue when earned and expenses when incurred, regardless of when cash moves. This is what GAAP/IFRS require for most businesses since it gives a truer picture of profitability.\n\n"
     "For your assignment I'd show journal entries under both — it makes the timing difference obvious to whoever grades it.",
     True, None),
    ('backpropagation', 'tobi_akin',
     "Think of it as the chain rule applied backwards through the network. Forward pass computes the output and the error (loss). Backprop then asks: 'how much did each weight contribute to that error?' and nudges each weight a little in the direction that reduces the error — that's gradient descent.\n\n"
     "The 'backward' part just means you compute these contribution values (gradients) starting from the output layer and working back to the input layer, reusing calculations layer by layer instead of redoing everything — that's what makes it efficient.",
     True, 'dr.okafor'),
]
for title_fragment, author_uname, content, verified, verifier_uname in reply_map:
    thread = next((t for k, t in created_threads.items() if title_fragment in k), None)
    author = get_student(author_uname)
    if not thread or not author or thread.replies.exists():
        continue
    verifier = None
    if verifier_uname:
        verifier = User.objects.filter(username=verifier_uname).first()
    Reply.objects.create(
        thread=thread, author=author, content=content,
        is_verified=verified, verified_by=verifier
    )

# A couple of un-verified, casual back-and-forth replies on open threads
casual_replies = [
    ('Agile vs Waterfall', 'tobi_akin', "I used a lightweight Agile approach (2-week sprints) for mine last session — worked well because requirements kept shifting as my supervisor gave feedback. Waterfall would've meant redoing whole sections."),
    ('Agile vs Waterfall', 'chiamaka_igwe', "Agree with Tobi. Also most supervisors expect to see 'iterations' in your Chapter 4 writeup, which naturally fits Agile language better."),
    ('cranial nerves', 'grace_udo', "Not medicine but I've heard 'Oh Oh Oh To Touch And Feel Very Good Velvet, Ah Heaven' is a classic mnemonic for the 12 nerves in order — might be worth googling the full version."),
    ('First Law of Thermodynamics', 'samuel_afolabi', "Try drawing the system boundary first before writing any equation — half my classmates' mistakes came from not being clear on what's inside vs outside the control volume."),
]
for title_fragment, author_uname, content in casual_replies:
    thread = next((t for k, t in created_threads.items() if title_fragment in k), None)
    author = get_student(author_uname)
    if not thread or not author:
        continue
    if not thread.replies.filter(content=content).exists():
        Reply.objects.create(thread=thread, author=author, content=content)

# ---------------------------------------------------------------------------
# 4. Chat rooms + messages (direct messages between pairs of users)
# ---------------------------------------------------------------------------
def get_or_create_room(user_a, user_b):
    room = ChatRoom.objects.filter(participants=user_a).filter(participants=user_b).first()
    if room:
        return room, False
    room = ChatRoom.objects.create()
    room.participants.add(user_a, user_b)
    return room, True

chat_conversations = [
    ('tobi_akin', 'blessing_nnaji', [
        ('tobi_akin', "Hey, did you finish the CSC 405 group presentation slides?"),
        ('blessing_nnaji', "Almost! I'm stuck on the architecture diagram section, can you help after class?"),
        ('tobi_akin', "Sure, I'll be free by 4pm. Send me what you have so far."),
        ('blessing_nnaji', "Just sent it to your email. Thanks a lot!"),
        ('tobi_akin', "Got it, looking now. This is actually solid, just needs the deployment layer added."),
    ]),
    ('fatima_musa', 'grace_udo', [
        ('fatima_musa', "Are you going for the study group tomorrow?"),
        ('grace_udo', "Yes! What time and where again?"),
        ('fatima_musa', "5pm at the faculty library, third floor."),
        ('grace_udo', "Perfect, see you there. Bring your anatomy atlas if you can."),
    ]),
    ('samuel_afolabi', 'chiamaka_igwe', [
        ('samuel_afolabi', "Your reply on the backprop thread finally made it click for me, thank you!"),
        ('chiamaka_igwe', "Glad it helped! It confused me for weeks too before it clicked."),
        ('samuel_afolabi', "Do you have notes on gradient descent variants (Adam, RMSprop etc)? We might need it for the AI course project."),
        ('chiamaka_igwe', "I do, let me export them and send over tonight."),
    ]),
    ('daniel_okoro', 'ibrahim_yusuf', [
        ('daniel_okoro', "Random question — are you still doing the joint hostel dues collection?"),
        ('ibrahim_yusuf', "Yeah, until Friday. You can drop yours with the porter."),
        ('daniel_okoro', "Noted, will do it tomorrow."),
    ]),
    ('emeka_eze', 'ngozi_obi', [
        ('emeka_eze', "Thanks for the merge sort vs quick sort explanation on the forum, super clear."),
        ('ngozi_obi', "No wasahala, glad it helped for the exam prep."),
        ('emeka_eze', "Are you attempting the DBMS assignment on isolation levels too?"),
        ('ngozi_obi', "Yes, still reading up on it. Let's compare answers before submission."),
    ]),
]

msg_count = 0
room_count = 0
for uname_a, uname_b, messages in chat_conversations:
    user_a = students.get(uname_a) or User.objects.filter(username=uname_a).first()
    user_b = students.get(uname_b) or User.objects.filter(username=uname_b).first()
    if not user_a or not user_b:
        continue
    room, created_room = get_or_create_room(user_a, user_b)
    if created_room:
        room_count += 1
    if room.messages.exists():
        continue  # already seeded this conversation
    for sender_uname, content in messages:
        sender = user_a if sender_uname == uname_a else user_b
        ChatMessage.objects.create(room=room, sender=sender, content=content)
        msg_count += 1

print("Expanded seed complete!")

# --- Nationwide demo: a second institution, isolated from UNN -------------
unilag, _ = School.objects.get_or_create(
    name='University of Lagos',
    defaults={'short_name': 'UNILAG', 'school_type': 'university', 'state': 'Lagos'},
)
unilag_csc, _ = Department.objects.get_or_create(
    school=unilag, code='CSC',
    defaults={'name': 'Computer Science', 'faculty': 'Faculty of Science',
              'description': 'Software engineering, AI, and systems at UNILAG.',
              'color': '#6C63FF', 'icon': 'bi-cpu'}
)
unilag_csc201, _ = Course.objects.get_or_create(
    department=unilag_csc, code='CSC 201',
    defaults={'title': 'Introduction to Computer Science', 'level': '200L',
              'semester': 'First Semester', 'units': 3}
)
unilag_student, created = User.objects.get_or_create(
    username='tunde_bakare_unilag',
    defaults={
        'email': 'tunde.bakare@unilag.edu.ng', 'first_name': 'Tunde', 'last_name': 'Bakare',
        'role': 'student', 'school': unilag, 'department': unilag_csc,
        'matric_number': '190403010', 'reputation': 40,
    },
)
if created:
    unilag_student.set_password('student123')
    unilag_student.save()
Thread.objects.get_or_create(
    course=unilag_csc201, author=unilag_student,
    title='Best resources for learning Python at UNILAG CSC 201?',
    defaults={
        'content': "Looking for recommended textbooks or online resources for our CSC 201 Python module. What did previous students use?",
        'status': 'open',
    },
)
print(f"  Schools: {School.objects.count()} (includes a UNILAG demo institution to prove cross-school isolation)")
print(f"  Departments: {Department.objects.count()}")
print(f"  Courses: {Course.objects.count()}")
print(f"  Users: {User.objects.count()}")
print(f"  Threads: {Thread.objects.count()}")
print(f"  Replies: {Reply.objects.count()}")
print(f"  Chat rooms: {ChatRoom.objects.count()} (created {room_count} new)")
print(f"  Chat messages: {ChatMessage.objects.count()} (created {msg_count} new)")
print()
print("New login credentials (password in parentheses):")
print("  Lecturers: dr.nwachukwu, prof.balogun, dr.eze (lecturer123)")
print("  Students: tobi_akin, fatima_musa, daniel_okoro, blessing_nnaji,")
print("            ibrahim_yusuf, grace_udo, samuel_afolabi, chiamaka_igwe (student123)")