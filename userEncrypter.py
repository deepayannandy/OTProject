import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Deepayan Nandy", "Root"]
usernames = ["dny", "root"]
passwords = ["lipi@6622", "66226622"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)