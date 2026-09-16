"""
seed_nationwide.py

Populates departments, courses, a demo student (and lecturer, for
universities), and a starter discussion thread for EVERY School already in
the database. Safe to re-run: everything uses get_or_create, so running it
twice will not create duplicates.

Usage:
    python manage.py shell < seed_nationwide.py
or
    python seed_nationwide.py   (after django.setup())
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniconnect.settings')
django.setup()

from django.utils.text import slugify
from forum.models import School, Department, Course, Thread, Tag
from accounts.models import User


# ---------------------------------------------------------------------------
# Department templates, per institution type
# ---------------------------------------------------------------------------

UNIVERSITY_DEPTS = [
    ('Computer Science', 'CSC', 'Faculty of Physical Sciences',
     'Programming, algorithms, AI, databases and software engineering.', '#6C63FF', 'bi-cpu'),
    ('Mechanical Engineering', 'MEG', 'Faculty of Engineering',
     'Thermodynamics, fluid mechanics, machine design.', '#f59e0b', 'bi-gear'),
    ('Medicine & Surgery', 'MED', 'College of Medicine',
     'Clinical medicine, surgery, pharmacology.', '#ef4444', 'bi-heart-pulse'),
    ('Economics', 'ECO', 'Faculty of Social Sciences',
     'Microeconomics, macroeconomics, econometrics.', '#10b981', 'bi-graph-up'),
    ('Law', 'LAW', 'Faculty of Law',
     'Constitutional law, commercial law, criminal law.', '#3b82f6', 'bi-book'),
    ('English & Literary Studies', 'ENG', 'Faculty of Arts',
     'Literature, linguistics, creative writing.', '#ec4899', 'bi-pen'),
    ('Mathematics', 'MTH', 'Faculty of Physical Sciences',
     'Pure mathematics, applied mathematics, statistics.', '#8b5cf6', 'bi-calculator'),
    ('Physics', 'PHY', 'Faculty of Physical Sciences',
     'Classical mechanics, quantum physics, electromagnetism.', '#06b6d4', 'bi-lightning'),
    ('Accountancy', 'ACC', 'Faculty of Social Sciences',
     'Financial accounting, auditing, taxation.', '#22c55e', 'bi-cash-coin'),
    ('Political Science', 'POL', 'Faculty of Social Sciences',
     'Government, public policy, international relations.', '#f97316', 'bi-bank'),
]

POLYTECHNIC_DEPTS = [
    ('Computer Science', 'CSC', 'School of Science & Technology',
     'Software development, networking and systems administration.', '#6C63FF', 'bi-cpu'),
    ('Accountancy', 'ACC', 'School of Business Studies',
     'Financial accounting, auditing, taxation.', '#22c55e', 'bi-cash-coin'),
    ('Business Administration & Management', 'BAM', 'School of Business Studies',
     'Management principles, entrepreneurship, marketing.', '#f59e0b', 'bi-briefcase'),
    ('Mass Communication', 'MCM', 'School of Communication & Media Studies',
     'Journalism, broadcasting, public relations.', '#ec4899', 'bi-broadcast'),
    ('Estate Management', 'ESM', 'School of Environmental Studies',
     'Property valuation, land economics, facilities management.', '#10b981', 'bi-building'),
    ('Electrical/Electronics Engineering Technology', 'EEE', 'School of Engineering',
     'Power systems, electronics, telecommunications.', '#3b82f6', 'bi-lightning-charge'),
    ('Mechanical Engineering Technology', 'MET', 'School of Engineering',
     'Manufacturing, thermodynamics, machine design.', '#f97316', 'bi-gear'),
]

COLLEGE_OF_EDUCATION_DEPTS = [
    ('Educational Foundations', 'EDF', 'Faculty of Education',
     'Philosophy, history and sociology of education.', '#8b5cf6', 'bi-mortarboard'),
    ('English Education', 'ENG', 'Faculty of Education',
     'Language teaching methodology and literature.', '#ec4899', 'bi-pen'),
    ('Mathematics Education', 'MTE', 'Faculty of Education',
     'Pedagogy for teaching mathematics at secondary level.', '#8b5cf6', 'bi-calculator'),
    ('Integrated Science Education', 'ISE', 'Faculty of Education',
     'Teaching methods for basic science subjects.', '#06b6d4', 'bi-flask'),
    ('Social Studies Education', 'SSE', 'Faculty of Education',
     'Civics, government and social studies pedagogy.', '#f97316', 'bi-people'),
    ('Computer Science Education', 'CSE', 'Faculty of Education',
     'Teaching methodology for computing and ICT.', '#6C63FF', 'bi-cpu'),
]

# Monotechnics are specialised — keyed by a short_name substring, with a
# generic fallback for any monotechnic not explicitly listed.
MONOTECHNIC_DEPTS = {
    'FCFMT': [
        ('Fisheries Technology', 'FIS', 'School of Fisheries & Aquaculture',
         'Fish farming, aquaculture and fisheries management.', '#06b6d4', 'bi-water'),
        ('Nautical Science', 'NTS', 'School of Maritime Studies',
         'Navigation, seamanship and maritime law.', '#3b82f6', 'bi-compass'),
        ('Marine Engineering', 'MEN', 'School of Maritime Studies',
         'Ship propulsion systems and marine machinery.', '#f97316', 'bi-gear'),
    ],
    'NCAT': [
        ('Aircraft Maintenance Engineering', 'AME', 'School of Engineering',
         'Airframe, powerplant and avionics maintenance.', '#f97316', 'bi-airplane'),
        ('Air Traffic Control', 'ATC', 'School of Flight Operations',
         'Radar procedures, airspace management, aviation communication.', '#06b6d4', 'bi-broadcast-pin'),
        ('Aviation Management', 'AVM', 'School of Management Technology',
         'Airport operations, airline management and aviation safety.', '#8b5cf6', 'bi-briefcase'),
    ],
}
GENERIC_MONOTECHNIC_DEPTS = [
    ('General Studies', 'GNS', 'School of General Studies',
     'Communication skills and foundational studies.', '#6C63FF', 'bi-book'),
    ('Technology Management', 'TEM', 'School of Management Technology',
     'Applied technology and industrial management.', '#f97316', 'bi-briefcase'),
]

FIRST_NAMES = ['Chinedu', 'Amaka', 'Ibrahim', 'Fatima', 'Tunde', 'Ngozi', 'Emeka', 'Aisha',
               'Bolaji', 'Chiamaka', 'Yusuf', 'Halima', 'Obinna', 'Funmilayo', 'Sani', 'Grace']
LAST_NAMES = ['Okafor', 'Bello', 'Adewale', 'Musa', 'Eze', 'Yusuf', 'Ogunleye', 'Danladi',
              'Nwachukwu', 'Abubakar', 'Balogun', 'Suleiman', 'Chukwu', 'Garba', 'Adeyemi', 'Lawal']


def dept_list_for(school):
    if school.school_type == 'university':
        return UNIVERSITY_DEPTS
    if school.school_type == 'polytechnic':
        return POLYTECHNIC_DEPTS
    if school.school_type == 'college_of_education':
        return COLLEGE_OF_EDUCATION_DEPTS
    if school.school_type == 'monotechnic':
        for key, depts in MONOTECHNIC_DEPTS.items():
            if key in (school.short_name or '') or key.lower() in school.name.lower():
                return depts
        return GENERIC_MONOTECHNIC_DEPTS
    return GENERIC_MONOTECHNIC_DEPTS


def make_courses(department, dept_short_code):
    """Two plausible courses per department: an intro (200L) and an
    intermediate (300L) course."""
    courses = []
    intro, _ = Course.objects.get_or_create(
        department=department, code=f'{dept_short_code} 201',
        defaults={
            'title': f'Introduction to {department.name}',
            'description': f'Foundational concepts in {department.name.lower()}.',
            'level': '200L', 'semester': 'First Semester', 'units': 3,
        }
    )
    courses.append(intro)
    inter, _ = Course.objects.get_or_create(
        department=department, code=f'{dept_short_code} 301',
        defaults={
            'title': f'{department.name} II',
            'description': f'Intermediate topics in {department.name.lower()}.',
            'level': '300L', 'semester': 'Second Semester', 'units': 3,
        }
    )
    courses.append(inter)
    return courses


def make_username(school, first, last, suffix):
    base = f'{first.lower()}_{last.lower()}_{slugify(school.short_name or school.name)[:10]}_{suffix}'
    return base


def seed():
    tag_names = [('exam', '#f59e0b'), ('assignment', '#6C63FF'), ('lecture', '#10b981'),
                 ('practical', '#ef4444'), ('textbook', '#8b5cf6')]
    tags = {}
    for name, color in tag_names:
        t, _ = Tag.objects.get_or_create(name=name, defaults={'color': color})
        tags[name] = t

    schools = School.objects.all().order_by('name')
    print(f'Found {schools.count()} schools. Seeding departments/courses/demo users/threads...\n')

    for school in schools:
        existing_depts = Department.objects.filter(school=school).count()
        dept_templates = dept_list_for(school)

        created_departments = []
        for name, code, faculty, desc, color, icon in dept_templates:
            dept, created = Department.objects.get_or_create(
                school=school, code=code,
                defaults={'name': name, 'faculty': faculty, 'description': desc,
                          'color': color, 'icon': icon}
            )
            created_departments.append(dept)

        # Courses for every department belonging to this school (idempotent).
        all_courses = []
        for dept in Department.objects.filter(school=school):
            courses = make_courses(dept, dept.code)
            all_courses.extend(courses)

        # One demo student (every school) + one demo lecturer (universities only).
        primary_dept = created_departments[0] if created_departments else Department.objects.filter(school=school).first()

        school_slug = slugify(school.short_name or school.name)[:10]
        idx = school.pk  # deterministic per-school index, independent of iteration order

        # Idempotency guard: if this school already has a demo account
        # (matching the naming convention used by this script, regardless of
        # which first/last name a previous run picked), reuse it instead of
        # generating a new one. This keeps re-runs stable even if the school
        # list changes order or a new school is inserted between two
        # existing ones.
        student = User.objects.filter(
            school=school, username__endswith=f'_{school_slug}_student'
        ).first()

        if student is None:
            first = FIRST_NAMES[idx % len(FIRST_NAMES)]
            last = LAST_NAMES[idx % len(LAST_NAMES)]
            student_username = make_username(school, first, last, 'student')
            student = User.objects.create(
                username=student_username,
                email=f'{student_username}@{school_slug}.edu.ng',
                first_name=first, last_name=last,
                role='student', school=school, department=primary_dept,
                matric_number=f'{slugify(school.short_name or "SCH")[:6].upper()}/{2020 + (idx % 5)}/{1000 + idx}',
                reputation=15 + (idx * 3) % 80,
            )
            student.set_password('student123')
            student.save()

        lecturer = None
        if school.school_type == 'university' and primary_dept:
            lecturer = User.objects.filter(
                school=school, username__endswith=f'_{school_slug}_lecturer'
            ).first()
            if lecturer is None:
                lfirst = FIRST_NAMES[(idx + 3) % len(FIRST_NAMES)]
                llast = LAST_NAMES[(idx + 3) % len(LAST_NAMES)]
                lecturer_username = make_username(school, lfirst, llast, 'lecturer')
                lecturer = User.objects.create(
                    username=lecturer_username,
                    email=f'{lecturer_username}@{school_slug}.edu.ng',
                    first_name=lfirst, last_name=llast,
                    role='lecturer', school=school, department=primary_dept,
                    reputation=200 + (idx * 7) % 150,
                )
                lecturer.set_password('lecturer123')
                lecturer.save()

        # A starter discussion thread so the school isn't empty.
        if primary_dept:
            first_course = Course.objects.filter(department=primary_dept).order_by('code').first()
            if first_course and not Thread.objects.filter(course=first_course, author=student).exists():
                thread = Thread.objects.create(
                    course=first_course,
                    author=student,
                    title=f'Welcome {school.short_name or school.name} students — introduce yourselves!',
                    content=(
                        f'Hi everyone, I am a {primary_dept.name} student at '
                        f'{school.name}. Excited to use Uni-Connect to discuss '
                        f'coursework, share notes, and prepare for exams together. '
                        f'Drop a reply below and say hello!'
                    ),
                    status='open',
                )
                thread.tags.add(tags['lecture'])

        print(f'  [{school.short_name or school.name}] '
              f'{Department.objects.filter(school=school).count()} depts, '
              f'{sum(1 for c in all_courses)} courses touched, '
              f'demo student: {student.username}' +
              (f', demo lecturer: {lecturer.username}' if lecturer else ''))

    print('\nDone.')
    print(f'Totals -> Schools: {School.objects.count()}, '
          f'Departments: {Department.objects.count()}, '
          f'Courses: {Course.objects.count()}, '
          f'Users: {User.objects.count()}, '
          f'Threads: {Thread.objects.count()}')


if __name__ == '__main__':
    seed()
