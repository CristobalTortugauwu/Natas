## Natas 11 walkthrough

First, after we put the correct credentials, the first thing we see here is this image:
![alt text](frontend.png)

There are two things that are very useful in this frontend page, the first one is that they are telling us that they page is using XOR encryption for the cookies, and the second one, is that we can take a look at the sourcecode. 
So we are going to take a look at the cookies, and we find that there is one named data, and has the following value. 
![alt text](cookies.png)

and then we take a look at the source code
![alt text](code1.png)
![alt text](code2.png)

we see that there is a variable called *defaultdata*, this variable contains two values, the most important one is *showpassword*, then we have a xor_encrypt function, and we can that the $key is censored, so from this we can infere that we have to guess the key, is some way, we will see how later on!
And then we have another two function called *loadData* and *saveData*. 

From the logic of this code, we can see that the page first loads the data from the cookies, applies the encryption, and then it saves the encrypted message in the cookies. And then, in the html page, we can see that is the cookies has a *yes* value in the variable *showpassword*, then the page will show the password to next level of natas, and that is the one password that we are looking for after all. 

So mainly what we have to do one is: Guess the key, and then change the value of the array to yes.

### Guessing the key

### Changing the value