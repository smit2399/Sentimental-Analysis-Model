import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import pickle
import hashlib



def make_hashes(password):   #hashlib for encryption
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# Trends Tab

def Trending():
	df_td = pickle.load(open('Trending.sav','rb'))
	return df_td.reset_index(drop=True)

# Influencers Tab

def Influencers():
    df_ss = pickle.load(open('Influencer.sav', 'rb'))
    return df_ss.reset_index(drop=True)


#Text Handling

def Return_value(Text_input):
        loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
        final_result = loaded_model.predict(Text_input)[0]
        return final_result

def Text_handling(User_input):
        vect = pickle.load(open('vac.sav', 'rb'))
        Text_input = vect.transform([User_input])
        return Return_value(Text_input)


import sqlite3     # DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Social Media Analytics"""

	st.title("Social Media Analytics")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home") #Home
		image = Image.open('social_media.jpg')
		st.image(image)


	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))
				task = st.selectbox("Task",["Sentiment Analysis","Top Influencers","Dashboard","Trends"])
				if task == "Sentiment Analysis":
					st.subheader("Type your sentence")
					user_input = st.text_input("User Input")
					if st.button("Click!"):
                                            final_result = Text_handling(user_input)
                                            if final_result == 'Positive':
                                                st.markdown(''' :green[Positive] ''')
                                            elif final_result == 'Negative':
                                                st.markdown(''' :red[Negative] ''')
                                            elif final_result == 'Neutral':
                                                st.markdown(''' :orange[Neutral] ''')
				elif task == "Top Influencers":
					st.subheader("Top Influencers")
					user_result = Influencers()
					#clean_db = pd.DataFrame(user_result,columns=["Username","followers"])
					st.dataframe(user_result, use_container_width=True)
						

				elif task == "Dashboard":
					st.subheader("Vaccine Dataset Analysis")
					image = Image.open('Dashboard.png')
					st.image(image)
					
				elif task == "Trends":
					st.subheader("Trending right now!")
					user_trends = Trending()
					#clean_db = pd.DataFrame(user_result,columns=["Username","followers"])
					st.dataframe(user_trends, use_container_width=True)

			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
