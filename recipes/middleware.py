import os

from django.contrib.auth import get_user_model
from django.db import DatabaseError


class RestoreMissingUserMiddleware:
    """
    Восстанавливает пользователя между экземплярами Vercel, у которых разные
    временные копии SQLite. Выполняется после SessionMiddleware и до
    AuthenticationMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.environ.get('VERCEL') == '1':
            user_id = request.session.get('_auth_user_id')
            snapshot = request.session.get('auth_user_snapshot')

            if user_id and snapshot and str(snapshot.get('id')) == str(user_id):
                try:
                    user_id = int(user_id)
                    User = get_user_model()
                    user_data = {
                        'username': snapshot['username'],
                        'password': snapshot['password'],
                        'first_name': snapshot.get('first_name', ''),
                        'last_name': snapshot.get('last_name', ''),
                        'email': snapshot.get('email', ''),
                        'is_staff': bool(snapshot.get('is_staff')),
                        'is_superuser': bool(snapshot.get('is_superuser')),
                        'is_active': bool(snapshot.get('is_active', True)),
                    }

                    User.objects.update_or_create(
                        id=user_id,
                        defaults=user_data,
                    )
                except (DatabaseError, KeyError, TypeError, ValueError):
                    pass

        return self.get_response(request)
