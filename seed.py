import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniconnect.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from forum.models import School, Department, Course, Thread, Reply, Tag
from accounts.models import User


# Tags
tags = {}
for name, color in [('exam', '#f59e0b'), ('assignment', '#6C63FF'), ('lecture', '#10b981'), ('practical', '#ef4444'), ('textbook', '#8b5cf6')]:
    t, _ = Tag.objects.get_or_create(name=name, defaults={'color': color})
    tags[name] = t

# School
unn, _ = School.objects.get_or_create(
    name='University of Nigeria, Nsukka',
    defaults={'short_name': 'UNN', 'school_type': 'university', 'state': 'Enugu'},
)

# Departments
dept_data = [
    ('Computer Science', 'CSC', 'Faculty of Physical Sciences', 'Programming, algorithms, AI, databases and software engineering.', '#6C63FF', 'bi-cpu'),
    ('Mechanical Engineering', 'MEG', 'Faculty of Engineering', 'Thermodynamics, fluid mechanics, machine design.', '#f59e0b', 'bi-gear'),
    ('Medicine & Surgery', 'MED', 'College of Medicine', 'Clinical medicine, surgery, pharmacology.', '#ef4444', 'bi-heart-pulse'),
    ('Economics', 'ECO', 'Faculty of Social Sciences', 'Microeconomics, macroeconomics, econometrics.', '#10b981', 'bi-graph-up'),
    ('Law', 'LAW', 'Faculty of Law', 'Constitutional law, commercial law, criminal law.', '#3b82f6', 'bi-book'),
    ('English & Literary Studies', 'ENG', 'Faculty of Arts', 'Literature, linguistics, creative writing.', '#ec4899', 'bi-pen'),
    ('Mathematics', 'MTH', 'Faculty of Physical Sciences', 'Pure mathematics, applied mathematics, statistics.', '#8b5cf6', 'bi-calculator'),
    ('Physics', 'PHY', 'Faculty of Physical Sciences', 'Classical mechanics, quantum physics, electromagnetism.', '#06b6d4', 'bi-lightning'),
]
depts = {}
for name, code, faculty, desc, color, icon in dept_data:
    d, _ = Department.objects.get_or_create(school=unn, code=code, defaults={
        'name': name, 'faculty': faculty, 'description': desc, 'color': color, 'icon': icon
    })
    depts[code] = d

# Courses
csc = depts['CSC']
meg = depts['MEG']
med = depts['MED']
eco = depts['ECO']
mth = depts['MTH']

course_data = [
    (csc, 'CSC 201', 'Introduction to Computer Science', '200L', 'First Semester', 3),
    (csc, 'CSC 301', 'Data Structures and Algorithms', '300L', 'First Semester', 3),
    (csc, 'CSC 303', 'Database Management Systems', '300L', 'Second Semester', 3),
    (csc, 'CSC 401', 'Operating Systems', '400L', 'First Semester', 3),
    (csc, 'CSC 403', 'Computer Networks', '400L', 'Second Semester', 3),
    (csc, 'CSC 407', 'Artificial Intelligence', '400L', 'First Semester', 3),
    (meg, 'MEG 201', 'Engineering Mathematics I', '200L', 'First Semester', 3),
    (meg, 'MEG 301', 'Thermodynamics', '300L', 'First Semester', 3),
    (meg, 'MEG 303', 'Fluid Mechanics', '300L', 'Second Semester', 3),
    (med, 'MED 301', 'Anatomy and Physiology', '300L', 'First Semester', 6),
    (med, 'MED 401', 'Pharmacology', '400L', 'First Semester', 6),
    (eco, 'ECO 201', 'Microeconomics I', '200L', 'First Semester', 3),
    (eco, 'ECO 301', 'Macroeconomics', '300L', 'First Semester', 3),
    (mth, 'MTH 201', 'Mathematical Methods', '200L', 'First Semester', 3),
    (mth, 'MTH 301', 'Real Analysis', '300L', 'First Semester', 3),
]
courses = {}
for dept, code, title, level, sem, units in course_data:
    c, _ = Course.objects.get_or_create(department=dept, code=code, defaults={
        'title': title, 'level': level, 'semester': sem, 'units': units
    })
    courses[code] = c

