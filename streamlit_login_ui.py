import streamlit as st
import time
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(
    page_title="Modern Login UI",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit elements and set custom styling
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default padding and margins */
    .stApp {
        background: #1a1a2e;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: none !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00d4ff;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00b8d4;
    }
    
    /* Animation keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(0, 212, 255, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(0, 212, 255, 0);
        }
    }
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for toggling between login and signup
if 'is_login' not in st.session_state:
    st.session_state.is_login = True

# Function to toggle between login and signup
def toggle_form():
    st.session_state.is_login = not st.session_state.is_login

# Main container with custom CSS
st.markdown("""
<div class="auth-wrapper" style="
    position: relative;
    width: 100%;
    max-width: 900px;
    height: 600px;
    margin: 50px auto;
    border: 2px solid #00d4ff;
    box-shadow: 0 0 30px #00d4ff, 0 0 60px rgba(0, 212, 255, 0.3);
    overflow: hidden;
    background: #1a1a2e;
    border-radius: 10px;
    animation: float 6s ease-in-out infinite;
">
    <!-- Background Shape -->
    <div class="background-shape" style="
        position: absolute;
        right: 0;
        top: -5px;
        height: 600px;
        width: 850px;
        background: linear-gradient(45deg, #1a1a2e, #00d4ff, #1a1a2e, #00d4ff);
        background-size: 300% 300%;
        transform: rotate(10deg) skewY(40deg);
        transform-origin: bottom right;
        transition: 1.5s ease;
        animation: gradientShift 10s ease infinite;
    "></div>
    
    <!-- Secondary Shape -->
    <div class="secondary-shape" style="
        position: absolute;
        left: 250px;
        top: 100%;
        height: 700px;
        width: 850px;
        background: #1a1a2e;
        border-top: 3px solid #00d4ff;
        transform: rotate(0deg) skewY(0deg);
        transform-origin: bottom left;
        transition: 1.5s ease;
    "></div>
""", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns(2)

# LOGIN FORM (Left side when login is active)
with col1:
    if st.session_state.is_login:
        login_container = st.container()
        with login_container:
            # Login Form
            st.markdown("""
            <div class="credentials-panel signin" style="
                position: absolute;
                top: 0;
                left: 0;
                width: 50%;
                height: 100%;
                display: flex;
                justify-content: center;
                flex-direction: column;
                padding: 0 40px;
                z-index: 10;
            ">
                <h2 style="
                    font-size: 32px;
                    text-align: center;
                    color: #fff;
                    margin-bottom: 20px;
                    animation: slideInLeft 0.6s ease forwards;
                ">Login</h2>
                
                <form action="#" method="post">
            """, unsafe_allow_html=True)
            
            # Username field
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        height: 50px;
                        margin-top: 25px;
                        animation: slideInLeft 0.7s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username", label_visibility="collapsed", placeholder=" ")
            st.markdown("""
                        <i class="fa-solid fa-user" style="
                            position: absolute;
                            top: 50%;
                            right: 0;
                            font-size: 18px;
                            transform: translateY(-50%);
                            color: #00d4ff;
                        "></i>
                    </div>
            """, unsafe_allow_html=True)
            
            # Password field
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        height: 50px;
                        margin-top: 25px;
                        animation: slideInLeft 0.8s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            password = st.text_input("Password", type="password", key="login_password", label_visibility="collapsed", placeholder=" ")
            st.markdown("""
                        <i class="fa-solid fa-lock" style="
                            position: absolute;
                            top: 50%;
                            right: 0;
                            font-size: 18px;
                            transform: translateY(-50%);
                            color: #00d4ff;
                        "></i>
                    </div>
            """, unsafe_allow_html=True)
            
            # Login button
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        margin-top: 30px;
                        animation: slideInLeft 0.9s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            
            if st.button("Login", key="login_btn", use_container_width=True):
                if username and password:
                    st.success(f"Welcome back, {username}! 🎉")
                    time.sleep(1)
                    st.balloons()
                else:
                    st.error("Please fill in all fields!")
            
            st.markdown("""
                    </div>
                    
                    <div class="switch-link" style="
                        font-size: 14px;
                        text-align: center;
                        margin: 20px 0 10px;
                        animation: slideInLeft 1.0s ease forwards;
                    ">
                        <p style="color: #fff;">Don't have an account? <br> 
            """, unsafe_allow_html=True)
            
            # Sign Up link
            if st.button("Sign Up", key="to_signup"):
                toggle_form()
                st.rerun()
            
            st.markdown("""
                        </p>
                    </div>
                </form>
            </div>
            """, unsafe_allow_html=True)

# WELCOME SECTION for LOGIN (Right side when login is active)
with col2:
    if st.session_state.is_login:
        st.markdown("""
        <div class="welcome-section signin" style="
            position: absolute;
            top: 0;
            right: 0;
            height: 100%;
            width: 50%;
            display: flex;
            justify-content: center;
            flex-direction: column;
            text-align: right;
            padding: 0 40px 60px 150px;
            z-index: 5;
        ">
            <h2 style="
                color: #fff;
                font-size: 36px;
                text-transform: uppercase;
                line-height: 1.3;
                animation: slideInRight 0.8s ease forwards;
                text-shadow: 0 0 10px #00d4ff;
            ">WELCOME BACK!</h2>
            <p style="
                color: #fff;
                font-size: 16px;
                animation: slideInRight 1.0s ease forwards;
                opacity: 0.8;
            ">We missed you! Sign in to continue your journey with us.</p>
        </div>
        """, unsafe_allow_html=True)

# SIGNUP FORM (Right side when signup is active)
with col2:
    if not st.session_state.is_login:
        signup_container = st.container()
        with signup_container:
            st.markdown("""
            <div class="credentials-panel signup" style="
                position: absolute;
                top: 0;
                right: 0;
                width: 50%;
                height: 100%;
                display: flex;
                justify-content: center;
                flex-direction: column;
                padding: 0 60px;
                z-index: 10;
            ">
                <h2 style="
                    font-size: 32px;
                    text-align: center;
                    color: #fff;
                    margin-bottom: 20px;
                    animation: slideInRight 0.6s ease forwards;
                ">Register</h2>
                
                <form action="#" method="post">
            """, unsafe_allow_html=True)
            
            # Username field
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        height: 50px;
                        margin-top: 25px;
                        animation: slideInRight 0.7s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            signup_username = st.text_input("Username", key="signup_username", label_visibility="collapsed", placeholder=" ")
            st.markdown("""
                        <i class="fa-solid fa-user" style="
                            position: absolute;
                            top: 50%;
                            right: 0;
                            font-size: 18px;
                            transform: translateY(-50%);
                            color: #00d4ff;
                        "></i>
                    </div>
            """, unsafe_allow_html=True)
            
            # Email field
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        height: 50px;
                        margin-top: 25px;
                        animation: slideInRight 0.8s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            signup_email = st.text_input("Email", key="signup_email", label_visibility="collapsed", placeholder=" ")
            st.markdown("""
                        <i class="fa-solid fa-envelope" style="
                            position: absolute;
                            top: 50%;
                            right: 0;
                            font-size: 18px;
                            transform: translateY(-50%);
                            color: #00d4ff;
                        "></i>
                    </div>
            """, unsafe_allow_html=True)
            
            # Password field
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        height: 50px;
                        margin-top: 25px;
                        animation: slideInRight 0.9s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            signup_password = st.text_input("Password", type="password", key="signup_password", label_visibility="collapsed", placeholder=" ")
            st.markdown("""
                        <i class="fa-solid fa-lock" style="
                            position: absolute;
                            top: 50%;
                            right: 0;
                            font-size: 18px;
                            transform: translateY(-50%);
                            color: #00d4ff;
                        "></i>
                    </div>
            """, unsafe_allow_html=True)
            
            # Register button
            st.markdown("""
                    <div class="field-wrapper" style="
                        position: relative;
                        width: 100%;
                        margin-top: 30px;
                        animation: slideInRight 1.0s ease forwards;
                    ">
            """, unsafe_allow_html=True)
            
            if st.button("Register", key="signup_btn", use_container_width=True):
                if signup_username and signup_email and signup_password:
                    st.success(f"Welcome {signup_username}! Account created successfully! 🎉")
                    time.sleep(1)
                    st.balloons()
                    time.sleep(2)
                    toggle_form()
                    st.rerun()
                else:
                    st.error("Please fill in all fields!")
            
            st.markdown("""
                    </div>
                    
                    <div class="switch-link" style="
                        font-size: 14px;
                        text-align: center;
                        margin: 20px 0 10px;
                        animation: slideInRight 1.1s ease forwards;
                    ">
                        <p style="color: #fff;">Already have an account? <br> 
            """, unsafe_allow_html=True)
            
            # Sign In link
            if st.button("Sign In", key="to_login"):
                toggle_form()
                st.rerun()
            
            st.markdown("""
                        </p>
                    </div>
                </form>
            </div>
            """, unsafe_allow_html=True)

# WELCOME SECTION for SIGNUP (Left side when signup is active)
with col1:
    if not st.session_state.is_login:
        st.markdown("""
        <div class="welcome-section signup" style="
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 50%;
            display: flex;
            justify-content: center;
            flex-direction: column;
            text-align: left;
            padding: 0 150px 60px 38px;
            z-index: 5;
        ">
            <h2 style="
                color: #fff;
                font-size: 36px;
                text-transform: uppercase;
                line-height: 1.3;
                animation: slideInLeft 0.8s ease forwards;
                text-shadow: 0 0 10px #00d4ff;
            ">WELCOME!</h2>
            <p style="
                color: #fff;
                font-size: 16px;
                animation: slideInLeft 1.0s ease forwards;
                opacity: 0.8;
            ">Join us today! Create an account to access all features.</p>
        </div>
        """, unsafe_allow_html=True)

# Close the auth-wrapper div
st.markdown("""
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer" style="
    text-align: center;
    padding: 20px;
    margin-top: 20px;
    font-size: 14px;
    color: #fff;
    animation: fadeInUp 1.2s ease forwards;
">
    <p>Made with ❤️ by <a href="#" style="
        color: #00d4ff;
        text-decoration: none;
        font-weight: 600;
        transition: 0.3s;
    " onmouseover="this.style.textDecoration='underline'" 
       onmouseout="this.style.textDecoration='none'">Jaipur Team</a></p>
</div>

<!-- Font Awesome Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# Add JavaScript for interactive effects
st.markdown("""
<script>
    // Add hover effects and animations
    document.addEventListener('DOMContentLoaded', function() {
        const buttons = document.querySelectorAll('.stButton button');
        buttons.forEach(button => {
            button.style.transition = 'all 0.3s ease';
            button.style.animation = 'pulse 2s infinite';
            
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
                this.style.boxShadow = '0 0 20px #00d4ff';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            });
        });
        
        // Add floating animation to inputs
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
    });
</script>
""", unsafe_allow_html=True)