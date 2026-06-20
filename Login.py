import streamlit as st
from pathlib import Path
from streamlit.components.v1 import html as st_html
import urllib.parse

# Page configuration - Full screen
st.set_page_config(
    page_title="Login & Signup",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)
if "token" in st.query_params:
    st.session_state["token"] = st.query_params["token"]
    st.query_params.clear()
    st.switch_page("pages/App.py")
    st.stop()
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {visibility: hidden;}
[data-testid="stSidebar"] {visibility: hidden;}
#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
section.main > div {padding-top: 0rem;}
.block-container {padding-top: 0rem; padding-bottom: 0rem;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Read your existing JavaScript file
base_path = Path(__file__).resolve().parent
js_path = base_path / "style.js"

try:
    js_content = js_path.read_text(encoding="utf-8")
except FileNotFoundError:
    js_content = """
    // Fallback JS if style.js not found
    document.addEventListener('DOMContentLoaded', function() {
        const authWrapper = document.querySelector('.auth-wrapper');
        const registerTrigger = document.querySelector('.register-trigger');
        const loginTrigger = document.querySelector('.login-trigger');
        
        if(registerTrigger) {
            registerTrigger.addEventListener('click', function(e) {
                e.preventDefault();
                authWrapper.classList.add('toggled');
            });
        }
        
        if(loginTrigger) {
            loginTrigger.addEventListener('click', function(e) {
                e.preventDefault();
                authWrapper.classList.remove('toggled');
            });
        }
    });
    """
st.markdown("""
<style>

/* Remove ALL default Streamlit spacing */
html, body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove main block padding */
.block-container {
    padding: 0 !important;
    margin: 0 !important;
}

/* Remove max-width restriction */
section.main > div {
    max-width: 100% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Remove extra wrapper spacing */
[data-testid="stAppViewContainer"] {
    padding: 0 !important;
    margin: 0 !important;
}

/* Hide sidebar completely */
[data-testid="stSidebar"] {
    display: none !important;
}

/* Hide header/footer/menu */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Remove iframe margins */
iframe {
    margin: 0 !important;
    padding: 0 !important;
}

</style>
""", unsafe_allow_html=True)
# Your complete CSS (embedded - no external file needed)
css_content = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
    color: #fff;
}

html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
}

body {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #1a1a2e;
    padding: 20px;
}

.footer {
    margin-top: 30px;
    text-align: center;
    padding: 15px;
    font-size: 14px;
    color: #fff;
}

.footer a {
    color: #00d4ff;
    text-decoration: none;
    font-weight: 600;
    transition: .3s;
}

.footer a:hover {
    text-decoration: underline;
    color: #00b8d4;
}

.auth-wrapper {
    position: relative;
    width: 100%;
    max-width: 1000px;
    height: 700px;
    border: 2px solid #00d4ff;
    box-shadow: 0 0 25px #00d4ff;
    overflow: hidden;
}

