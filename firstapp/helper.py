import requests
from django.http import HttpResponse
from firstapp.models import UserData

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
        # print(d['token'])
        d['instance_url'] = r.json()["instance_url"]
        # print(d['instance_url'])
    elif r.status_code == 400:
        print("Invalid auth code")
        d = dict()
    else:
        d = dict()
    return d


def fetch_user_util(token, instance_url):
    print('fetch_user_util..')
    header = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get(
        instance_url + "/services/data/v52.0/query/?q=SELECT+email+,+name+,+employeenumber+,+department+,+companyname+,+city+from+User",
        headers=header)
    if str(r.status_code) == '401':
        return {'success': False, 'code': '401', 'msg': 'Invalid Session Id'}
    elif str(r.status_code) == '200':
        return {'success': True, 'code': '200', 'msg': 'Request completed', 'data': r.json()['records']}
    return {'success': False, 'code': r.status_code, 'msg': 'Request Could Not Complete'}


def save_todb_users(temp_variable):
    for var in temp_variable:
        obj = UserData(Email=var['Email'], Name=var['Name'], EmployeeNumber=var['EmployeeNumber'],
                       Department=['Department'], City=var['Department'])
        obj.save()


def get_fromdb_users():
    return UserData.objects.all()

