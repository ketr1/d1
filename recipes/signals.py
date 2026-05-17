from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import ShoppingList

@receiver(user_logged_in)
def transfer_shopping_list(sender, request, user, **kwargs):
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