.auth-wrapper .credentials-panel {
    position: absolute;
    top: 0;
    width: 50%;
    height: 100%;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.credentials-panel.signin {
    left: 0;
    padding: 0 40px;
}

.credentials-panel.signin .slide-element {
    transform: translateX(0%);
    transition: .7s;
    opacity: 1;
}

.credentials-panel.signin .slide-element:nth-child(1) {
    transition-delay: 2.1s;
}

.credentials-panel.signin .slide-element:nth-child(2) {
    transition-delay: 2.2s;
}

.credentials-panel.signin .slide-element:nth-child(3) {
    transition-delay: 2.3s;
}

.credentials-panel.signin .slide-element:nth-child(4) {
    transition-delay: 2.4s;
}

.credentials-panel.signin .slide-element:nth-child(5) {
    transition-delay: 2.5s;
}

.auth-wrapper.toggled .credentials-panel.signin .slide-element {
    transform: translateX(-120%);
    opacity: 0;
}

.auth-wrapper.toggled .credentials-panel.signin .slide-element:nth-child(1) {
    transition-delay: 0s;
}

.auth-wrapper.toggled .credentials-panel.signin .slide-element:nth-child(2) {
    transition-delay: 0.1s;
}

.auth-wrapper.toggled .credentials-panel.signin .slide-element:nth-child(3) {
    transition-delay: 0.2s;
}

.auth-wrapper.toggled .credentials-panel.signin .slide-element:nth-child(4) {
    transition-delay: 0.3s;
}

.auth-wrapper.toggled .credentials-panel.signin .slide-element:nth-child(5) {
    transition-delay: 0.4s;
}

.credentials-panel.signup {
    right: 0;
    padding: 0 60px;
}

.credentials-panel.signup .slide-element {
    transform: translateX(120%);
    transition: .7s ease;
    opacity: 0;
    filter: blur(10px);
}

.credentials-panel.signup .slide-element:nth-child(1) {
    transition-delay: 0s;
}

.credentials-panel.signup .slide-element:nth-child(2) {
    transition-delay: 0.1s;
}

.credentials-panel.signup .slide-element:nth-child(3) {
    transition-delay: 0.2s;
}

.credentials-panel.signup .slide-element:nth-child(4) {
    transition-delay: 0.3s;
}

.credentials-panel.signup .slide-element:nth-child(5) {
    transition-delay: 0.4s;
}

.credentials-panel.signup .slide-element:nth-child(6) {
    transition-delay: 0.5s;
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element {
    transform: translateX(0%);
    opacity: 1;
    filter: blur(0px);
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element:nth-child(1) {
    transition-delay: 1.7s;
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element:nth-child(2) {
    transition-delay: 1.8s;
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element:nth-child(3) {
    transition-delay: 1.9s;
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element:nth-child(4) {
    transition-delay: 1.9s;
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element:nth-child(5) {
    transition-delay: 2.0s;
}

.auth-wrapper.toggled .credentials-panel.signup .slide-element:nth-child(6) {
    transition-delay: 2.1s;
}

.credentials-panel h2 {
    font-size: 32px;
    text-align: center;
}

.credentials-panel .field-wrapper {
    position: relative;
    width: 100%;
    height: 50px;
    margin-top: 25px;
}

.field-wrapper input {
    width: 100%;
    height: 100%;
    background: transparent;
    border: none;
    outline: none;
    font-size: 16px;
    color: #fff;
    font-weight: 600;
    border-bottom: 2px solid #fff;
    padding-right: 23px;
    transition: .5s;
}

.field-wrapper input:focus,
.field-wrapper input:valid {
    border-bottom: 2px solid #00d4ff;
}

.field-wrapper label {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    font-size: 16px;
    color: #fff;
    transition: .5s;
}

.field-wrapper input:focus~label,
.field-wrapper input:valid~label {
    top: -5px;
    color: #00d4ff;
}

.field-wrapper i {
    position: absolute;
    top: 50%;
    right: 0;
    font-size: 18px;
    transform: translateY(-50%);
    color: #fff;
}

.field-wrapper input:focus~i,
.field-wrapper input:valid~i {
    color: #00d4ff;
}

.submit-button {
    position: relative;
    width: 100%;
    height: 45px;
    background: transparent;
    border-radius: 40px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    border: 2px solid #00d4ff;
    overflow: hidden;
    z-index: 1;
}

.submit-button::before {
    content: "";
    position: absolute;
    height: 300%;
    width: 100%;
    background: linear-gradient(#1a1a2e, #00d4ff, #1a1a2e, #00d4ff);
    top: -100%;
    left: 0;
    z-index: -1;
    transition: .5s;
}

.submit-button:hover:before {
    top: 0;
}

.switch-link {
    font-size: 14px;
    text-align: center;
    margin: 20px 0 10px;
}

.switch-link a {
    text-decoration: none;
    color: #00d4ff;
    font-weight: 600;
}

.switch-link a:hover {
    text-decoration: underline;
}

.welcome-section {
    position: absolute;
    top: 0;
    height: 100%;
    width: 50%;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.welcome-section.signin {
    right: 0;
    text-align: right;
    padding: 0 40px 60px 150px;
}

.welcome-section.signin .slide-element {
    transform: translateX(0);
    transition: .7s ease;
    opacity: 1;
    filter: blur(0px);
}

.welcome-section.signin .slide-element:nth-child(1) {
    transition-delay: 2.0s;
}

.welcome-section.signin .slide-element:nth-child(2) {
    transition-delay: 2.1s;
}

.auth-wrapper.toggled .welcome-section.signin .slide-element {
    transform: translateX(120%);
    opacity: 0;
    filter: blur(10px);
}

.auth-wrapper.toggled .welcome-section.signin .slide-element:nth-child(1) {
    transition-delay: 0s;
}

.auth-wrapper.toggled .welcome-section.signin .slide-element:nth-child(2) {
    transition-delay: 0.1s;
}

.welcome-section.signup {
    left: 0;
    text-align: left;
    padding: 0 150px 60px 38px;
    pointer-events: none;
}

.welcome-section.signup .slide-element {
    transform: translateX(-120%);
    transition: .7s ease;
    opacity: 0;
    filter: blur(10PX);
}

.welcome-section.signup .slide-element:nth-child(1) {
    transition-delay: 0s;
}

.welcome-section.signup .slide-element:nth-child(2) {
    transition-delay: 0.1s;
}

.auth-wrapper.toggled .welcome-section.signup .slide-element {
    transform: translateX(0%);
    opacity: 1;
    filter: blur(0);
}

.auth-wrapper.toggled .welcome-section.signup .slide-element:nth-child(1) {
    transition-delay: 1.7s;
}

.auth-wrapper.toggled .welcome-section.signup .slide-element:nth-child(2) {
    transition-delay: 1.8s;
}

.welcome-section h2 {
    text-transform: uppercase;
    font-size: 36px;
    line-height: 1.3;
}

.welcome-section p {
    font-size: 16px;
}

.auth-wrapper .background-shape {
    position: absolute;
    right: 0;
    top: -5px;
    height: 600px;
    width: 850px;
    background: linear-gradient(45deg, #1a1a2e, #00d4ff);
    transform: rotate(10deg) skewY(40deg);
    transform-origin: bottom right;
    transition: 1.5s ease;
    transition-delay: 1.6s;
}

.auth-wrapper.toggled .background-shape {
    transform: rotate(0deg) skewY(0deg);
    transition-delay: .5s;
}

.auth-wrapper .secondary-shape {
    position: absolute;
    left: 250px;
    top: 100%;
    height: 700px;
    width: 900px;
    background: #1a1a2e;
    border-top: 3px solid #00d4ff;
    transform: rotate(0deg) skewY(0deg);
    transform-origin: bottom left;
    transition: 1.5s ease;
    transition-delay: .5s;
}

.auth-wrapper.toggled .secondary-shape {
    transform: rotate(-11deg) skewY(-41deg);
    transition-delay: 1.2s;
}

@media (max-width: 768px) {
    body {
         padding: 10px;
    }

    .footer {
        margin-top: 20px;
        font-size: 13px;
    }

    .auth-wrapper {
        height: auto;
        min-height: 500px;
        flex-direction: column;
    }

    .auth-wrapper .credentials-panel,
    .welcome-section {
        width: 100%;
        position: relative;
    }

    .credentials-panel.signin,
    .credentials-panel.signup {
        padding: 40px 30px;
        left: 0;
        right: 0;
    }

    .credentials-panel.signin {
        display: flex;
        animation: fadeInUp 0.6s ease forwards;
    }

    .credentials-panel.signup {
        display: none;
    }

    .auth-wrapper.toggled .credentials-panel.signin {
        display: none;
        animation: fadeOutDown 0.6s ease forwards;
    }

    .auth-wrapper.toggled .credentials-panel.signup {
        display: flex;
        animation: fadeInUp 0.6s ease forwards;
    }

    .credentials-panel.signin .slide-element,
    .credentials-panel.signup .slide-element {
        transform: translateY(0);
        opacity: 1;
        filter: blur(0);
        animation: slideInUp 0.5s ease forwards;
    }

    .credentials-panel.signin .slide-element:nth-child(1),
    .credentials-panel.signup .slide-element:nth-child(1) {
        animation-delay: 0.1s;
        opacity: 0;
    }

    .credentials-panel.signin .slide-element:nth-child(2),
    .credentials-panel.signup .slide-element:nth-child(2) {
        animation-delay: 0.2s;
        opacity: 0;
    }

    .credentials-panel.signin .slide-element:nth-child(3),
    .credentials-panel.signup .slide-element:nth-child(3) {
        animation-delay: 0.3s;
        opacity: 0;
    }

    .credentials-panel.signin .slide-element:nth-child(4),
    .credentials-panel.signup .slide-element:nth-child(4) {
        animation-delay: 0.4s;
        opacity: 0;
    }

    .credentials-panel.signin .slide-element:nth-child(5),
    .credentials-panel.signup .slide-element:nth-child(5) {
        animation-delay: 0.5s;
        opacity: 0;
    }

    .credentials-panel.signup .slide-element:nth-child(6) {
        animation-delay: 0.6s;
        opacity: 0;
    }

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

    @keyframes fadeOutDown {
        from {
            opacity: 1;
            transform: translateY(0);
        }

        to {
            opacity: 0;
            transform: translateY(30px);
        }
    }

    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .welcome-section {
        display: none;
    }

    .credentials-panel h2 {
        font-size: 28px;
        margin-bottom: 10px;
    }

    .auth-wrapper .background-shape,
    .auth-wrapper .secondary-shape {
        display: none;
    }

    .field-wrapper {
        margin-top: 20px;
    }
}

@media (max-width: 480px) {

    .credentials-panel.signin,
    .credentials-panel.signup {
        padding: 30px 20px;
    }

    .credentials-panel h2 {
        font-size: 24px;
    }

    .field-wrapper input,
    .field-wrapper label {
        font-size: 14px;
    }

    .submit-button {
        font-size: 14px;
        height: 40px;
    }

    .switch-link {
        font-size: 13px;
    }
}
"""
API_BASE_URL = "https://localhost:7047/api"
# Predefined credentials




# Complete HTML with embedded CSS and JS
page_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login & Signup Form</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <style>
        html, body {{
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        {css_content}
    </style>
    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css"
        integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
    <div class="auth-wrapper">
        <div class="background-shape"></div>
        <div class="secondary-shape"></div>
        
        <!-- Login Panel -->
        <div class="credentials-panel signin">
            <h2 class="slide-element">Login</h2>
            <form id="login-form">
                <div class="field-wrapper slide-element">
                    <input type="text" id="login-username" required />
                    <label for="login-username">Username</label>
                    <i class="fa-solid fa-user"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <input type="password" id="login-password" required />
                    <label for="login-password">Password</label>
                    <i class="fa-solid fa-lock"></i>
                </div>

                <div id="login-error" style="color: #ff4757; text-align: center; font-size: 14px; margin-top: 10px; display: none;">
                    Invalid username or password!
                </div>

                <div class="field-wrapper slide-element">
                    <button class="submit-button" type="submit">Login</button>
                </div>

                <div class="switch-link slide-element">
                    <p>Don't have an account? <br /> <a href="#" class="register-trigger">Sign Up</a></p>
                </div>
            </form>
        </div>

        <!-- Welcome Section (Login) -->
        <div class="welcome-section signin">
            <h2 class="slide-element">WELCOME BACK!</h2>
        </div>

        <!-- Signup Panel -->
        <div class="credentials-panel signup">
            <h2 class="slide-element">Register</h2>
            <form id="signup-form">
                <div class="field-wrapper slide-element">
                    <input type="text" id="signup-username" required />
                    <label for="signup-username">Username</label>
                    <i class="fa-solid fa-user"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <input type="email" id="signup-email" required />
                    <label for="signup-email">Email</label>
                    <i class="fa-solid fa-envelope"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <input type="password" id="signup-password" required />
                    <label for="signup-password">Password</label>
                    <i class="fa-solid fa-lock"></i>
                </div>

                <div id="signup-success" style="color: #2ed573; text-align: center; font-size: 14px; margin-top: 10px; display: none;">
                    Registration successful! You can now login.
                </div>

                <div class="field-wrapper slide-element">
                    <button class="submit-button" type="submit">Register</button>
                </div>

                <div class="switch-link slide-element">
                    <p>Already have an account? <br /> <a href="#" class="login-trigger">Sign In</a></p>
                </div>
            </form>
        </div>

        <!-- Welcome Section (Signup) -->
        <div class="welcome-section signup">
            <h2 class="slide-element">WELCOME!</h2>
        </div>
    </div>
    
    <div class="footer">
        <p>Made with ❤️ by <a href="#" target="_blank">Jaipur Team</a></p>
    </div>

    <script>
        // Your style.js content
        {js_content}
        
        // Additional script to ensure animations work in Streamlit iframe
        document.addEventListener('DOMContentLoaded', function() {{
            const authWrapper = document.querySelector('.auth-wrapper');
            const registerTrigger = document.querySelector('.register-trigger');
            const loginTrigger = document.querySelector('.login-trigger');
            
            if(registerTrigger) {{
                registerTrigger.addEventListener('click', function(e) {{
                    e.preventDefault();
                    authWrapper.classList.add('toggled');
                }});
            }}
            
            if(loginTrigger) {{
                loginTrigger.addEventListener('click', function(e) {{
                    e.preventDefault();
                    authWrapper.classList.remove('toggled');
                }});
            }}
            
            // Handle form submissions
            const loginForm = document.getElementById('login-form');
            const signupForm = document.getElementById('signup-form');
            const loginError = document.getElementById('login-error');
            const signupSuccess = document.getElementById('signup-success');
            
      if (loginForm) {{
         loginForm.addEventListener('submit', async function (e) {{
        e.preventDefault();        
        const rawEmail = document.getElementById('login-username').value.trim();
        const rawPassword = document.getElementById('login-password').value.trim();
     const secretKey = "ABCDF1232EYSDBSDHDHMVHSJNDHSN123"; // 32 chars
     const iv = CryptoJS.enc.Utf8.parse("1234567890123456"); // 16 bytes IV
     const key = CryptoJS.enc.Utf8.parse(secretKey);

const encryptedEmail = CryptoJS.AES.encrypt(rawEmail,key,
    {{
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }}
).toString();

const encryptedPassword = CryptoJS.AES.encrypt(
    rawPassword,
    key,
    {{
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }}
).toString();
        


        loginError.style.display = "none";
        try {{
            const response = await fetch("{API_BASE_URL}/Auth/login", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{
                    Email:encryptedEmail,
                    Password:encryptedPassword 
                }})
            }});
            if (response.ok) {{
                const data = await response.json();
                if (data.token) {{               
                    window.location.href = "/?token=" + encodeURIComponent(data.token);
                }} else {{
                    loginError.style.display = "block";
                }}

            }} else {{
                loginError.style.display = "block";
            }}

          }} catch (error) {{
            loginError.style.display = "block";
         }}
       }});
   }}
 
if (signupForm) {{
    signupForm.addEventListener('submit', async function (e) {{
        e.preventDefault();

        const username = document.getElementById('signup-username').value.trim();
        const email = document.getElementById('signup-email').value.trim();
        const password = document.getElementById('signup-password').value.trim();
        const secretKey = "ABCDF1232EYSDBSDHDHMVHSJNDHSN123"; 
        const iv = CryptoJS.enc.Utf8.parse("1234567890123456");
        const key = CryptoJS.enc.Utf8.parse(secretKey);

const encryptedEmail = CryptoJS.AES.encrypt(email, key, {{
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
}}).toString();

const encryptedPassword = CryptoJS.AES.encrypt(password, key, {{
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
}}).toString();

const encryptedUsername = CryptoJS.AES.encrypt(username, key, {{
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
}}).toString();



        signupSuccess.style.display = "none";

        try {{
            const response = await fetch("https://localhost:7047/api/Auth/register", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{
                    Username: encryptedUsername,
                    Email: encryptedEmail,
                    Password: encryptedPassword
                }})
            }});

            if (response.ok) {{
                signupSuccess.innerText = "Registration successful!";
                signupSuccess.style.display = "block";
            }} else {{
                signupSuccess.innerText = "Registration failed!";
                signupSuccess.style.display = "block";
            }}

        }} catch (error) {{
            signupSuccess.innerText = "Server error!";
            signupSuccess.style.display = "block";
        }}
    }});
}}



}});
    </script>
</body>
</html>
"""

# Handle message from iframe
st_html(page_html, height=700, scrolling=False)
