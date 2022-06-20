from bs4 import BeautifulSoup
import requests


def updateCookie(session, responce):
    
    if 'Set-Cookie' not in responce.headers:
        return
    
    recvCookie = responce.headers['Set-Cookie'].replace(' ', '').replace(',', ';').split(';')
    
    cokies = []
    if 'cookie' in session.headers:
        cokies = session.headers['cookie'].replace(' ', '').split(';')
    
    requiredCookie = [
        '_device_id',
        '_octo',
        'logged_in',
        '_gh_sess',
        'tz',
        'has_recent_activity',
        'user_session',
        '__Host-user_session_same_site',
        'dotcom_user',
    ]
    
    for cookie in recvCookie:
        name = cookie.split('=')[0]
        if name in requiredCookie:
            # if cookie is in cokies, delete it
            for c in cokies:
                if c.split('=')[0] == name:
                    cokies.remove(c)
                    break
            cokies.append(cookie)
            



def login(session, userName, password):
    
    # not a robot header
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
    }

    try:
        # get login page
        loginUrl = 'https://github.com/login'
        loginPage = session.get(loginUrl)
        updateCookie(session, loginPage)
        
        # get authenticity token 
        soup = BeautifulSoup(loginPage.text, 'html5lib')
        authToken = soup.find('input', attrs={'name': 'authenticity_token'})['value']
        
        authData = {
            'commit': 'Sign in',
            'authenticity_token': authToken,
            # 'webauthn-support': 'supported',
            # 'webauthn-iuvpaa-support': 'supported',
        }
        
        
        # get other form-control names and values
        formControl = soup.find_all('input', {'class': 'form-control'})
        
        for control in formControl:
            name = control['name']
            value = ''
            # if control contains attribute 'value', set value to it
            if name == 'login':
                value = userName
            elif name == 'password':
                value = password
            elif 'value' in control.attrs:
                value = control['value']
            authData[name] = value
        
        
        authUrl = 'https://github.com/session'
        authResponce = session.post(authUrl, data=authData)
        updateCookie(session, authResponce)
        
        
        # if responce still cntains 'Sign in', login failed
        if authResponce.text.lower().find('sign in') != -1:
            return False
        else:
            return True
        
    except Exception as e:
        print(e)
        return False