# Users
admin_user, _ = User.objects.get_or_create(username='admin', defaults={
    'email': 'admin@unn.edu.ng', 'first_name': 'Admin', 'last_name': 'UNN',
    'role': 'admin', 'is_staff': True, 'is_superuser': True, 'reputation': 500, 'school': unn,
})
if _:
    admin_user.set_password('admin123')
    admin_user.save()

lecturer1, _ = User.objects.get_or_create(username='dr.okafor', defaults={
    'email': 'okafor@unn.edu.ng', 'first_name': 'Dr. Chukwuemeka', 'last_name': 'Okafor',
    'role': 'lecturer', 'school': unn, 'department': csc, 'reputation': 320,
})
if _:
    lecturer1.set_password('lecturer123')
    lecturer1.save()

students = []
student_data = [
    ('emeka_eze', 'Emeka', 'Eze', csc, '2020/242345', 150),
    ('ngozi_obi', 'Ngozi', 'Obi', csc, '2020/242346', 230),
    ('chidi_nwosu', 'Chidi', 'Nwosu', meg, '2020/242400', 80),
    ('adaeze_onwu', 'Adaeze', 'Onwudiwe', med, '2020/242500', 175),
    ('kelechi_agu', 'Kelechi', 'Aguocha', eco, '2020/242600', 60),
]
for uname, fname, lname, dept, matric, rep in student_data:
    u, _ = User.objects.get_or_create(username=uname, defaults={
        'email': f'{uname}@unn.edu.ng', 'first_name': fname, 'last_name': lname,
        'role': 'student', 'school': unn, 'department': dept, 'matric_number': matric, 'reputation': rep,
    })
    if _:
        u.set_password('student123')
        u.save()
    students.append(u)

emeka, ngozi, chidi, adaeze, kelechi = students
csc301 = courses['CSC 301']
csc303 = courses['CSC 303']
csc407 = courses['CSC 407']
mth201 = courses['MTH 201']
eco201 = courses['ECO 201']

# Threads
threads_data = [
    (csc301, emeka, 'How does Big O notation work for nested loops?',
     "I'm struggling to understand how to calculate the time complexity of nested for loops. For example, if I have a loop inside another loop that both go from 0 to n, is it always O(n²)? What if the inner loop doesn't always run n times?",
     'open', False, ['exam']),
    (csc301, ngozi, 'Difference between merge sort and quick sort?',
     "The lecturer explained merge sort and quick sort but I'm confused about when to use each one. Both have O(n log n) average complexity right? Why does quicksort sometimes perform better in practice?",
     'resolved', False, ['lecture', 'exam']),
    (csc303, emeka, 'ACID properties — can someone explain Isolation?',
     "I understand Atomicity, Consistency and Durability, but Isolation is confusing me. Does it mean transactions can never see each other's data at all? What about read-committed isolation level?",
     'open', True, ['assignment']),
    (csc407, ngozi, 'What is the difference between supervised and unsupervised learning?',
     "I know supervised learning uses labeled data and unsupervised doesn't, but I want a deeper understanding. When would you choose one over the other? And where does reinforcement learning fit?",
     'resolved', False, ['lecture']),
    (mth201, emeka, 'How do I solve differential equations using integrating factor method?',
     "We covered this in class but the steps are still unclear to me. Specifically, I'm stuck on first-order linear ODEs of the form dy/dx + P(x)y = Q(x). Can someone walk through an example step by step?",
     'open', False, ['exam', 'assignment']),
    (eco201, kelechi, 'What is the price elasticity of demand and how do you calculate it?',
     "I have an assignment asking me to calculate PED for different goods. I know the formula involves percentage changes but I keep getting confused about whether to use initial or midpoint values.",
     'open', False, ['assignment']),
    (csc301, chidi, 'Stack vs Queue — which data structure should I use?',
     "I have a practical coming up and the question says 'choose the most appropriate data structure for a print spooler'. I think it's a queue (FIFO) but my friend says stack. Can someone clarify?",
     'resolved', False, ['practical']),
]

