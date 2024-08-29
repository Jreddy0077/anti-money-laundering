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




####################################################################################

db_user = '2yasPb2k6DKrXZH.root'
db_password = 'E28f3eorNGjxx6K4'
db_host = 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com'
db_port = '4000'
db_name = 'test'
ca_path = '/path/to/ca_cert.pem'  

# creating the sql syntax for connecting with the database

connection_string = (
    f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?'
    f'ssl_ca={ca_path}&ssl_verify_cert=true'

)

# ca_path 
#  CA certificate is used to verify the identity of the database server to ensure that the connection is secure.

def add_user(first_name, last_name, sur_name, number, mail, password):
    try:
        engine = create_engine(connection_string)
        conn = engine.connect()

        insert_query =text("""
            INSERT INTO users (first_name, last_name, sur_name, number, mail, password)
            VALUES (:first_name, :last_name, :sur_name, :number, :mail, :password)
        """)
        
        conn.execute(insert_query, {
            'first_name': first_name,
            'last_name': last_name,
            'sur_name': sur_name,
            'number': number,
            'mail': mail,
            'password': password
        })
        
        conn.commit()
        conn.close()
        
        st.success("User added successfully!")
    except SQLAlchemyError as e:
        st.error(f"An error occurred: {str(e)}")

############################################################################



try:
    engine = create_engine(connection_string)
    conn = engine.connect()
    df_user= pd.read_sql('SELECT * FROM users', conn)

    df_user['number'] = df_user['number'].astype(str)

    conn.close()
    engine.dispose()
except SQLAlchemyError as e:
    st.error(f"An error occurred: {str(e)}")



df=None
def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()




#st.set_page_config(layout="wide")

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
        options=["Home", "Register/Login/Profile"],  # required
        icons=["house", "person-square"],  # optional
         menu_icon="box-arrow-in-right",
        default_index=1,  # optional
    )

if selected == "Home":
    pass;
    
