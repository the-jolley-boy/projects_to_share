from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate, login
from decouple import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

# Create your views here.

auth_url_discord = f"https://discord.com/api/oauth2/authorize?client_id=1092643533221003286&redirect_uri={settings.REDIRECT_URI}&response_type=code&scope=identify%20guilds"

def notify(request):
    return render(request, 'notify.html')

@login_required(login_url="/notify/login")
def staff_data(request):
    if 'intended_page' in request.session:
        intended_page = request.session.pop('intended_page')
        return redirect(intended_page)
    return render(request, 'staff_data.html')

def betting(request):
    return render(request, 'betting.html')

def release_channel_generator(request):
    return render(request, 'release_channel_generator.html')

@login_required(login_url="/notify/login")
def weekly_calendar(request):
    if 'intended_page' in request.session:
        intended_page = request.session.pop('intended_page')
        return redirect(intended_page)
    return render(request, 'weekly_calendar.html')

@login_required(login_url="/notify/login")
def monthly_calendar(request):
    if 'intended_page' in request.session:
        intended_page = request.session.pop('intended_page')
        return redirect(intended_page)
    return render(request, 'monthly_calendar.html')

@login_required(login_url="/notify/login")
def release_intro(request):
    if 'intended_page' in request.session:
        intended_page = request.session.pop('intended_page')
        return redirect(intended_page)
    return render(request, 'release_intro.html')

@login_required(login_url="/notify/login")
def staff_data_2(request):
    return render(request, 'staff_data.html')

def discord_login(request: HttpRequest):

    # Check if the user is already authenticated
    if request.user.is_authenticated:
        intended_page = request.GET.get('intended_page', '/')
        return redirect(intended_page)

    intended_page = request.GET.get('intended_page')
    if intended_page:
        request.session['intended_page'] = intended_page

    return redirect(auth_url_discord)

def discord_login_redirect(request: HttpRequest):
    # For making sure guilds/roles match what is needed
    required_guild_id = "570142274902818816"
    required_role_id = "570142915326771218"

    code = request.GET.get('code')

    access_token = exchange_code(code)
    user = get_user(access_token)
    user_id = user['id']
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user, backend='discordlogin.auth.DiscordAuthenticationBackend')

    # Get user's guilds
    user_guilds = get_user_guilds(access_token)
    user_roles = get_user_roles(access_token, required_guild_id, user_id)  # Pass in required_guild_id and user ID

    if any(guild['id'] == required_guild_id for guild in user_guilds):
        if required_role_id in user_roles['roles']:
            intended_page = request.session.pop('intended_page')  # Retrieve the intended_page from the session
            return redirect(intended_page)

    # Clear the session if the user doesn't have permission
    logout(request)
    request.session.clear()

    return HttpResponseForbidden("You don't have permission to access this page.")

def get_user_guilds(access_token):
    guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers={
        'Authorization': f'Bearer {access_token}',
    })
    if guilds_response.status_code == 200:
        return guilds_response.json()
    else:
        return []

def get_user_roles(access_token, guild_id, user_id):
    roles_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}', headers={
        'Authorization': f'Bot {config("BOT_TOKEN")}',
        # 'Authorization': f'Bearer {access_token}',
    })
    if roles_response.status_code == 200:
        return roles_response.json()
    else:
        return []

def get_user(access_token):
    response = requests.get("https://discord.com/api/v9/users/@me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user

def exchange_code(code: str):
    print(settings.REDIRECT_URI)
    data = {
        "client_id": config('CLIENT_ID'),
        "client_secret": config('CLIENT_SECRET'),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.REDIRECT_URI,
        "scope": "identify guilds"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    
    return access_token