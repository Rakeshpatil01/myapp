import streamlit as st
from multiapp import MultiApp
from apps import home, data, model
import requests
loginSection = st.container()
logOutSection = st.container()

app = MultiApp()


def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    res = requests.post(f"http://localhost:8080/token", json=data)
    if res.status_code == 200:
        return True
    else:
        return False


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        col1, col2, col3 = st.columns(3)
        with col3:
            st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with loginSection:
        st.markdown("""
        # FINSYS-I

        welcome! FINSYS-I is helper tool for day to day activity
        """)
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(
                label="", value="", placeholder="Enter your user name")
            password = st.text_input(
                label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked,
                      args=(userName, password))


# first run will have nothing in session_state
if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False
    show_login_page()
else:
    if st.session_state['loggedIn']:
        # Add all your application here
        app.add_app("Home", home.app)
        app.add_app("Data", data.app)
        app.add_app("Model", model.app)
        # The main app
        show_logout_page()
    else:
        show_login_page()


app.run()
