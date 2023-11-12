import joblib
import numpy as np
import streamlit as st
from PIL import Image
from db import ConnectDB
import pandas as pd

model = joblib.load('credit_fraud.pkl')

image = Image.open('bank.png')
new_image = image.resize((200, 200))
with st.columns(3)[1]:
    st.image(new_image, caption='Credit Fraud')


# Create Streamlit app
st.title("Credit Card Fraud Detection Model")
st.write('visit the dataset used: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud')


# side bar menu creations
menu = ['Home', 'Login', 'SignUp']
side_choice = st.sidebar.selectbox("Menu", menu)
# Variable to track login status
is_logged_in = False
if side_choice == "Home":
    st.subheader("Home")

elif side_choice == "Login":
    st.sidebar.subheader("Login")
    # form fields defintion
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.checkbox("Login"):
        result = ConnectDB.login_user(
            username=username,
            password=password
        )

        if result:
            st.sidebar.success(f"Logged-In as {username}")
            is_logged_in = True
            menu = ['Prediction', 'Users']
            side_choice = st.sidebar.selectbox("Task", menu)         

            if st.sidebar.checkbox("Prediction"):

                st.write("Enter features from V1-V28, seperated by commas, to check if the \
            transaction is legitimate or fraudulent:")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    v1 = st.text_input("enter v1")
                with col2:
                    v2 = st.text_input("enter v2")
                with col3:
                    v3 = st.text_input("enter v3")
                with col4:
                    v4 = st.text_input("enter v4")
                with col5:
                    v5 = st.text_input("enter v5")
                # row two
                with col1:
                    v6 = st.text_input("enter v6")
                with col2:
                    v7 = st.text_input("enter v7")
                with col3:
                    v8 = st.text_input("enter v8")
                with col4:
                    v9 = st.text_input("enter v9")
                with col5:
                    v10 = st.text_input("enter v10")
                # row three
                with col1:
                    v11 = st.text_input("enter v11")
                with col2:
                    v12 = st.text_input("enter v12")
                with col3:
                    v13 = st.text_input("enter v13")
                with col4:
                    v14 = st.text_input("enter v14")
                with col5:
                    v15 = st.text_input("enter v15")

                # row four
                with col1:
                    v16 = st.text_input("enter v16")
                with col2:
                    v17 = st.text_input("enter v17")
                with col3:
                    v18 = st.text_input("enter v18")
                with col4:
                    v19 = st.text_input("enter v19")
                with col5:
                    v20 = st.text_input("enter v20")

                # row five
                with col1:
                    v21 = st.text_input("enter v21")
                with col2:
                    v22 = st.text_input("enter v22")
                with col3:
                    v23 = st.text_input("enter v23")
                with col4:
                    v24 = st.text_input("enter v24")
                with col5:
                    v25 = st.text_input("enter v25")

                # row six
                with col1:
                    v26 = st.text_input("enter v26")
                with col2:
                    v27 = st.text_input("enter v27")
                with col3:
                    v28 = st.text_input("enter v28")

                # Create input fields for the user to enter feature values
                # input_df = st.text_input('V1,..V28 features')
                input_df_lst = [
                    v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,
                    v11, v12, v13, v14, v15, v16, v17, v18, v19, v20,
                    v21, v22, v23, v24, v25, v26, v27, v28
                ]

                # Create a button to submit input and get a prediction
                submit = st.button("Submit")

                if submit:
                    # Get input feature values
                    features = np.array(input_df_lst, dtype=np.float64)

                    # Make prediction
                    prediction = model.predict(features.reshape(1, -1))

                    # Display the result
                    if prediction[0] == 0:
                        st.write("Legitimate transaction")
                    else:
                        st.write("Fraudulent transaction")

            # display users
            if st.sidebar.checkbox("Users"):

                st.title('User Data Display')
                # Fetch data from SQLite database
                data = ConnectDB().get_user()
                # Convert the fetched data to a Pandas DataFrame
                df = pd.DataFrame(data, columns=['username'])

                # Display the DataFrame using Streamlit
                st.dataframe(df, height=800, width=1200)
        else:
            st.sidebar.error("wrong credentials")

elif side_choice == "SignUp":
    st.subheader("SignUp")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("SignUp"):
        ConnectDB.create_user_table()
        ConnectDB.create_user(
            username=username,
            password=password
        )
        st.success("Account created")
        st.info("Goto Login")