for course, author, title, content, status, pinned, tag_names in threads_data:
    t, created = Thread.objects.get_or_create(
        title=title,
        defaults={
            'course': course, 'author': author, 'content': content,
            'status': status, 'is_pinned': pinned, 'views': 0,
        }
    )
    if created:
        for tn in tag_names:
            if tn in tags:
                t.tags.add(tags[tn])
        t.views = __import__('random').randint(15, 120)
        t.save()

# Replies for resolved threads
t1 = Thread.objects.get(title__contains='merge sort')
if not t1.replies.exists():
    r1 = Reply.objects.create(
        thread=t1, author=lecturer1,
        content="Great question! Both have O(n log n) average time complexity, but here's the key difference:\n\n**Merge Sort:**\n- Always O(n log n) — even worst case\n- Stable sort (preserves order of equal elements)\n- Requires O(n) extra memory for merging\n- Better for linked lists and external sorting\n\n**Quick Sort:**\n- Average O(n log n) but worst case O(n²) — usually avoided with good pivot selection\n- In-place (O(log n) stack space)\n- Cache-friendly — better locality of reference\n- In practice, faster for arrays in memory\n\nUse Merge Sort when stability matters or memory isn't a concern. Quick Sort for in-memory arrays where raw speed matters.",
        is_verified=True, verified_by=lecturer1
    )
    t1.status = 'resolved'
    t1.save()

t2 = Thread.objects.get(title__contains='supervised')
if not t2.replies.exists():
    Reply.objects.create(
        thread=t2, author=ngozi,
        content="Here's how I understand it:\n\n**Supervised Learning:** You have labeled training data — every input has a correct output. The model learns to map inputs to outputs. Examples: image classification, spam detection, price prediction.\n\n**Unsupervised Learning:** No labels. The model finds patterns, clusters, or structure in the data itself. Examples: customer segmentation, anomaly detection, topic modeling.\n\n**Reinforcement Learning:** The model learns by trial and error, receiving rewards or penalties. Used in game AI, robotics, recommendation systems.\n\nChoose supervised when you have labeled data and a specific prediction task. Choose unsupervised for exploratory analysis or when labeling is expensive.",
        is_verified=True, verified_by=lecturer1
    )
    t2.status = 'resolved'
    t2.save()

t3 = Thread.objects.get(title__contains='Stack vs Queue')
if not t3.replies.exists():
    Reply.objects.create(
        thread=t3, author=ngozi,
        content="Your instinct is right — a print spooler should use a **Queue (FIFO)**!\n\nThe logic: print jobs should be processed in the order they arrive — first in, first out. If you sent your assignment to print and then someone else prints after you, yours should print first.\n\nA Stack (LIFO) would mean the last print job sent gets printed first — that's obviously unfair and would be terrible UX.\n\nQueue use cases: print spoolers, task scheduling, BFS traversal, process management in OS.\nStack use cases: undo operations, call stack in programs, DFS traversal, expression evaluation.",
        is_verified=True, verified_by=emeka
    )
    t3.status = 'resolved'
    t3.save()

# Add some non-verified replies to open threads
t4 = Thread.objects.get(title__contains='Big O')
if not t4.replies.exists():
    Reply.objects.create(
        thread=t4, author=ngozi,
        content="For nested loops where both go from 0 to n, yes it's O(n²). But the key is to count iterations carefully:\n\nIf inner loop goes from 0 to i (not n), the total iterations = 0+1+2+...+(n-1) = n(n-1)/2 which is still O(n²).\n\nBut if inner loop goes from 0 to a constant k regardless of n, then it's O(n) × O(1) = O(n).\n\nTip: Always look at what the loop variable is bounded by, not just the loop structure itself."
    )

print("✅ Seed data created successfully!")
print(f"  Departments: {Department.objects.count()}")
print(f"  Courses: {Course.objects.count()}")
print(f"  Users: {User.objects.count()}")
print(f"  Threads: {Thread.objects.count()}")
print(f"  Replies: {Reply.objects.count()}")
print("\nLogin credentials:")
print("  Admin: admin / admin123")
print("  Lecturer: dr.okafor / lecturer123")
print("  Students: emeka_eze / student123")
