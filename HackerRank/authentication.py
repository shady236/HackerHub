import json
from bs4 import BeautifulSoup
import requests


def getCsrfToken(page):
    soup = BeautifulSoup(page.content, 'html5lib')
    csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
    return csrf_token


def login(session, userName, password):
    
    # not a robot header
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
    }

    try:
        # get login page
        loginUrl = 'https://www.hackerrank.com/auth/login'
        page = session.get(loginUrl)

        # add csrf token to header
        session.headers['x-csrf-token'] = getCsrfToken(page)

        # post authentication data (user, pass, ...)
        authUrl = 'https://www.hackerrank.com/rest/auth/login'
        authData = {
            'login': userName,
            'password': password,
            'remember_me': False,
            'fallback': True
        }
        authResponce = session.post(authUrl, data=authData)
        
        status = json.loads(authResponce.text)['status']
        if status == False:
            return False
        
        # get redirected page
        authRedirectUrl = 'https://www.hackerrank.com/rest/auth/get_redirect_url/master'
        page = session.get(authRedirectUrl)
        session.headers['x-csrf-token'] = getCsrfToken(page)	# update csrf token
        return True
    except Exception as e:
       return False

