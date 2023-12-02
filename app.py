import joblib
import datetime
from datetime import time
import numpy as np
import streamlit as st
from PIL import Image
from db import ConnectDB
import pandas as pd
from sklearn.preprocessing import StandardScaler

model = joblib.load('credit_fraud.pkl')

image = Image.open('bank.png')
new_image = image.resize((200, 200))
with st.columns(3)[1]:
    st.image(new_image, caption='Credit Fraud')


# Create Streamlit app
st.title("Credit Card Fraud Detection Model")
st.write('visit the dataset used: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud')


def is_numeric(value):
    """check if the value is numeric or not"""
    try:
        _ = float(value)
        return True
    except ValueError:
        return False


# scale using MinMaxScaler
def scale_values(values):
    ''' function to scale the values'''
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform([values])
    return scaled_values.flatten()

usr = None

# create the tables
ConnectDB.create_user_table()
ConnectDB.create_prediction_table()


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
            usr = username
            menu = None
            if usr == 'admin':
                menu = ['Prediction', 'Users', 'Predicted']
            else:
                menu = ['Prediction',  'Predicted']
            side_checker = st.sidebar.selectbox("Task", menu)
            # st.sidebar.selectbox        

            if side_checker == "Prediction":

                # User Information
                st.header("User Information")
                user_xname = st.text_input("Full Name")
                card_xnumber = st.text_input("Card Number")
                expiration_xdate = st.date_input("Expiration Date", min_value=datetime.date.today())
                cvvx = st.text_input("CVV")
                amount = st.text_input("enter amount")
                selected_time = st.time_input("Select a time", time(12, 0))

                # Submit Button
                # if st.button("Submit Transaction"):

                #     card_res = ConnectDB.check_user_card(
                #         fullname=user_xname,
                #         card_number=card_xnumber,
                #         expiration_date=expiration_xdate,
                #         cvv=cvvx
                #     )

                    # if card_res:
                        # Transaction Information
                st.header("Transaction Information")
                st.write("Enter features from V1-V28, seperated by commas, to check if the \
            transaction is legitimate or fraudulent:")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    v4 = st.text_input("enter v4")
                with col2:
                    v7 = st.text_input("enter v7")
                with col3:
                    v9 = st.text_input("enter v9")
                with col4:
                    v12 = st.text_input("enter v12")
                with col5:
                    v18 = st.text_input("enter v18")
                # row two
                with col1:
                    v19 = st.text_input("enter v19")
                with col2:
                    v20 = st.text_input("enter v20")
                with col3:
                    v21 = st.text_input("enter v21")
                with col4:
                    v22 = st.text_input("enter v22")
                with col5:
                    v28 = st.text_input("enter v28")

                # Create input fields for the user to enter feature values
                # input_df = st.text_input('V1,..V28 features')
                input_df_lst = [
                    v4, v7, v9, v12, v18, v19, v20, v21, v22, v28,
                ]

                # Validation check
                if all(is_numeric(value) for value in input_df_lst):
                    submit_button = st.button("Submit")
                    if submit_button:
                        card_res = ConnectDB.check_user_card(
                            fullname=user_xname,
                            card_number=card_xnumber,
                            expiration_date=expiration_xdate,
                            cvv=cvvx
                        )

                        if not card_res:
                            st.error("provide a valid credit or debit card details")
                        else:
                            # Get input feature values
                            features = np.array(input_df_lst, dtype=np.float64)
                           
                            # Make prediction
                            prediction = model.predict(features.reshape(1, -1))
                            # prediction = model.predict(scaled_input)

                            # Display the result
                            status = None
                            if prediction[0] == 0:
                                status = "Legitimate"
                                st.write(f"The transaction details \
                                        captured is {status}")
                                ConnectDB.create_prediction(
                                    username=username,
                                    transaction_time=str(selected_time),
                                    amount=amount,
                                    card_expiration_date=expiration_xdate,
                                    card_number=card_xnumber,
                                    v4=v4, v7=v7,
                                    v9=v9, v12=v12,
                                    v18=v18, v19=v19,
                                    v20=v20, v21=v21,
                                    v22=v22, v28=v28,
                                    status=status
                                )
                            else:
                                status = "Fraudulent"
                                st.write(f"the transaction detail given is a \
                                        ${status} transaction")
                                ConnectDB.create_prediction(
                                    username=username,
                                    transaction_time=str(selected_time),
                                    amount=amount,
                                    v4=v4, v7=v7,
                                    card_expiration_date=expiration_xdate,
                                    card_number=card_xnumber,
                                    v9=v9, v12=v12,
                                    v18=v18, v19=v19,
                                    v20=v20, v21=v21,
                                    v22=v22, v28=v28,
                                    status=status
                                )
                    
                else:
                    st.warning("Please enter valid numeric values \
                                for all transactions.")
                    # else:
                    #     st.error("invalid card credentials")
            # display users
            if side_checker == "Users":

                st.title('User Data Display')
                # Fetch data from SQLite database
                data = ConnectDB().get_user()
                # Convert the fetched data to a Pandas DataFrame
                df = pd.DataFrame(data, columns=['username', 'fullname', 'card_number', 'expiration_date'])
                # Display the DataFrame using Streamlit
                st.dataframe(df.dropna(), height=800, width=2000)
               
            
            if side_checker == "Predicted":
                st.title('Predicted Data Display')
                # Fetch data from SQLite database
                data_x = ConnectDB().get_predictions()
                # Convert the fetched data to a Pandas DataFrame

                df = pd.DataFrame(data_x, columns=['id', 'username', 'transaction_time', 'amount', 'card_expiration_date', 'card_number', 'v4', 'v7', 'v9', 'v12', 'v18', 'v19', 'v20', 'v21', 'v22', 'v28', 'status'])
                print(df)
                # Filter the DataFrame based on the selected username
                if usr != 'admin':
                    filtered_df = df.loc[df['username'] == usr]
                else:
                    filtered_df = df.copy()
                # Display the cleaned DataFrame using Streamlit
                st.dataframe(filtered_df, height=800, width=1200)
                # st.dataframe(df, height=800, width=1800)
        
        else:
            st.sidebar.error("wrong credentials")

elif side_choice == "SignUp":
    st.subheader("SignUp")

    username_reg = st.text_input("Username")
    password_reg = st.text_input("Password", type="password")
    fullxx_name = st.text_input("Full Name", "")
    card_num_reg = st.text_input("Card Number", "")
    expiration_date_reg = st.date_input("Expiration Date", min_value=datetime.date.today())
    cvv_reg = st.text_input("CVV", "")

    if st.button("SignUp"):
        ConnectDB.create_user_table()
        ConnectDB.create_user(
            username=username_reg,
            password=password_reg,
            fullname=fullxx_name,
            card_number=card_num_reg,
            expiration_date=expiration_date_reg,
            cvv=cvv_reg
        )
        st.success("Account created")
        st.info("Goto Login")
