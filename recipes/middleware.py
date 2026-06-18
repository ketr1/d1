    import os

from django.contrib.auth.models import User


class RestoreMissingUserMiddleware:
    """
    Костыль для Vercel + SQLite:
    если пользователь есть в cookie-сессии, но исчез из временной SQLite-базы,
    создаём его заново с тем же id до AuthenticationMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.environ.get('VERCEL') == '1':
            user_id = request.session.get('_auth_user_id')

            if user_id:
                try:
                    user_id = int(user_id)

                    if not User.objects.filter(id=user_id).exists():
                        User.objects.create(
                            id=user_id,
                            username=f'restored_user_{user_id}',
                            is_staff=True,
                            is_superuser=True,
                            is_active=True,
                        )
                except Exception:
                    pass

        return self.get_response(request)