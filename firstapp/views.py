from django.shortcuts import render
from django.http import HttpResponse
from firstapp.helper import fetch_user_util, save_todb_users, get_fromdb_users
from firstapp.helper import client_id, redirect_uri, get_token


def UserLogin(request):  # accessing authorization server
    if request.method == 'GET':
        url = "https://login.salesforce.com/services/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
        return render(request, 'loginform.html', {'url': url})


def redirected(request):
    if request.method == 'GET':
        print("count")
        try:
            params = request.GET
            auth_code = params.get('code')
            if auth_code is not None:
                temp = get_token(code=auth_code)
                print(temp)
                request.session['token'] = temp['token']
                request.session['instance_url'] = temp['instance_url']
                request.session['refresh_token'] = temp['refresh_token']
            elif 'refresh_token' not in request.session:
                url = "https://login.salesforce.com/services/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code"
                return render(request, 'loginform.html', {'url': url})
        except Exception as e:
            print(e)
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
        # elif 'accounts' in request.POST:
        #     pass
        # elif 'contacts' in request.POST:
        #     pass


def fetch_users(request):
    return render(request, "users.html", {})


def list_users(request):
    if request.method == 'POST':
        refresh_token = request.session['refresh_token']
        try:
            token = request.session['token']
            instance_url = request.session['instance_url']
            # refresh_token = request.session['referesh_token']
        except KeyError as e:
            handle_refresh_token(request, refresh_token)
            return render(request, 'redirectform.html', {'msg': 'logged in again'})

        temp_variable = fetch_user_util(token, instance_url)
        if temp_variable['success']:
            user_data = temp_variable['data']
            save_todb_users(user_data)
            context = {
                "msg": temp_variable['msg'],
            }
        else:
            if temp_variable['code'] == '401':
                handle_refresh_token(request, refresh_token)
                return render(request, 'redirectform.html', {'msg': 'logged in again'})
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


def handle_refresh_token(request, refresh_token):
    temp = get_token(code=None, refresh_token=refresh_token)
    request.session['token'] = temp['token']
    request.session['instance_url'] = temp['instance_url']
