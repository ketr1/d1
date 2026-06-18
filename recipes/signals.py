import os

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import ShoppingList

@receiver(user_logged_in)
def transfer_shopping_list(sender, request, user, **kwargs):
    if os.environ.get('VERCEL') == '1':
        request.session['auth_user_snapshot'] = {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
        }

    session_key = request.session.session_key
    if session_key:
        session_items = ShoppingList.objects.filter(session_key=session_key)
        for item in session_items:
            ShoppingList.objects.create(
                user=user,
                ingredient=item.ingredient,
                quantity_grams=item.quantity_grams,
                checked=item.checked
            )
            item.delete()
