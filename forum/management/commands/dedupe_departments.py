from django.core.management.base import BaseCommand
from django.db import transaction
from forum.models import Department, Course

ICON_MAP = {
    'computer science': ('bi-cpu', '#6C63FF'),
    'mechanical engineering': ('bi-gear', '#f59e0b'),
    'medicine & surgery': ('bi-heart-pulse', '#ef4444'),
    'economics': ('bi-graph-up', '#10b981'),
    'law': ('bi-book', '#3b82f6'),
    'english & literary studies': ('bi-pen', '#ec4899'),
    'mathematics': ('bi-calculator', '#8b5cf6'),
    'physics': ('bi-lightning', '#06b6d4'),
    'accountancy': ('bi-cash-coin', '#22c55e'),
    'political science': ('bi-bank', '#f97316'),
    'business administration & management': ('bi-briefcase', '#f59e0b'),
    'mass communication': ('bi-broadcast', '#ec4899'),
    'estate management': ('bi-building', '#10b981'),
    'electrical/electronics engineering technology': ('bi-lightning-charge', '#3b82f6'),
    'mechanical engineering technology': ('bi-gear', '#f97316'),
    'educational foundations': ('bi-mortarboard', '#8b5cf6'),
    'mathematics education': ('bi-calculator', '#8b5cf6'),
    'integrated science education': ('bi-flask', '#06b6d4'),
    'social studies education': ('bi-people', '#f97316'),
    'computer science education': ('bi-cpu', '#6C63FF'),
}


class Command(BaseCommand):
    help = 'Merge duplicate departments (same school + name) and correct mismatched icons/colors.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Report what would change without saving anything.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        seen = {}
        merged = 0

        for dept in Department.objects.select_related('school').order_by('id'):
            key = (dept.school_id, dept.name.strip().lower())
            if key not in seen:
                seen[key] = dept
                continue

            keeper = seen[key]
            self.stdout.write(f'Duplicate: "{dept.name}" at {dept.school} — '
                               f'merging id={dept.id} into id={keeper.id}')
            if not dry_run:
                with transaction.atomic():
                    Course.objects.filter(department=dept).update(department=keeper)
                    dept.delete()
            merged += 1

        fixed_icons = 0
        for dept in Department.objects.all():
            mapping = ICON_MAP.get(dept.name.strip().lower())
            if mapping and (dept.icon, dept.color) != mapping:
                self.stdout.write(f'Icon mismatch: "{dept.name}" at {dept.school} — '
                                   f'{dept.icon} -> {mapping[0]}')
                if not dry_run:
                    dept.icon, dept.color = mapping
                    dept.save(update_fields=['icon', 'color'])
                fixed_icons += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n{"[DRY RUN] " if dry_run else ""}Merged {merged} duplicate department(s), '
            f'fixed {fixed_icons} icon/color mismatch(es).'
        ))