from django.db import migrations
from django.utils.text import slugify


DEFAULT_SCHOOL_NAME = 'University of Nigeria, Nsukka'
DEFAULT_SCHOOL_SHORT = 'UNN'


def backfill_school(apps, schema_editor):
    """Every Department that existed before this upgrade belonged to UNN
    (the platform's original, single-institution scope). Create that School
    record and attach it to any Department that doesn't already have one, so
    no existing data is lost or orphaned.
    """
    School = apps.get_model('forum', 'School')
    Department = apps.get_model('forum', 'Department')

    school, _ = School.objects.get_or_create(
        name=DEFAULT_SCHOOL_NAME,
        defaults={
            'short_name': DEFAULT_SCHOOL_SHORT,
            'slug': slugify(DEFAULT_SCHOOL_SHORT),
            'school_type': 'university',
            'state': 'Enugu',
            'is_active': True,
        },
    )

    Department.objects.filter(school__isnull=True).update(school=school)


def noop_reverse(apps, schema_editor):
    # Intentionally left as a no-op: reversing would risk detaching
    # departments that legitimately belong to UNN.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_alter_department_code_school_department_school_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_school, noop_reverse),
    ]
