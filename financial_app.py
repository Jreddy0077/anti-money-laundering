from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import streamlit as st
import time
import base64
from sqlalchemy import create_engine,text
import pymysql
from sqlalchemy.exc import SQLAlchemyError
import re



import os
model_path = os.path.join(os.path.dirname(__file__), "aml.pkl")
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error(f"Model file {model_path} not found.")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
####################################################################################


df=None
def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()




st.set_page_config(layout="wide")

# Custom CSS to remove padding and margins

# these are the internal dinamic classes genrating during running and we are making them padding 0
# style for inserting the css script
# unsafe_allow_html=True to insert the html and css into the streamlit
# markdown is to exicute the css and html into the streamlit

custom_css = """
    <style>
    .css-1d391kg, .css-1v3fvcr, .css-18e3th9 {
        padding: 0 !important;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)



# Navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=["Home", "Prediction Analytics"],  # required
        icons=["house", "bar-chart"],  # optional
         menu_icon="box-arrow-in-right",
        default_index=0,  # optional
    )

# Pages based on selected option
if selected == "Home":
        bg_image_path = r"bg_home1.jpg.png"
        bg_image_base64 = get_base64_of_bin_file(bg_image_path)
        st.markdown(f"""
        <style>
        .stApp {{

            background-image: url("data:image/jpg;base64,{bg_image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)
        dic={}

        #st.title("**anti money laundering**")
        st.markdown('<h2 style="color:yellow;">There You Can Check The Trasaction</h2>', unsafe_allow_html=True)


        st.markdown('<h4 style="color:orange;">Select Prediction Method</h4>', unsafe_allow_html=True)

        prediction_method = st.radio('', ('Predict Record-wise', 'Predict for Entire DataFrame'))
        if prediction_method=='Predict Record-wise':
            from datetime import datetime

            c1, c2, c3 = st.columns([1, 1, 1.5])
            
            with c1:
                st.markdown('<p style="color:red;">Timestamp</p>', unsafe_allow_html=True)
                timestamp = st.text_input("Enter Timestamp (YYYY-MM-DD HH:MM:SS)", key='timestamp')
            
                st.markdown('<p style="color:red;">From Bank</p>', unsafe_allow_html=True)
                from_bank = st.text_input("From Bank", key='from_bank')
            
                st.markdown('<p style="color:red;">From Account</p>', unsafe_allow_html=True)
                from_account = st.text_input("From Account", key='from_account')
            
            with c2:
                st.markdown('<p style="color:red;">To Bank</p>', unsafe_allow_html=True)
                to_bank = st.text_input("To Bank", key='to_bank')
            
                st.markdown('<p style="color:red;">To Account</p>', unsafe_allow_html=True)
                to_account = st.text_input("To Account", key='to_account')
            
                st.markdown('<p style="color:red;">Amount Received</p>', unsafe_allow_html=True)
                amount_received = st.number_input("Amount Received", key='amount_received')
            
            with c3:
                st.markdown('<p style="color:red;">Receiving Currency</p>', unsafe_allow_html=True)
                receiving_currency = st.selectbox("Receiving Currency",['US Dollar', 'Bitcoin', 'Euro', 'Australian Dollar', 'Yuan','Rupee', 'Mexican Peso', 'Yen', 'UK Pound', 'Ruble','Canadian Dollar', 'Swiss Franc', 'Brazil Real', 'Saudi Riyal', 'Shekel'], key='receiving_currency')
            
                st.markdown('<p style="color:red;">Amount Paid</p>', unsafe_allow_html=True)
                amount_paid = st.number_input("Amount Paid", key='amount_paid')
            
                st.markdown('<p style="color:red;">Payment Currency</p>', unsafe_allow_html=True)
                payment_currency = st.selectbox("Payment Currency", ['US Dollar', 'Bitcoin', 'Euro', 'Australian Dollar', 'Yuan','Rupee', 'Yen', 'Mexican Peso', 'UK Pound', 'Ruble', 'Canadian Dollar', 'Swiss Franc', 'Brazil Real', 'Saudi Riyal','Shekel'], key='payment_currency')
            
                st.markdown('<p style="color:red;">Payment Format</p>', unsafe_allow_html=True)
                payment_format = st.selectbox("Payment Format", ['Reinvestment', 'Cheque', 'Credit Card', 'ACH', 'Cash', 'Wire','Bitcoin'], key='payment_format')
            
            # Extracting time-related features from the timestamp
            try:
                if timestamp:
                    # Parse the timestamp
                    dt = datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S")
                    day = dt.day
                    hour = dt.hour
                    minute = dt.minute
                    day_of_week = dt.strftime('%A')  # Extract the day name, e.g., Monday
                    day_type = "Weekend" if day_of_week in ["Saturday", "Sunday"] else "Weekday"
                    
                    # Display parsed results
                    st.write("**Day:**", day)
                    st.write("**Hour:**", hour)
                    st.write("**Minute:**", minute)
                    st.write("**Day Type:**", day_type)
                    st.write("**Day of Week:**", day_of_week)
                    
                else:
                    st.error("Please enter a valid timestamp.")
                    
            except ValueError:
                st.error("Incorrect timestamp format. Please use YYYY-MM-DD HH:MM:SS.")
            
            # Creating the DataFrame
            data = [[timestamp, from_bank, from_account, to_bank, to_account, amount_received, 
                     receiving_currency, amount_paid, payment_currency, payment_format, 
                     day, hour, minute, day_type, day_of_week]]
            
            columns = ["time stamp", "from bank", "account", "to bank", "account.1", "amount received", 
                       "receiving currency", "amount paid", "payment currency", "payment format", 
                       "day", "hour", "min", "day_type", "day_of_week"]
            
            df = pd.DataFrame(data, columns=columns)
            
            # Display the DataFrame
            st.write("Data for Prediction:")
            st.write(df)
            

######################################################

            
            
                
            if st.button("Predict"):
                with st.spinner("Please wait while predicting...."):
                    time.sleep(0.5)
                
                    try:
                        result = model.predict(df2)
                        if result[0] == 0:
                            st.write("**Congratulations! The customer is likely to continue their subscription.** 🎉😊")
                            st.balloons()  # This simulates a celebratory animation
                        else:
                            st.write("**Bad luck! The customer is predicted to churn and discontinue their subscription.** 😞")
                            st.toast('bad luck', icon="👎")
                    except Exception as e:
                        st.error(f"An error occurred during prediction: {e}")
    
                
        if prediction_method=='Predict Churn for Entire DataFrame':
                

                st.markdown('<p style="color:red;">Select file type</p>', unsafe_allow_html=True)

        
                file_type = st.selectbox("", ("CSV", "Excel"))
                #uploaded_file=None


        
                uploaded_file = st.file_uploader(f"Upload {file_type} file",type=[file_type.lower()])

                if file_type=="CSV":

                    try:
                        df=pd.read_csv(uploaded_file)
                        df.to_csv("df.csv",index=False)
                    except Exception as e:
                                    st.write("Not Uploaded")
                else:
                    try:
                        df=pd.read_excel(uploaded_file)
                        df.to_excel("df.xlsx",index=False)

                    except Exception as e:
                                    st.write("Not Uploaded")

                    
        
                #with c1:
                if st.button("Predict"):
                    with st.spinner("Please wait while predicting...."):
                        time.sleep(1)
                    
                    
                        try:
                            result = model.predict(df)
                            laundering = ["Yes" if pred == 1 else "No" for pred in result]
                            df["laundering"] = laundering
        
                            l_counts = df['laundering'].value_counts()
        
                            st.markdown(f'<p style="color:orange; font-weight:bold;">No of churn customers: {l_counts["Yes"]}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="color:orange; font-weight:bold;">Total customers: {len(laundering)}</p>', unsafe_allow_html=True)
                            st.title("Go to Prediction Analytics to view analytics")
                                    
        
        
                        except Exception as e:
                                st.error("Please upload your file before predicting...")
                        
                    
                        


elif selected == "Prediction Analytics":
    data=False



   
    with st.container():
         st.title('Churn Prediction Analysis...........')
    try:
         df = pd.read_csv("df.csv")
         data=True
    except Exception as e:
         st.title("You Have No Any Prediction yet")
    

    


    #st.set_option('deprecation.showPyplotGlobalUse', False)
    
    p1,p2=st.columns(2)

    if data:
      st.write("hi")
    
    


