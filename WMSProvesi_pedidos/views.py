from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from urllib.parse import urlencode

@login_required
def me(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
    })

def logout(request):
    """Cierra la sesión en Django y en Auth0, y luego redirige de vuelta al backend."""
    django_logout(request)

    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = settings.LOGOUT_REDIRECT_URL 

    params = urlencode({
        'returnTo': return_to,
        'client_id': client_id,
    })

    return redirect(f'https://{domain}/v2/logout?{params}')