elif selected == "Register/Login/Profile":
    l_number = list(df_user["number"])


   
    

    st.markdown('<h2 style="color:orange;">Welcome To Churn Prediction Application</h2>', unsafe_allow_html=True)





    with st.container():
        st.markdown('<p style="color:red;">To access the app please Login or Signup</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:red;">Select an option:</p>', unsafe_allow_html=True)
        option = st.selectbox('', ('Login',"Signup"))


    col1, col2 ,col3= st.columns([2,1,3])

    


       



    if option=="Login":
        import streamlit as st
        import pandas as pd
        
        # Assuming l_number and df_user are already defined
        
        with col1:
            st.markdown('<p style="color:gold;">Enter Your Mobile Number..</p>', unsafe_allow_html=True)
            number1 = st.text_input("", key="number1")
        
            # Initialize mobile check
            mobile = False
        
            # Check if the number is in the list
            if number1 in l_number:
                st.markdown('<p style="color:gold;">Mobile Number Is Correct</p>', unsafe_allow_html=True)
                mobile = True
            else:
                st.markdown('<p style="color:gold;">Incorrect Mobile Number</p>', unsafe_allow_html=True)
        
            # UI for password input
            st.markdown('<p style="color:gold;">Enter Your Password..</p>', unsafe_allow_html=True)
            password1 = st.text_input("", key="password1", type="password")
        
            # Initialize password check
            passs = False
        
            if mobile:
                # Check if the number is present in the DataFrame
                if number1 in df_user["number"].values:
                    # Get the original password for the entered number
                    password_org = df_user[df_user["number"] == number1]["password"].values[0]
        
                    # Check if the entered password matches the original password
                    if password_org == password1:
                        st.markdown('<p style="color:gold;">Password Is Correct</p>', unsafe_allow_html=True)
                        passs = True
                    else:
                        st.markdown('<p style="color:gold;">Incorrect Password</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color:gold;">Mobile Number Not Found in Database</p>', unsafe_allow_html=True)
            
            # Check login button
            if st.button("Login"):
                if mobile and passs:
                    st.markdown('<p style="color:gold;">Successfully Logged In</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color:gold;">Enter The Details Correctly</p>', unsafe_allow_html=True)
        
        with col3:
            if mobile and passs:
                if st.button("Show Profile"):
                    user_info = df_user[df_user["number"] == number1].iloc[0]
                    name = f"{user_info['first_name']} {user_info['last_name']} {user_info['sur_name']}"
                    mail = user_info['mail']
                    contact = number1
        
                    st.write("     ")
                    st.markdown(f'<h3 style="color:red;">Name: {name}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="color:red;">Contact: {contact}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="color:red;">Mail: {mail}</h3>', unsafe_allow_html=True)
        
        
                                
        
                    
                            

    coll1,coll2=st.columns(2)
    if option == "Signup":
        with coll1:
            st.markdown('<p style="color:gold;">Enter The First Name:</p>', unsafe_allow_html=True)
            first_name = st.text_input("", key="first_name")
            st.markdown('<p style="color:gold;">Enter The Surname:</p>', unsafe_allow_html=True)
            sur_name = st.text_input("", key="sur_name")

            st.markdown('<p style="color:gold;">Enter The Last Name:</p>', unsafe_allow_html=True)
            last_name = st.text_input("", key="last_name")
            st.markdown('<p style="color:gold;">Enter Your Mobile Number:</p>', unsafe_allow_html=True)
            number = st.text_input("", key="number")

            if number.isnumeric() and number[0] in "9876" and len(number) == 10:
                st.markdown('<p style="color:green;">Number is valid</p>', unsafe_allow_html=True)
                number_val = True
            else:
                st.markdown('<p style="color:red;">Number is invalid</p>', unsafe_allow_html=True)
                number_val = False

            

        

        #with coll2:

            st.markdown('<p style="color:gold;">Enter The Mail</p>', unsafe_allow_html=True)
            mail = st.text_input("", key="maill")

            def is_valid_email(email):
                pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                return pattern.match(email) is not None

            if is_valid_email(mail):
                st.markdown('<p style="color:green;">The email address is valid</p>', unsafe_allow_html=True)
                mail_val = True
            else:
                st.markdown('<p style="color:red;">The email address is invalid</p>', unsafe_allow_html=True)
                mail_val = False

            def is_valid_password(password):
                pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@#$!%*?&]{8,16}$')
                return pattern.match(password) is not None

    
            
            st.markdown('<p style="color:gold;">Enter the password</p>', unsafe_allow_html=True)
            password = st.text_input("", key="password", type="password")

            if is_valid_password(password):
                st.markdown('<p style="color:green;">The password is valid</p>', unsafe_allow_html=True)
                password_val = True
            else:
                st.markdown('<p style="color:red;">The password should have at least one lowercase letter, one uppercase letter, one digit, one special character (@$!%*?&) and be 8-16 characters long.</p>', unsafe_allow_html=True)
                password_val = False

            st.markdown('<p style="color:gold;">Confirm the password</p>', unsafe_allow_html=True)
            c_password = st.text_input("", key="c_password", type="password")

            if c_password == password:
                st.markdown('<p style="color:green;">Password Is Matched</p>', unsafe_allow_html=True)
                c_password_val = True
            else:
                st.markdown('<p style="color:red;">Password Is Not Matches</p>', unsafe_allow_html=True)
                c_password_val = False
            
    

        if st.button("Register"):
            l_password = list(df_user["password"])

            l_number = list(df_user["number"])
            l_mail = list(df_user["mail"])
            

            
            
            if (number) in l_number:
                st.markdown('<p style="color:red;">This Number is Already Registered</p>', unsafe_allow_html=True)
            elif mail in l_mail:
                st.markdown('<p style="color:red;">This mail is Already Registered</p>', unsafe_allow_html=True)
            elif password in l_password:
                st.markdown('<p style="color:red;">This password is Already Registered</p>', unsafe_allow_html=True)


            elif c_password_val and password_val and mail_val and number_val:

                
            

                #new_user = [first_name, last_name, sur_name, (number), mail, password]

                add_user(first_name, last_name, sur_name, number, mail, password)




                
                st.markdown('<p style="color:green;">Successfully Registered</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:red;">You Have Entered Something Wrong</p>', unsafe_allow_html=True)
