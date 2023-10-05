import joblib
import numpy as np
import streamlit as st
from PIL import Image

model = joblib.load('credit_fraud.pkl')

image = Image.open('bank.png')
new_image = image.resize((200, 200))
with st.columns(3)[1]:
    st.image(new_image, caption='Credit Fraud')
# Create Streamlit app
st.title("Credit Card Fraud Detection Model")
st.write('visit the dataset used: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud')
st.write("Enter features from V1-V28, seperated by commas, to check if the \
          transaction is legitimate or fraudulent:")

# Create input fields for the user to enter feature values
input_df = st.text_input('V1,..V28 features')
input_df_lst = input_df.split(',')

# Create a button to submit input and get a prediction
submit = st.button("Submit")

if submit:
    # Check if the input has exactly 29 features
    if len(input_df_lst) == 28:
        # Get input feature values
        features = np.array(input_df_lst, dtype=np.float64)
        # Make prediction
        prediction = model.predict(features.reshape(1, -1))
        # Display the result
        if prediction[0] == 0:
            st.write("Legitimate transaction")
        else:
            st.write("Fraudulent transaction")
    else:
        st.write("Please enter exactly the 28 feature for the credit card \
                 fraud dataset. V1, V2, … V28 ")
