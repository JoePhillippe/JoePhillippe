"""
═══════════════════════════════════════════════════════════════════════════
    NETWORKING TUTORS - AUTHENTICATED WEB APPLICATION FOR RENDER
═══════════════════════════════════════════════════════════════════════════

Password-protected web application with all 4 agents.
Perfect for Render deployment with authentication.

ENVIRONMENT VARIABLES (Set in Render):
- ANTHROPIC_API_KEY: Your Anthropic API key
- APP_USERNAME: Login username (you choose)
- APP_PASSWORD: Login password (you choose)

ROUTES:
/login         → Login page
/logout        → Logout
/              → Main menu (requires login)
/agent1        → Basic Subnetting (requires login)
/agent2        → Custom Subnet Masks (requires login)
/agent3        → Subnet Ranges (requires login)
/agent4        → VLSM (requires login)

═══════════════════════════════════════════════════════════════════════════
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from anthropic import Anthropic
from functools import wraps
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Authentication credentials from environment variables
APP_USERNAME = os.environ.get('APP_USERNAME', 'admin')
APP_PASSWORD = os.environ.get('APP_PASSWORD', 'password123')

# API client
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'YOUR_KEY_HERE')
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ═══════════════════════════════════════════════════════════════════════════
# AUTHENTICATION DECORATOR
# ═══════════════════════════════════════════════════════════════════════════

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ═══════════════════════════════════════════════════════════════════════════
# LOGIN/LOGOUT ROUTES
# ═══════════════════════════════════════════════════════════════════════════

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - Networking Tutors</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .login-container {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus,
        input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #888;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🌐 Networking Tutors</h1>
        <p class="subtitle">Please login to continue</p>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        
        <div class="footer">
            Cisco Subnetting AI Tutor Suite
        </div>
    </div>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == APP_USERNAME and password == APP_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"
    
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/logout')
def logout():
    """Logout and redirect to login"""
    session.clear()
    return redirect(url_for('login'))

# ═══════════════════════════════════════════════════════════════════════════
# MAIN MENU (PROTECTED)
# ═══════════════════════════════════════════════════════════════════════════

MENU_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Networking Tutor Suite</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .top-bar {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }
        .logout-btn {
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background 0.3s;
        }
        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .header {
            background: white;
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        .header h1 { color: #667eea; font-size: 3em; margin-bottom: 20px; }
        .header p { color: #666; font-size: 1.3em; }
        .welcome {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 15px;
            font-size: 0.9em;
        }
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }
        .agent-card {
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.2);
            transition: all 0.3s;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .agent-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .agent-number {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .agent-title { font-size: 1.8em; font-weight: 700; margin-bottom: 15px; color: #333; }
        .agent-description { color: #666; line-height: 1.6; font-size: 1.05em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="top-bar">
            <a href="/logout" class="logout-btn">Logout</a>
        </div>
        
        <div class="header">
            <h1>🌐 Networking Tutor Suite</h1>
            <p>Master Cisco Subnetting with AI-Powered Mentoring</p>
            <div class="welcome">Welcome, {{ username }}!</div>
        </div>
        
        <div class="agents-grid">
            <a href="/agent1" class="agent-card">
                <div class="agent-number">1</div>
                <div class="agent-title">Basic Subnetting</div>
                <div class="agent-description">
                    Binary conversion, IP address classes, and fundamental subnetting concepts. 80 practice questions.
                </div>
            </a>
            <a href="/agent2" class="agent-card">
                <div class="agent-number">2</div>
                <div class="agent-title">Custom Subnet Masks</div>
                <div class="agent-description">
                    Calculate subnet bits, host bits, and custom subnet masks. 6 comprehensive problems.
                </div>
            </a>
            <a href="/agent3" class="agent-card">
                <div class="agent-number">3</div>
                <div class="agent-title">Subnet Ranges</div>
                <div class="agent-description">
                    Master subnet ranges, broadcast addresses, and assignable IP ranges. 6 detailed problems.
                </div>
            </a>
            <a href="/agent4" class="agent-card">
                <div class="agent-number">4</div>
                <div class="agent-title">VLSM</div>
                <div class="agent-description">
                    Apply Variable Length Subnet Masking to real-world network design scenarios.
                </div>
            </a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
@login_required
def home():
    """Main menu - requires login"""
    return render_template_string(MENU_HTML, username=session.get('username', 'User'))

# ═══════════════════════════════════════════════════════════════════════════
# AGENT ROUTES (ALL PROTECTED)
# ═══════════════════════════════════════════════════════════════════════════

# Note: The actual agent implementations would go here
# For now, showing the structure with placeholders

@app.route('/agent1')
@login_required
def agent1_home():
    """Agent 1: Basic Subnetting"""
    return """
    <html>
    <head><title>Agent 1: Basic Subnetting</title></head>
    <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
        <h1 style="color: #667eea;">Agent 1: Basic Subnetting</h1>
        <p style="font-size: 1.2em;">Full agent integration in progress...</p>
        <p><a href="/" style="color: #667eea;">← Back to Menu</a> | <a href="/logout" style="color: #667eea;">Logout</a></p>
    </body>
    </html>
    """

@app.route('/agent2')
@login_required
def agent2_home():
    """Agent 2: Custom Subnet Masks"""
    return """
    <html>
    <head><title>Agent 2: Custom Subnet Masks</title></head>
    <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
        <h1 style="color: #667eea;">Agent 2: Custom Subnet Masks</h1>
        <p style="font-size: 1.2em;">Full agent integration in progress...</p>
        <p><a href="/" style="color: #667eea;">← Back to Menu</a> | <a href="/logout" style="color: #667eea;">Logout</a></p>
    </body>
    </html>
    """

@app.route('/agent3')
@login_required
def agent3_home():
    """Agent 3: Subnet Ranges"""
    return """
    <html>
    <head><title>Agent 3: Subnet Ranges</title></head>
    <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
        <h1 style="color: #667eea;">Agent 3: Subnet Ranges</h1>
        <p style="font-size: 1.2em;">Full agent integration in progress...</p>
        <p><a href="/" style="color: #667eea;">← Back to Menu</a> | <a href="/logout" style="color: #667eea;">Logout</a></p>
    </body>
    </html>
    """

@app.route('/agent4')
@login_required
def agent4_home():
    """Agent 4: VLSM"""
    return """
    <html>
    <head><title>Agent 4: VLSM</title></head>
    <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
        <h1 style="color: #667eea;">Agent 4: VLSM</h1>
        <p style="font-size: 1.2em;">Full agent integration in progress...</p>
        <p><a href="/" style="color: #667eea;">← Back to Menu</a> | <a href="/logout" style="color: #667eea;">Logout</a></p>
    </body>
    </html>
    """

# ═══════════════════════════════════════════════════════════════════════════
# HEALTH CHECK (PUBLIC - for Render monitoring)
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/health')
def health():
    """Health check endpoint - no authentication required"""
    return jsonify({"status": "healthy", "agents": 4}), 200

# ═══════════════════════════════════════════════════════════════════════════
# RUN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
