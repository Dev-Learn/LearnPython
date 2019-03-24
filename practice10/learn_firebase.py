import pyrebase

config = {
    "apiKey": "AIzaSyBEWe5NAhhwqOVge-kMvQjBUhWnm4U4Yk8",
    "authDomain": "learnpython-88c3f.firebaseapp.com",
    "databaseURL": "https://learnpython-88c3f.firebaseio.com",
    "projectId": "learnpython-88c3f",
    "storageBucket": "learnpython-88c3f.appspot.com",
    "messagingSenderId": "132293237205"
}

firebase = pyrebase.initialize_app(config=config)

auth = firebase.auth()

storage = firebase.storage()

# if __name__ == '__main__':
# auth.send_password_reset_email("namtran09061992@gmail.com")
# email = input("Please input email")
# password = input("Please input password")

# user = auth.create_user_with_email_and_password(email,password)
#
#     user = auth.sign_in_with_email_and_password(email,password)
#
# if user['idToken']:
# print(auth.get_account_info(user['idToken']))
# auth.send_email_verification(user['idToken'])
