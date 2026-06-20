import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# Configuration
USERS_FILE = 'users.json'

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Helper functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def verify_user(username, password):
    """Verify user credentials"""
    users = load_users()
    if username in users:
        if users[username]['password'] == hash_password(password):
            return True
    return False

def create_user(username, password, email):
    """Create new user account"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_users(users)
    return True, "Account created successfully"

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.username = None

# Main application
def main():
    st.set_page_config(
        page_title="Streamlit Login System",
        page_icon="🔐",
        layout="centered"
    )
    
    # Check if user is logged in
    if st.session_state.logged_in:
        show_dashboard()
    else:
        show_login_page()

def show_login_page():
    """Display login/signup page"""
    st.title("🔐 Welcome")
    
    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # Login tab
    with tab1:
        st.subheader("Login to your account")
        
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    if verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
    
    # Signup tab
    with tab2:
        st.subheader("Create a new account")
        
        with st.form("signup_form"):
            new_username = st.text_input("Username", key="signup_username")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            signup = st.form_submit_button("Sign Up", use_container_width=True)
            
            if signup:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, message = create_user(new_username, new_password, new_email)
                        if success:
                            st.success(message)
                            st.info("Please login with your new credentials")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill all fields")

def show_dashboard():
    """Display dashboard for logged-in users"""
    st.title(f"👋 Welcome, {st.session_state.username}!")
    
    # Sidebar with user info
    with st.sidebar:
        st.header("User Profile")
        st.write(f"**Username:** {st.session_state.username}")
        
        users = load_users()
        if st.session_state.username in users:
            user_data = users[st.session_state.username]
            st.write(f"**Email:** {user_data['email']}")
            st.write(f"**Member since:** {user_data['created_at']}")
        
        st.divider()
        
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Main dashboard content
    st.subheader("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", len(load_users()))
    
    with col2:
        st.metric("Status", "Active", delta="Online")
    
    with col3:
        st.metric("Session", "Valid", delta="Authenticated")
    
    st.divider()
    
    # Sample dashboard content
    st.subheader("📊 Your Content")
    
    tab1, tab2, tab3 = st.tabs(["Overview", "Settings", "Activity"])
    
    with tab1:
        st.write("This is your main dashboard overview.")
        st.info("You are successfully logged in! This is a protected area.")
        
        # Sample chart
        import pandas as pd
        import numpy as np
        
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['A', 'B', 'C']
        )
        st.line_chart(chart_data)
    
    with tab2:
        st.write("Settings and preferences")
        
        with st.form("settings_form"):
            st.text_input("Display Name", value=st.session_state.username)
            st.selectbox("Theme", ["Light", "Dark", "Auto"])
            st.checkbox("Email Notifications")
            
            if st.form_submit_button("Save Settings"):
                st.success("Settings saved successfully!")
    
    with tab3:
        st.write("Recent activity")
        st.write("- Login successful")
        st.write(f"- Last login: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
