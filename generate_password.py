import streamlit_authenticator as stauth

password = input("enter your password: ")

hashed_passwords = stauth.Hasher([password]).generate()

print(hashed_passwords)