from django.shortcuts import render
from django.http import HttpResponse
from firstapp.helper import fetch_user_util
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from firstapp.helper import client_id, redirect_uri, get_token


def UserLogin(request):
    if request.method == 'GET':
        url = "https://login.salesforce.com/services/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
        return render(request, 'loginform.html', {'url': url})


def redirected(request):
    params = request.GET
    auth_code = params.get('code')
    temp = get_token(auth_code)
    request.session['token'] = temp['token']
    request.session['instance_url'] = temp['instance_url']
    # print("token is {} ".format(request.session['token']))
    # print("instance_url is {}".format(request.session['instance_url']))
    return HttpResponse("Congratulations...")


def fetch_users(request):
    return render(request, "users.html", {})


# @login_required(login_url='/login/')
def list_users(request):
    print("User Is Logged In")
    token = request.session.get('token', default='Guest')
    instance_url = request.session['instance_url']
    temp_variable = fetch_user_util(token, instance_url)
    context = {
        'msg': temp_variable['msg']
    }
    return render(request, "fetchusers.html", context)

