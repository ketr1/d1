from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Создает группы и права для редакторов'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Recipe)

        can_edit_all, _ = Permission.objects.get_or_create(
            codename='can_edit_all_recipes',
            name='Может редактировать любые рецепты',
            content_type=content_type,
        )

        can_delete_all, _ = Permission.objects.get_or_create(
            codename='can_delete_all_recipes',
            name='Может удалять любые рецепты',
            content_type=content_type,
        )

        editors_group, _ = Group.objects.get_or_create(name='Редакторы')
        editors_group.permissions.add(can_edit_all)

        moderators_group, _ = Group.objects.get_or_create(name='Модераторы')
        moderators_group.permissions.add(can_edit_all, can_delete_all)

        self.stdout.write(self.style.SUCCESS('Группы и права созданы:'))
        self.stdout.write(f'- Редакторы: могут редактировать любые рецепты')
        self.stdout.write(f'- Модераторы: могут редактировать и удалять любые рецепты')