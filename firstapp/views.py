from django.shortcuts import render
from django.http import HttpResponse
from firstapp.helper import fetch_user_util, save_todb_users, get_fromdb_users
from firstapp.helper import client_id, redirect_uri, get_token


def UserLogin(request):
    if request.method == 'GET':
        url = "https://login.salesforce.com/services/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
        return render(request, 'loginform.html', {'url': url})


def redirected(request):
    if request.method == 'GET':
        try:
            params = request.GET
            auth_code = params.get('code')
            temp = get_token(auth_code)
            print(auth_code)
            print(temp)
            request.session['token'] = temp['token']
            request.session['instance_url'] = temp['instance_url']
        except KeyError as e:
            url = "https://login.salesforce.com/services/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
            return render(request, 'loginform.html', {'url': url})
        # print("token is {} ".format(request.session['token']))
        # print("instance_url is {}".format(request.session['instance_url']))
        context = {
            'msg': ''
        }
        return render(request, 'redirectform.html', context)

    elif request.method == 'POST':
        if 'users' in request.POST:
            return list_users(request)
        elif 'accounts' in request.POST:
            pass
        elif 'contacts' in request.POST:
            pass


def fetch_users(request):
    return render(request, "users.html", {})


def list_users(request):
    if request.method == 'POST':
        try:
            token = request.session['token']
            instance_url = request.session['instance_url']
        except KeyError as e:
            url = "http://login.salesforce.com/services/oauth2/authorize?client id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
            return render(request, "loginform.html", {'url': url})

        temp_variable = fetch_user_util(token, instance_url)
        if temp_variable['success']:
            user_data = temp_variable['data']
            save_todb_users(user_data)
            context = {
                "msg": temp_variable['msg'],
            }
        else:
            if temp_variable['code'] == '401':
                url = "https://login.salesforce.com/services/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
                return render(request, 'loginform.html', {'url': url})
            else:
                # print("Error")
                context = {
                    "msg": temp_variable['msg'],
                }
        return render(request, "redirectform.html", context)

    elif request.method == 'GET':

        context = {
            'data': get_fromdb_users()
        }
        return render(request, 'fetchusers.html', context)
