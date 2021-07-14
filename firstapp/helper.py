import requests
from django.http import HttpResponse

client_id = '3MVG9fe4g9fhX0E6eAkSTAIn6bHBDUBPVS51MnSHeEjZq58NEPaOM37jXoEWVtM10l7gMKoLjHDuPLZhTt9fi'
client_secret = '21D77A2819CA4DCDA21E90C6E1C6FDE11806895AC5959FE7371A344B426E273F'
redirect_uri = 'http://localhost:8000/user/'


def get_token(code):
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': "authorization_code",
        'code': code
    }
    r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
    if r.status_code == 200:
        d = dict()
        d['token'] = r.json()["access_token"]
        print(d['token'])
        d['instance_url'] = r.json()["instance_url"]
        print(d['instance_url'])
    elif r.status_code == 404:
        return HttpResponse("Page Not Found")
    else:
        return HttpResponse("")
    return d


def fetch_user_util(token, instance_url):
    print('fetch_user_util..')
    header = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get(instance_url + "/services/scim/v2/Users", headers=header)
    if str(r.status_code) == '401':
        return {'success': False, 'msg': 'Invalid Session Id'}
    elif str(r.status_code) == '200':
        print(r.json())
        return {'success': True, 'msg': r.json()}
    return {'success': False, 'msg': 'Request Could Not Complete'}
