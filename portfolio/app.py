import getpass

def app_signin():
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    
    print(username, password)

def app_signup():
    pass

def app_show_options():
    pass

def run():
    print("Welcome!")

    while True:
        a = input('Enter l to login, s to sign up or e to exit.\nEnter command: ')
        if a == 'l':
            app_signin()

        if a == 's':
            app_signup()

        if a == 'e':
            print('bye')
            break
        else:
            break

if __name__ == '__main__':
   run()



