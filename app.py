from flask import Flask, request, redirect, url_for, session, flash, render_template_string, jsonify
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'rizzos-ai-secure-key-2024')

# OpenAI Configuration for Coey AI Assistant
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# 3-Part Admin Authentication
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'rizzos-admin')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@rizzosai.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'SecureAdmin2024!')

# Data Storage Files
CUSTOMERS_FILE = 'customers.json'
BANNED_USERS_FILE = 'banned_users.json'
CHAT_MEMORY_FILE = 'chat_memory.json'

def load_customers():
    """Load customers from JSON file"""
    try:
        with open(CUSTOMERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_customers(customers):
    """Save customers to JSON file"""
    with open(CUSTOMERS_FILE, 'w') as f:
        json.dump(customers, f, indent=2)

def load_banned_users():
    """Load banned users from JSON file"""
    try:
        with open(BANNED_USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_banned_users(banned_users):
    """Save banned users to JSON file"""
    with open(BANNED_USERS_FILE, 'w') as f:
        json.dump(banned_users, f, indent=2)

def load_chat_memory():
    """Load chat conversation memory"""
    try:
        with open(CHAT_MEMORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_chat_memory(memory):
    """Save chat conversation memory"""
    with open(CHAT_MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def get_openai_response(messages, max_tokens=800, temperature=0.3):
    """Get response from OpenAI GPT-4 for Coey AI"""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        return "I'm currently not configured with an API key. Please contact support for assistance."
    
    try:
        import openai
        # Use the older OpenAI library syntax (v0.28.1)
        openai.api_key = OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except ImportError:
        return "OpenAI library is not installed. Please contact support."
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return "Invalid API key configuration. Please contact support."
        elif "model" in error_msg.lower() or "not found" in error_msg.lower():
            return "Model access issue. Please contact support."
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            return "Network connectivity issue. Please try again later."
        else:
            return f"Technical difficulties: {error_msg[:100]}..."

# Elite Package System - Domain Investing Guides
PACKAGES = {
    'starter': {
        'name': 'Starter Package',
        'price': '$29.99',
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup']
    },
    'pro': {
        'name': 'Pro Package', 
        'price': '$99.99',
        'guides': [
            'Domain Basics', 'First Purchase Guide', 'Quick Setup', 
            'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 
            'Market Analysis', 'Negotiation Tactics'
        ]
    },
    'elite': {
        'name': 'Elite Package',
        'price': '$499.99', 
        'guides': [
            'Domain Basics', 'First Purchase Guide', 'Quick Setup', 
            'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 
            'Market Analysis', 'Negotiation Tactics', 'Empire Building', 
            'Advanced Analytics', 'Premium Tools', 'Elite Strategies', 'Insider Secrets'
        ]
    },
    'empire': {
        'name': 'Empire Package',
        'price': '$999.99',
        'guides': [
            'Domain Basics', 'First Purchase Guide', 'Quick Setup',
            'Advanced Strategies', 'Investment Guide', 'Portfolio Building',
            'Market Analysis', 'Negotiation Tactics', 'Empire Building',
            'Advanced Analytics', 'Premium Tools', 'Elite Strategies',
            'Insider Secrets', 'Master Class', 'Personal Coaching', 'Exclusive Networks'
        ]
    },
    'empire-trial': {
        'name': 'Empire Trial',
        'price': 'Free Trial',
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup'],
        'trial': True,
        'conversion_target': 'empire',
        'limit': 3
    }
}

def get_user_package(username):
    """Get user's package from customers database"""
    # Admin gets access to all packages (Empire level)
    if username == ADMIN_USERNAME:
        return 'empire'
    customers = load_customers()
    return customers.get(username, {}).get('package', 'starter')

def get_package_guides(username):
    """Get available guides for user's package"""
    # Admin gets access to all guides (Empire level)
    if username == ADMIN_USERNAME:
        return PACKAGES['empire']['guides']
    package = get_user_package(username)
    if package in PACKAGES:
        return PACKAGES[package]['guides']
    return PACKAGES['starter']['guides']

def is_banned_user(username):
    """Check if user is banned"""
    banned_users = load_banned_users()
    return username in banned_users

@app.route('/')
def dashboard():
    """Main dashboard - beautiful modern design"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Check if user is banned
    if is_banned_user(username):
        session.clear()
        flash('Your account has been suspended. Please contact support.', 'error')
        return redirect(url_for('login'))
    
    package = get_user_package(username)
    available_guides = get_package_guides(username)
    
    # Trial status for empire-trial users
    trial_status = ""
    if package == 'empire-trial':
        customers = load_customers()
        guides_accessed = customers.get(username, {}).get('guides_accessed', 0)
        remaining = PACKAGES['empire-trial']['limit'] - guides_accessed
        if remaining <= 0:
            trial_status = f"""
            <div class="trial-expired">
                <h3>🚀 Trial Complete! Ready to Unlock Everything?</h3>
                <p>You've explored {PACKAGES['empire-trial']['limit']} guides. Upgrade to Elite Package for unlimited access to all {len(PACKAGES['elite']['guides'])} premium guides!</p>
                <a href="https://buy.stripe.com/14AbJ299E1os2Jp8Td1oI0h" class="upgrade-btn">Upgrade to Elite Package - $499.99</a>
            </div>
            """
        else:
            trial_status = f"""
            <div class="trial-status">
                <p>🎯 <strong>Empire Trial:</strong> {remaining} guides remaining</p>
            </div>
            """
    
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rizzos AI - Domain Empire Backoffice</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .header {{ 
                background: rgba(255,255,255,0.95); 
                border-radius: 15px; 
                padding: 20px; 
                margin-bottom: 20px; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }}
            .welcome {{ text-align: center; }}
            .welcome h1 {{ color: #4a5568; font-size: 2.5em; margin-bottom: 10px; }}
            .welcome p {{ color: #718096; font-size: 1.1em; }}
            .user-info {{ 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-top: 15px; 
                padding-top: 15px; 
                border-top: 1px solid #e2e8f0;
            }}
            .package-badge {{ 
                background: linear-gradient(135deg, #ff6b6b, #feca57); 
                color: white; 
                padding: 8px 16px; 
                border-radius: 20px; 
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
            }}
            .logout-btn {{ 
                background: #e53e3e; 
                color: white; 
                padding: 8px 16px; 
                border: none; 
                border-radius: 8px; 
                text-decoration: none; 
                transition: all 0.3s;
            }}
            .logout-btn:hover {{ background: #c53030; }}
            .main-content {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 20px; 
                margin-bottom: 20px;
            }}
            .section {{ 
                background: rgba(255,255,255,0.95); 
                border-radius: 15px; 
                padding: 25px; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }}
            .section h2 {{ color: #4a5568; margin-bottom: 15px; font-size: 1.5em; }}
            .guides-grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 15px; 
                margin-top: 15px;
            }}
            .guide-card {{ 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center; 
                cursor: pointer; 
                transition: all 0.3s;
                text-decoration: none;
            }}
            .guide-card:hover {{ 
                transform: translateY(-5px); 
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                color: white;
                text-decoration: none;
            }}
            .coey-section {{ grid-column: span 2; }}
            .coey-btn {{ 
                background: linear-gradient(135deg, #48bb78, #38a169); 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                font-size: 1.1em; 
                cursor: pointer; 
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
                margin-right: 15px;
            }}
            .coey-btn:hover {{ 
                transform: translateY(-2px); 
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
                color: white;
                text-decoration: none;
            }}
            .trial-status {{ 
                background: linear-gradient(135deg, #feca57, #ff9ff3); 
                color: white; 
                padding: 10px 15px; 
                border-radius: 8px; 
                margin-bottom: 15px; 
                text-align: center;
                font-weight: bold;
            }}
            .trial-expired {{ 
                background: linear-gradient(135deg, #ff6b6b, #feca57); 
                color: white; 
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 15px; 
                text-align: center;
            }}
            .upgrade-btn {{ 
                background: white; 
                color: #ff6b6b; 
                padding: 12px 24px; 
                border-radius: 8px; 
                text-decoration: none; 
                font-weight: bold; 
                display: inline-block; 
                margin-top: 10px;
                transition: all 0.3s;
            }}
            .upgrade-btn:hover {{ transform: translateY(-2px); }}
            @media (max-width: 768px) {{ 
                .main-content {{ grid-template-columns: 1fr; }}
                .coey-section {{ grid-column: span 1; }}
                .guides-grid {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="welcome">
                    <h1>🏆 Rizzos AI Domain Empire</h1>
                    <p>Your gateway to domain investing mastery</p>
                </div>
                <div class="user-info">
                    <div>
                        <strong>Welcome, {username}!</strong>
                        <span class="package-badge">{PACKAGES.get(package, {}).get('name', 'Unknown Package')}</span>
                    </div>
                    <a href="/logout" class="logout-btn">Logout</a>
                </div>
            </div>
            
            {trial_status}
            
            <div class="main-content">
                <div class="section">
                    <h2>📚 Your Guides ({len(available_guides)})</h2>
                    <p>Access your premium domain investing guides</p>
                    <div class="guides-grid">
                        {''.join([f'<a href="/guide/{guide.replace(" ", "-").lower()}" class="guide-card">{guide}</a>' for guide in available_guides])}
                    </div>
                </div>
                
                <div class="section">
                    <h2>⚡ Quick Actions</h2>
                    <p>Essential tools and resources</p>
                    <div style="margin-top: 15px;">
                        <a href="/portfolio" class="coey-btn">📊 Portfolio</a>
                        <a href="/market" class="coey-btn">📈 Market Data</a>
                        <a href="/tools" class="coey-btn">🛠️ Tools</a>
                    </div>
                </div>
                
                <div class="section coey-section">
                    <h2>🤖 Meet Coey - Your AI Domain Advisor</h2>
                    <p>Get personalized domain investing advice from our advanced AI assistant powered by GPT-4</p>
                    <div style="margin-top: 15px;">
                        <a href="/coey" class="coey-btn">💬 Chat with Coey</a>
                        <a href="/coey/onboarding" class="coey-btn">🎯 Onboarding Assistant</a>
                        <a href="/change-password" class="coey-btn">🔑 Change Password</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return dashboard_html

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User and Admin Authentication Login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()  # Only required for admin
        
        # Check if user is banned
        if is_banned_user(username):
            flash('Your account has been suspended. Please contact support.', 'error')
            return redirect(url_for('login'))
        
        # Admin Authentication (requires 3 fields)
        if username == ADMIN_USERNAME:
            if (email == ADMIN_EMAIL and password == ADMIN_PASSWORD):
                session['username'] = username
                session['is_admin'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials. All fields are required for admin access.', 'error')
                return redirect(url_for('login'))
        
        # Regular User Authentication (username + password only)
        customers = load_customers()
        if username in customers and customers[username].get('password') == password:
            session['username'] = username
            session['is_admin'] = False
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password.', 'error')
    
    login_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rizzos AI - Secure Login</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #333;
            }
            .login-container { 
                background: rgba(255,255,255,0.95); 
                border-radius: 20px; 
                padding: 40px; 
                box-shadow: 0 15px 50px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
                width: 100%;
                max-width: 400px;
            }
            .login-header { text-align: center; margin-bottom: 30px; }
            .login-header h1 { color: #4a5568; font-size: 2.2em; margin-bottom: 10px; }
            .login-header p { color: #718096; }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #4a5568; }
            .form-group input { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #e2e8f0; 
                border-radius: 8px; 
                font-size: 16px;
                transition: border-color 0.3s;
            }
            .form-group input:focus { 
                outline: none; 
                border-color: #667eea; 
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .login-btn { 
                width: 100%; 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; 
                padding: 12px; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px; 
                cursor: pointer; 
                transition: all 0.3s;
            }
            .login-btn:hover { 
                transform: translateY(-2px); 
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            }
            .flash-messages { margin-bottom: 20px; }
            .flash-error { 
                background: #fed7d7; 
                color: #c53030; 
                padding: 10px; 
                border-radius: 8px; 
                border-left: 4px solid #e53e3e;
            }
            .security-note {
                margin-top: 20px;
                padding: 15px;
                background: #f7fafc;
                border-radius: 8px;
                border-left: 4px solid #4299e1;
            }
            .security-note h4 { color: #2d3748; margin-bottom: 5px; }
            .security-note p { color: #4a5568; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
                <h1>🏆 Rizzos AI</h1>
                <p>Domain Empire Access Portal</p>
            </div>
            
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    <div class="flash-messages">
                        {% for message in messages %}
                            <div class="flash-error">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <!-- Admin email field (hidden by default) -->
                <div class="form-group" id="admin-email-group" style="display: none;">
                    <label for="email">Admin Email (Required for Admin Login)</label>
                    <input type="email" id="email" name="email">
                </div>
                
                <button type="submit" class="login-btn">Access Domain Empire</button>
            </form>
            
            <div style="text-align: center; margin-top: 15px;">
                <a href="/reset-password" style="color: #667eea; text-decoration: none; font-size: 14px;">
                    🔑 Forgot Password?
                </a>
            </div>
            
            <div class="security-note">
                <h4>🔒 User-Friendly Login</h4>
                <p>Regular users: Just username and password<br>
                Admin: Username, password, and email required</p>
            </div>
            
            <script>
                // Show email field when admin username is detected
                document.getElementById('username').addEventListener('input', function() {
                    const username = this.value.toLowerCase();
                    const emailGroup = document.getElementById('admin-email-group');
                    const emailField = document.getElementById('email');
                    
                    if (username.includes('admin') || username === 'rizzos-admin') {
                        emailGroup.style.display = 'block';
                        emailField.required = true;
                    } else {
                        emailGroup.style.display = 'none';
                        emailField.required = false;
                        emailField.value = '';
                    }
                });
            </script>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(login_html)

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard with Customer Management"""
    if 'username' not in session or not session.get('is_admin', False):
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))
    
    # Load customer data
    customers = load_customers()
    banned_users = load_banned_users()
    
    # Calculate package statistics
    package_counts = {}
    total_revenue = 0
    for customer in customers.values():
        package = customer.get('package', 'starter')
        package_counts[package] = package_counts.get(package, 0) + 1
        
        # Calculate revenue (simplified)
        price_map = {'starter': 29.99, 'pro': 99.99, 'elite': 499.99, 'empire': 999.99}
        if package in price_map:
            total_revenue += price_map[package]
    
    admin_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard - Rizzos AI</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                margin: 0; 
                padding: 20px; 
            }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ 
                background: rgba(255,255,255,0.95); 
                border-radius: 15px; 
                padding: 20px; 
                margin-bottom: 20px; 
                text-align: center; 
            }}
            .stats-grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 20px; 
                margin-bottom: 20px; 
            }}
            .stat-card {{ 
                background: rgba(255,255,255,0.95); 
                border-radius: 10px; 
                padding: 20px; 
                text-align: center; 
            }}
            .stat-number {{ 
                font-size: 2em; 
                font-weight: bold; 
                color: #667eea; 
            }}
            .customers-section {{ 
                background: rgba(255,255,255,0.95); 
                border-radius: 15px; 
                padding: 20px; 
            }}
            .customer-item {{ 
                padding: 10px; 
                border-bottom: 1px solid #eee; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
            }}
            .package-badge {{ 
                padding: 4px 8px; 
                border-radius: 4px; 
                color: white; 
                font-size: 0.8em; 
            }}
            .starter {{ background: #48bb78; }}
            .pro {{ background: #667eea; }}
            .elite {{ background: #ff6b6b; }}
            .empire {{ background: #feca57; color: black; }}
            .empire-trial {{ background: #ff9ff3; }}
            .logout-btn {{ 
                background: #e53e3e; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 8px; 
                text-decoration: none; 
            }}
            .action-buttons {{ margin-top: 15px; }}
            .action-btn {{ 
                background: #667eea; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 6px; 
                text-decoration: none; 
                margin-right: 10px; 
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏆 Admin Dashboard - Rizzos AI</h1>
                <p>Domain Empire Management System</p>
                <p>Welcome, {session['username']} | <a href="/logout" class="logout-btn">Logout</a></p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(customers)}</div>
                    <div>Total Customers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{package_counts.get('elite', 0)}</div>
                    <div>Elite Customers ($499.99)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{package_counts.get('empire', 0)}</div>
                    <div>Empire Customers ($999.99)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${total_revenue:,.2f}</div>
                    <div>Total Revenue</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(banned_users)}</div>
                    <div>Banned Users</div>
                </div>
            </div>
            
            <!-- Quick Admin User Management -->
            <div class="customers-section" style="margin-bottom: 30px;">
                <h2>🔗 Quick Admin User Management</h2>
                <p style="margin-bottom: 15px; color: #666;">Quickly promote users to Empire package or create new admin-linked users</p>
                
                <form method="POST" action="/quick-admin-link" style="display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap;">
                    <input type="text" name="target_username" placeholder="Enter username" required 
                           style="flex: 1; min-width: 200px; padding: 8px; border: 1px solid #ddd; border-radius: 5px;">
                    <button type="submit" name="action" value="promote" 
                            style="background: #28a745; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        👑 Promote to Empire
                    </button>
                    <button type="submit" name="action" value="demote" 
                            style="background: #dc3545; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        📉 Demote to Starter
                    </button>
                </form>
                
                <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; font-size: 12px; color: #666;">
                    <strong>Note:</strong> Promoting creates new users with Empire package access and default password "temppass123" if they don't exist.
                </div>
            </div>
            
            <div class="customers-section">
                <h2>Customer Management</h2>
                <div class="action-buttons">
                    <a href="/admin/export" class="action-btn">📊 Export Data</a>
                    <a href="/admin/analytics" class="action-btn">📈 Analytics</a>
                    <a href="/admin/settings" class="action-btn">⚙️ Settings</a>
                </div>
                <br>
                {''.join([f'''
                <div class="customer-item">
                    <div>
                        <strong>{username}</strong> ({customer.get('email', 'No email')})
                        <br><small>Created: {customer.get('created_at', 'Unknown')[:10]}</small>
                    </div>
                    <div>
                        <span class="package-badge {customer.get('package', 'starter')}">{PACKAGES.get(customer.get('package', 'starter'), {}).get('name', 'Unknown')}</span>
                    </div>
                </div>
                ''' for username, customer in customers.items()]) if customers else '<p>No customers yet.</p>'}
            </div>
        </div>
    </body>
    </html>
    """
    
    return admin_html

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/quick-admin-link', methods=['POST'])
def quick_admin_link():
    """Quick admin user linking - Admin only"""
    if 'username' not in session or not session.get('is_admin'):
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('login'))
    
    target_username = request.form.get('target_username', '').strip()
    action = request.form.get('action', 'promote')  # promote or demote
    
    if not target_username:
        flash('Username is required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Don't allow admin to modify their own account
    if target_username == ADMIN_USERNAME:
        flash('Cannot modify admin account through this interface.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    customers = load_customers()
    
    if action == 'promote':
        # Create or update user with admin-like privileges (Empire package)
        if target_username not in customers:
            # Create new user with Empire package
            customers[target_username] = {
                'password': 'temppass123',  # User should change this
                'email': f'{target_username}@rizzosai.com',
                'package': 'empire',
                'created_at': datetime.now().isoformat(),
                'admin_linked': True,
                'needs_password_change': True
            }
            flash(f'User {target_username} created with Empire package access! Default password: temppass123', 'success')
        else:
            # Upgrade existing user to Empire package
            customers[target_username]['package'] = 'empire'
            customers[target_username]['admin_linked'] = True
            flash(f'User {target_username} promoted to Empire package!', 'success')
    
    elif action == 'demote':
        if target_username in customers:
            customers[target_username]['package'] = 'starter'
            customers[target_username]['admin_linked'] = False
            flash(f'User {target_username} demoted to Starter package.', 'info')
        else:
            flash(f'User {target_username} not found.', 'error')
            return redirect(url_for('admin_dashboard'))
    
    save_customers(customers)
    return redirect(url_for('admin_dashboard'))

@app.route('/owner-access')
def owner_access():
    """Special route for owner to get Elite package access instantly"""
    # Auto-create owner account with Elite package
    customers = load_customers()
    
    owner_username = "rizzosowner"
    owner_password = "empire2024!"
    
    customers[owner_username] = {
        'password': owner_password,
        'email': 'owner@rizzosai.com',
        'package': 'elite',
        'created_at': datetime.now().isoformat(),
        'session_id': 'owner_direct_access',
        'guides_accessed': 0,
        'owner': True
    }
    
    save_customers(customers)
    
    # Auto-login the owner
    session['username'] = owner_username
    session['is_admin'] = False
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Owner Access Created - Rizzos AI</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
            }}
            .success-box {{ 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                text-align: center; 
                max-width: 500px; 
                box-shadow: 0 15px 50px rgba(0,0,0,0.2);
            }}
            .access-btn {{ 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                text-decoration: none; 
                display: inline-block; 
                margin-top: 20px; 
                transition: all 0.3s;
            }}
            .access-btn:hover {{ 
                transform: translateY(-2px); 
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            }}
            .credentials {{ 
                background: #f7fafc; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 15px 0; 
            }}
        </style>
    </head>
    <body>
        <div class="success-box">
            <h1>🏆 Owner Access Created Successfully!</h1>
            <div class="credentials">
                <p><strong>Username:</strong> {owner_username}</p>
                <p><strong>Password:</strong> {owner_password}</p>
                <p><strong>Package:</strong> Elite Package ($499.99)</p>
                <p><strong>Guides Available:</strong> {len(PACKAGES['elite']['guides'])}</p>
            </div>
            <p>You now have access to all Elite guides and premium features!</p>
            <a href="/" class="access-btn">Access Your Elite Dashboard</a>
        </div>
    </body>
    </html>
    """

@app.route('/coey')
def coey_chat():
    """Coey AI Chat Interface"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Check if user is banned
    if is_banned_user(username):
        session.clear()
        flash('Your account has been suspended. Please contact support.', 'error')
        return redirect(url_for('login'))
    
    chat_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coey AI - Domain Advisor</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                margin: 0; 
                padding: 20px; 
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 15px; 
                padding: 20px; 
                box-shadow: 0 15px 50px rgba(0,0,0,0.2);
            }
            .header { text-align: center; margin-bottom: 20px; }
            .header h1 { color: #4a5568; }
            .back-btn { 
                background: #e2e8f0; 
                color: #4a5568; 
                padding: 8px 16px; 
                border-radius: 8px; 
                text-decoration: none; 
                display: inline-block;
                margin-bottom: 20px;
            }
            .chat-area { 
                border: 2px solid #e2e8f0; 
                border-radius: 10px; 
                height: 400px; 
                overflow-y: auto; 
                padding: 15px; 
                margin-bottom: 15px;
                background: #f7fafc;
            }
            .chat-input-area { display: flex; gap: 10px; }
            .chat-input { 
                flex: 1; 
                padding: 10px; 
                border: 2px solid #e2e8f0; 
                border-radius: 8px; 
                font-size: 16px;
            }
            .send-btn { 
                background: linear-gradient(135deg, #48bb78, #38a169); 
                color: white; 
                padding: 10px 20px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
            }
            .message { 
                margin-bottom: 15px; 
                padding: 10px; 
                border-radius: 8px; 
            }
            .user-message { 
                background: #667eea; 
                color: white; 
                margin-left: 20%; 
            }
            .coey-message { 
                background: #e2e8f0; 
                color: #2d3748; 
                margin-right: 20%; 
            }
        </style>
        <script>
            async function sendMessage() {
                const input = document.getElementById('chatInput');
                const message = input.value.trim();
                if (!message) return;
                
                const chatArea = document.getElementById('chatArea');
                
                // Add user message
                chatArea.innerHTML += `<div class="message user-message">You: ${message}</div>`;
                input.value = '';
                
                // Add loading message
                chatArea.innerHTML += `<div class="message coey-message" id="loading">Coey: Thinking...</div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
                
                try {
                    const response = await fetch('/coey/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    document.getElementById('loading').innerHTML = `Coey: ${data.response}`;
                } catch (error) {
                    document.getElementById('loading').innerHTML = `Coey: Sorry, I'm having technical difficulties. Please try again.`;
                }
                
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('chatInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            });
        </script>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            <div class="header">
                <h1>🤖 Coey AI - Your Domain Investment Advisor</h1>
                <p>Powered by GPT-4 | Ask me anything about domain investing!</p>
            </div>
            
            <div id="chatArea" class="chat-area">
                <div class="message coey-message">
                    Coey: Hello! I'm Coey, your AI domain investment advisor. I'm here to help you build a successful domain portfolio. What would you like to know about domain investing?
                </div>
            </div>
            
            <div class="chat-input-area">
                <input type="text" id="chatInput" class="chat-input" placeholder="Ask me about domain investing strategies, market trends, portfolio building...">
                <button onclick="sendMessage()" class="send-btn">Send</button>
            </div>
        </div>
    </body>
    </html>
    """
    
    return chat_html

@app.route('/coey/chat', methods=['POST'])
def coey_chat_api():
    """Handle chat messages to Coey AI"""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Create system message for Coey
    system_message = """You are Coey, an expert AI domain investing advisor for Rizzos AI. You help users build successful domain portfolios with practical, actionable advice. 

Key areas you specialize in:
- Domain valuation and appraisal
- Market trends and opportunities
- Portfolio diversification strategies
- Buying and selling techniques
- Legal considerations
- Investment timing
- Niche market identification
- Brand development potential

Always provide specific, actionable advice. Be encouraging but realistic about domain investing challenges and opportunities."""
    
    # Get response from OpenAI
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    coey_response = get_openai_response(messages)
    
    # Save conversation to memory (optional)
    memory = load_chat_memory()
    username = session['username']
    if username not in memory:
        memory[username] = []
    
    memory[username].append({
        'user': user_message,
        'coey': coey_response,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last 50 conversations per user
    if len(memory[username]) > 50:
        memory[username] = memory[username][-50:]
    
    save_chat_memory(memory)
    
    return jsonify({'response': coey_response})

# Additional utility routes
@app.route('/guide/<guide_name>')
def view_guide(guide_name):
    """View individual guide content"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    available_guides = get_package_guides(username)
    
    # Convert URL format back to guide name
    guide_display_name = guide_name.replace('-', ' ').title()
    
    if guide_display_name not in available_guides:
        flash('You do not have access to this guide. Please upgrade your package.', 'error')
        return redirect(url_for('dashboard'))
    
    # Comprehensive guide content database
    guide_contents = {
        'Domain Basics': """
        <h2>🌐 Domain Basics - Your Foundation to Success</h2>
        
        <h3>What Are Domains?</h3>
        <p>A domain name is your digital real estate on the internet. Just like prime real estate locations, premium domains can be incredibly valuable assets that appreciate over time.</p>
        
        <h3>Why Domain Investing Works</h3>
        <ul>
            <li><strong>Scarcity:</strong> There's only one of each domain name</li>
            <li><strong>Demand:</strong> Every business needs an online presence</li>
            <li><strong>Branding Value:</strong> The right domain can make or break a brand</li>
            <li><strong>Type-in Traffic:</strong> People naturally type certain domains</li>
        </ul>
        
        <h3>Types of Valuable Domains</h3>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <p><strong>🏆 Exact Match Domains (EMDs):</strong> Insurance.com, Cars.com</p>
            <p><strong>💰 Short Domains:</strong> 1-3 characters (.com, .net)</p>
            <p><strong>🏢 Brandable Domains:</strong> Google.com, Spotify.com</p>
            <p><strong>🌍 Geographic Domains:</strong> NewYork.com, London.org</p>
            <p><strong>💊 Industry Domains:</strong> Crypto.com, Health.net</p>
        </div>
        
        <h3>Domain Extensions Priority</h3>
        <ol>
            <li><strong>.com</strong> - The gold standard (90% of investment focus)</li>
            <li><strong>.net</strong> - Second choice for tech/network businesses</li>
            <li><strong>.org</strong> - For organizations and nonprofits</li>
            <li><strong>Country TLDs</strong> - .co.uk, .de, .ca for local markets</li>
        </ol>
        
        <h3>Key Success Metrics</h3>
        <ul>
            <li>Age of domain (older = more valuable)</li>
            <li>Search volume for keywords</li>
            <li>Brandability and memorability</li>
            <li>Commercial intent of the keyword</li>
            <li>Type-in traffic potential</li>
        </ul>
        
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;">
            <strong>💡 Pro Tip:</strong> Start with exact match domains in industries you understand. If you know real estate, look for RealEstate[City].com domains.
        </div>
        """,
        
        'First Purchase Guide': """
        <h2>🎯 First Purchase Guide - Your First Domain Investment</h2>
        
        <h3>Step 1: Set Your Budget</h3>
        <p>For beginners, start with a budget of $100-$500 per domain. This allows you to:</p>
        <ul>
            <li>Learn without major financial risk</li>
            <li>Test different domain types</li>
            <li>Understand market dynamics</li>
            <li>Build confidence in your decisions</li>
        </ul>
        
        <h3>Step 2: Research Tools You Need</h3>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🔍 Keyword Research:</strong></p>
            <ul>
                <li>Google Keyword Planner (free)</li>
                <li>Ahrefs or SEMrush (paid)</li>
                <li>Ubersuggest (freemium)</li>
            </ul>
            
            <p><strong>📊 Domain Valuation:</strong></p>
            <ul>
                <li>Estibot.com</li>
                <li>GoDaddy Domain Appraisal</li>
                <li>NameWorth.com</li>
            </ul>
            
            <p><strong>🏪 Marketplaces:</strong></p>
            <ul>
                <li>Sedo.com (largest marketplace)</li>
                <li>Flippa.com (auctions)</li>
                <li>Afternic.com (premium domains)</li>
                <li>Dan.com (modern interface)</li>
            </ul>
        </div>
        
        <h3>Step 3: Find Your First Domain</h3>
        <p><strong>Look for these characteristics:</strong></p>
        <ol>
            <li><strong>Clear commercial intent</strong> - LosAngelesPlumber.com</li>
            <li><strong>High search volume</strong> - 1,000+ monthly searches</li>
            <li><strong>Short and memorable</strong> - Under 20 characters</li>
            <li><strong>.com extension</strong> - Always prioritize this</li>
            <li><strong>No hyphens or numbers</strong> - Harder to remember and type</li>
        </ol>
        
        <h3>Step 4: Due Diligence Checklist</h3>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
            <p><strong>⚠️ Before You Buy - Verify These:</strong></p>
            <ul>
                <li>✅ Domain history (use Wayback Machine)</li>
                <li>✅ No trademark conflicts (search USPTO database)</li>
                <li>✅ Clean backlink profile (use Ahrefs)</li>
                <li>✅ Not banned from Google (search "site:domainname.com")</li>
                <li>✅ Registrar reputation and transfer policies</li>
            </ul>
        </div>
        
        <h3>Step 5: Negotiation Strategy</h3>
        <p><strong>Start with 30-50% of asking price:</strong></p>
        <ul>
            <li>Be polite and professional</li>
            <li>Explain your intended use</li>
            <li>Show genuine interest</li>
            <li>Be prepared to walk away</li>
            <li>Use escrow services for transactions over $1,000</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>🎉 Success Framework:</strong> Your first purchase should be in a niche you understand. If you're a dentist, look for dental-related domains. Knowledge = Power = Profit.
        </div>
        """,
        
        'Quick Setup': """
        <h2>⚡ Quick Setup - Get Started in 24 Hours</h2>
        
        <h3>Hour 1-2: Account Setup</h3>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🏪 Create Marketplace Accounts:</strong></p>
            <ol>
                <li><strong>Sedo.com</strong> - Main marketplace (free)</li>
                <li><strong>GoDaddy Auctions</strong> - Daily expired domain auctions</li>
                <li><strong>Flippa.com</strong> - Website and domain auctions</li>
                <li><strong>Dan.com</strong> - Premium domain marketplace</li>
            </ol>
        </div>
        
        <h3>Hour 3-4: Research Tools Setup</h3>
        <p><strong>🔧 Essential Tools Configuration:</strong></p>
        <ul>
            <li><strong>Google Keyword Planner:</strong> Set up Google Ads account (free)</li>
            <li><strong>Namecheap Domain Search:</strong> Quick availability checks</li>
            <li><strong>Whois Lookup Tools:</strong> Domain registration info</li>
            <li><strong>Wayback Machine:</strong> Check domain history</li>
        </ul>
        
        <h3>Hour 5-8: Market Research</h3>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>📊 Find Your Niche - Choose ONE to start:</strong></p>
            <ul>
                <li><strong>Local Services:</strong> [City] + [Service] (e.g., MiamiPlumbing.com)</li>
                <li><strong>E-commerce:</strong> Product category domains</li>
                <li><strong>Cryptocurrency:</strong> Crypto + [Term] combinations</li>
                <li><strong>Health/Wellness:</strong> Medical and fitness terms</li>
                <li><strong>Technology:</strong> AI, Software, App related domains</li>
            </ul>
        </div>
        
        <h3>Hour 9-16: First Domain Search</h3>
        <p><strong>🎯 Systematic Approach:</strong></p>
        <ol>
            <li><strong>Keyword Research:</strong> Find 20 keywords in your chosen niche</li>
            <li><strong>Domain Combinations:</strong> Create 50+ domain variations</li>
            <li><strong>Availability Check:</strong> See what's available vs. taken</li>
            <li><strong>Expired Domain Search:</strong> Check recent expires in your niche</li>
            <li><strong>Auction Monitoring:</strong> Set up alerts for relevant auctions</li>
        </ol>
        
        <h3>Hour 17-20: Valuation & Selection</h3>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>💰 Quick Valuation Method:</strong></p>
            <ul>
                <li><strong>Search Volume × $0.50</strong> = Base value (monthly searches)</li>
                <li><strong>Commercial Intent Bonus:</strong> +50% for buying keywords</li>
                <li><strong>Exact Match Bonus:</strong> +100% for exact keyword match</li>
                <li><strong>.com Bonus:</strong> +200% over other extensions</li>
            </ul>
            <p><strong>Example:</strong> "Miami Dentist" = 2,000 searches × $0.50 = $1,000 base + commercial intent (+$500) + exact match (+$1,000) + .com (+$2,000) = $4,500 estimated value</p>
        </div>
        
        <h3>Hour 21-24: Make Your Move</h3>
        <p><strong>🚀 Time to Act:</strong></p>
        <ul>
            <li>Select your top 3 domain candidates</li>
            <li>Set maximum bid/offer amounts</li>
            <li>Contact sellers or place auction bids</li>
            <li>Set up domain parking (if purchased)</li>
            <li>Begin building your portfolio tracking system</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>✅ 24-Hour Goal:</strong> Have at least 3 serious domain opportunities identified and 1 offer submitted. Speed + Research = Success in domain investing.
        </div>
        """,
        
        'Advanced Strategies': """
        <h2>🚀 Advanced Strategies - Scale Your Domain Empire</h2>
        
        <h3>Strategy 1: Expired Domain Goldmine</h3>
        <p>Expired domains are pre-owned domains that weren't renewed. They often have existing SEO value, backlinks, and type-in traffic.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🏆 What Makes Expired Domains Valuable:</strong></p>
            <ul>
                <li><strong>Existing Backlinks:</strong> SEO authority already built</li>
                <li><strong>Domain Age:</strong> Older domains rank better</li>
                <li><strong>Type-in Traffic:</strong> People already know the domain</li>
                <li><strong>Brand Recognition:</strong> Established online presence</li>
            </ul>
        </div>
        
        <h3>Strategy 2: Geographic Domain Domination</h3>
        <p>Control entire geographic markets by acquiring city + service combinations.</p>
        
        <p><strong>📍 Geographic Strategy Framework:</strong></p>
        <ol>
            <li><strong>Choose a profitable service:</strong> Plumbing, Dental, Legal, Real Estate</li>
            <li><strong>Target growing cities:</strong> Austin, Denver, Nashville, Phoenix</li>
            <li><strong>Acquire variations:</strong></li>
            <ul>
                <li>[City][Service].com</li>
                <li>[City][Service]s.com</li>
                <li>[Service][City].com</li>
                <li>Best[Service][City].com</li>
            </ul>
        </ol>
        
        <h3>Strategy 3: Industry Trend Surfing</h3>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>🌊 Ride the Wave - Current Hot Industries:</strong></p>
            <ul>
                <li><strong>AI/Machine Learning:</strong> AI[Industry].com</li>
                <li><strong>Cryptocurrency:</strong> [Coin]Exchange.com</li>
                <li><strong>Remote Work:</strong> Remote[JobType].com</li>
                <li><strong>Sustainability:</strong> Green[Industry].com</li>
                <li><strong>Telehealth:</strong> Online[MedicalService].com</li>
            </ul>
        </div>
        
        <h3>Strategy 4: Premium Domain Acquisition</h3>
        <p><strong>💎 Going After $10K+ Domains:</strong></p>
        <ul>
            <li><strong>Payment Plans:</strong> Negotiate monthly payments</li>
            <li><strong>Joint Ventures:</strong> Partner with others to split costs</li>
            <li><strong>Development Deals:</strong> Offer to develop the domain</li>
            <li><strong>Revenue Sharing:</strong> Propose ongoing revenue splits</li>
        </ul>
        
        <h3>Strategy 5: Portfolio Syndication</h3>
        <p>Create themed domain portfolios that sell as packages.</p>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>📦 Portfolio Package Examples:</strong></p>
            <ul>
                <li><strong>State Law Package:</strong> [State]Lawyer.com × 50 states</li>
                <li><strong>Crypto Trading Suite:</strong> 20 crypto-related domains</li>
                <li><strong>Health & Wellness Bundle:</strong> 30 health service domains</li>
                <li><strong>E-commerce Category:</strong> Product-specific domain collections</li>
            </ul>
        </div>
        
        <h3>Strategy 6: International Expansion</h3>
        <p><strong>🌍 Global Domain Strategy:</strong></p>
        <ul>
            <li><strong>Country Code TLDs:</strong> .co.uk, .de, .au, .ca</li>
            <li><strong>Language Variations:</strong> English keywords in other TLDs</li>
            <li><strong>Cultural Adaptation:</strong> Local business naming conventions</li>
            <li><strong>Market Research:</strong> Understand local domain preferences</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>💡 Advanced Pro Tip:</strong> The most successful domain investors focus on becoming experts in 2-3 specific niches rather than trying to master everything. Deep knowledge = Higher profits.
        </div>
        """,
        
        'Investment Guide': """
        <h2>💰 Investment Guide - Building Wealth Through Domains</h2>
        
        <h3>Investment Philosophy</h3>
        <p>Domain investing is like real estate - location, timing, and market knowledge determine success. Unlike stocks, domains are unique assets that can't be duplicated.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🎯 Core Investment Principles:</strong></p>
            <ol>
                <li><strong>Scarcity Creates Value:</strong> Only one of each domain exists</li>
                <li><strong>Utility Drives Demand:</strong> Businesses need memorable domains</li>
                <li><strong>Brand Power:</strong> Great domains become brands themselves</li>
                <li><strong>Digital Real Estate:</strong> Prime locations command premium prices</li>
            </ol>
        </div>
        
        <h3>Investment Categories & ROI Expectations</h3>
        
        <h4>💎 Premium Domains ($10K - $1M+)</h4>
        <ul>
            <li><strong>ROI:</strong> 15-25% annually</li>
            <li><strong>Examples:</strong> Insurance.com, Voice.com, 360.com</li>
            <li><strong>Strategy:</strong> Buy and hold 3-5 years</li>
            <li><strong>Risk:</strong> Low (established value)</li>
        </ul>
        
        <h4>🏆 Exact Match Domains ($1K - $50K)</h4>
        <ul>
            <li><strong>ROI:</strong> 25-50% annually</li>
            <li><strong>Examples:</strong> ChicagoPlumber.com, OnlineMBA.com</li>
            <li><strong>Strategy:</strong> Active marketing to end users</li>
            <li><strong>Risk:</strong> Medium (market dependent)</li>
        </ul>
        
        <h4>⚡ Trend Domains ($100 - $10K)</h4>
        <ul>
            <li><strong>ROI:</strong> 50-200% annually</li>
            <li><strong>Examples:</strong> NFTMarket.com, TeleHealth.co</li>
            <li><strong>Strategy:</strong> Quick flip within 1-2 years</li>
            <li><strong>Risk:</strong> High (trend dependent)</li>
        </ul>
        
        <h3>Portfolio Allocation Strategy</h3>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>📊 Recommended Portfolio Mix:</strong></p>
            <ul>
                <li><strong>40% Premium Domains:</strong> Stable, appreciating assets</li>
                <li><strong>40% Exact Match:</strong> Active income generators</li>
                <li><strong>20% Trend/Speculation:</strong> High-growth potential</li>
            </ul>
        </div>
        
        <h3>Financial Planning & Budgeting</h3>
        
        <h4>Starting Capital Requirements</h4>
        <ul>
            <li><strong>Beginner:</strong> $1,000 - $5,000 (5-10 domains)</li>
            <li><strong>Intermediate:</strong> $10,000 - $50,000 (20-50 domains)</li>
            <li><strong>Advanced:</strong> $100,000+ (Premium focus)</li>
        </ul>
        
        <h4>Cash Flow Management</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>💸 Monthly Expenses to Budget:</strong></p>
            <ul>
                <li><strong>Renewal Fees:</strong> $10-15 per domain annually</li>
                <li><strong>Research Tools:</strong> $100-500 monthly</li>
                <li><strong>Marketing/Outreach:</strong> $200-1000 monthly</li>
                <li><strong>Legal/Escrow:</strong> 3-5% of transaction value</li>
            </ul>
        </div>
        
        <h3>Tax Optimization Strategies</h3>
        <p><strong>🏦 Maximize Your Returns:</strong></p>
        <ul>
            <li><strong>Business Structure:</strong> LLC for liability protection</li>
            <li><strong>Expense Deductions:</strong> Research tools, travel, education</li>
            <li><strong>Depreciation:</strong> Treat domains as business assets</li>
            <li><strong>1031 Exchanges:</strong> Defer taxes on domain sales</li>
        </ul>
        
        <h3>Exit Strategies</h3>
        
        <h4>When to Sell</h4>
        <ol>
            <li><strong>3x Purchase Price:</strong> Solid profit taking</li>
            <li><strong>Industry Peak:</strong> Trend domains at maximum hype</li>
            <li><strong>Cash Flow Needs:</strong> Liquidate for new opportunities</li>
            <li><strong>End User Interest:</strong> Someone needs it for their business</li>
        </ol>
        
        <h4>Selling Channels</h4>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <ul>
                <li><strong>Direct Outreach:</strong> Contact potential end users</li>
                <li><strong>Broker Networks:</strong> Professional domain brokers</li>
                <li><strong>Auction Platforms:</strong> Sedo, Flippa, GoDaddy</li>
                <li><strong>Domain Shows:</strong> NamesCon, DomainFest</li>
            </ul>
        </div>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>💡 Investment Success Formula:</strong> Research (40%) + Patience (30%) + Market Timing (20%) + Luck (10%) = Consistent Profits
        </div>
        """,
        
        'Portfolio Building': """
        <h2>🏗️ Portfolio Building - Systematic Domain Accumulation</h2>
        
        <h3>Portfolio Foundation Strategy</h3>
        <p>A strong domain portfolio is like a balanced investment portfolio - diversified across industries, price points, and risk levels.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🏗️ Building Blocks of Success:</strong></p>
            <ol>
                <li><strong>Foundation Layer:</strong> 5-10 premium .com domains</li>
                <li><strong>Growth Layer:</strong> 20-30 exact match domains</li>
                <li><strong>Speculation Layer:</strong> 10-20 trend/emerging domains</li>
                <li><strong>International Layer:</strong> 5-10 ccTLD domains</li>
            </ol>
        </div>
        
        <h3>Acquisition Timeline & Milestones</h3>
        
        <h4>Year 1: Foundation (10-20 domains)</h4>
        <ul>
            <li><strong>Month 1-3:</strong> Research and acquire first 5 domains</li>
            <li><strong>Month 4-6:</strong> Focus on one specific niche</li>
            <li><strong>Month 7-9:</strong> Expand to second complementary niche</li>
            <li><strong>Month 10-12:</strong> Add international variations</li>
        </ul>
        
        <h4>Year 2: Growth (50+ domains)</h4>
        <ul>
            <li><strong>Reinvest all profits</strong> into new acquisitions</li>
            <li><strong>Develop market expertise</strong> in chosen niches</li>
            <li><strong>Build industry relationships</strong> with brokers and investors</li>
            <li><strong>Start premium domain targeting</strong> ($10K+ acquisitions)</li>
        </ul>
        
        <h3>Portfolio Diversification Matrix</h3>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>📊 Industry Diversification (Example $50K Portfolio):</strong></p>
            <ul>
                <li><strong>Healthcare (25%):</strong> $12,500 - Medical, dental, wellness</li>
                <li><strong>Financial (20%):</strong> $10,000 - Banking, investing, crypto</li>
                <li><strong>Technology (20%):</strong> $10,000 - AI, software, apps</li>
                <li><strong>Local Services (15%):</strong> $7,500 - Plumbing, legal, real estate</li>
                <li><strong>E-commerce (10%):</strong> $5,000 - Product categories</li>
                <li><strong>Emerging Trends (10%):</strong> $5,000 - Speculation plays</li>
            </ul>
        </div>
        
        <h3>Quality Control Standards</h3>
        
        <h4>The RIZZOS Quality Framework</h4>
        <p><strong>R</strong>elevant - Clear commercial application</p>
        <p><strong>I</strong>ntuitive - Easy to remember and spell</p>
        <p><strong>Z</strong>ero Conflicts - No trademark issues</p>
        <p><strong>Z</strong>one Authority - Strong SEO potential</p>
        <p><strong>O</strong>ptimal Length - Under 15 characters preferred</p>
        <p><strong>S</strong>calable - Room for business growth</p>
        
        <h3>Portfolio Management Tools</h3>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>🛠️ Essential Management Tools:</strong></p>
            <ul>
                <li><strong>Spreadsheet Tracking:</strong> Purchase price, renewal dates, valuations</li>
                <li><strong>Domain Registrar Management:</strong> Consolidate at 1-2 registrars</li>
                <li><strong>Automated Renewals:</strong> Prevent accidental losses</li>
                <li><strong>Performance Monitoring:</strong> Track inquiries and offers</li>
                <li><strong>Market Value Updates:</strong> Quarterly valuation reviews</li>
            </ul>
        </div>
        
        <h3>Scaling Strategies</h3>
        
        <h4>Bootstrap Growth Method</h4>
        <ol>
            <li><strong>Start small:</strong> $1,000 initial investment</li>
            <li><strong>Sell for 2-3x:</strong> Target quick wins</li>
            <li><strong>Reinvest 80%:</strong> Keep 20% as profit</li>
            <li><strong>Compound growth:</strong> Double portfolio every 18 months</li>
        </ol>
        
        <h4>Leveraged Growth Method</h4>
        <ul>
            <li><strong>Business loans:</strong> Use domain portfolio as collateral</li>
            <li><strong>Investor partnerships:</strong> Split profits 50/50</li>
            <li><strong>Payment plans:</strong> Acquire premium domains over time</li>
            <li><strong>Revenue sharing:</strong> Ongoing income from development</li>
        </ul>
        
        <h3>Risk Management</h3>
        
        <h4>Portfolio Protection Strategies</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">
            <p><strong>⚠️ Risk Mitigation Checklist:</strong></p>
            <ul>
                <li>✅ Never put >10% in any single domain</li>
                <li>✅ Maintain 6 months renewal fees in cash</li>
                <li>✅ Diversify across multiple industries</li>
                <li>✅ Regular trademark searches</li>
                <li>✅ Backup registrar accounts</li>
                <li>✅ Annual portfolio insurance review</li>
            </ul>
        </div>
        
        <h3>Exit Planning</h3>
        <p><strong>🚪 Portfolio Exit Strategies:</strong></p>
        <ul>
            <li><strong>Gradual Liquidation:</strong> Sell 20% annually</li>
            <li><strong>Portfolio Sale:</strong> Package deal to strategic buyer</li>
            <li><strong>Development Exit:</strong> Build websites and sell businesses</li>
            <li><strong>Legacy Planning:</strong> Transfer to next generation</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>🎯 Portfolio Success Metric:</strong> Aim for 25% of your domains to generate 80% of your profits. Quality always beats quantity in domain investing.
        </div>
        """
    }
    
    # Get the content for the specific guide, or default content if not found
    guide_content = guide_contents.get(guide_display_name, f"""
    <h2>{guide_display_name}</h2>
    <p>This guide is currently being developed with comprehensive content. Please check back soon for detailed strategies and actionable steps.</p>
    <p>Your current package gives you access to this premium content as part of the Rizzos AI Domain Empire system.</p>
    """)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{guide_display_name} - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; }}
            h2 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
            h3 {{ color: #667eea; margin-top: 25px; }}
            h4 {{ color: #555; margin-top: 20px; }}
            ul, ol {{ line-height: 1.6; }}
            li {{ margin-bottom: 5px; }}
            .back-btn {{ display: inline-block; background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .back-btn:hover {{ background: #5a6fd8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            {guide_content}
        </div>
    </body>
    </html>
    """
            .back-btn {{ background: #e2e8f0; color: #4a5568; padding: 8px 16px; border-radius: 8px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            <br><br>
            {guide_content}
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

@app.route('/portfolio')
def portfolio():
    """Portfolio management page"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Portfolio - Rizzos AI</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; }
            .back-btn { background: #e2e8f0; color: #4a5568; padding: 8px 16px; border-radius: 8px; text-decoration: none; }
            .portfolio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
            .portfolio-card { background: #f7fafc; border-radius: 10px; padding: 20px; border-left: 4px solid #667eea; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            <h1>📊 Domain Portfolio Management</h1>
            <p>Track and manage your domain investments</p>
            
            <div class="portfolio-grid">
                <div class="portfolio-card">
                    <h3>Portfolio Value</h3>
                    <p>Total estimated value of your domain portfolio</p>
                </div>
                <div class="portfolio-card">
                    <h3>Active Domains</h3>
                    <p>Domains currently in your portfolio</p>
                </div>
                <div class="portfolio-card">
                    <h3>Revenue Tracking</h3>
                    <p>Monitor income from domain sales and parking</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/market')
def market():
    """Market analysis page"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Market Analysis - Rizzos AI</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; }
            .back-btn { background: #e2e8f0; color: #4a5568; padding: 8px 16px; border-radius: 8px; text-decoration: none; }
            .market-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
            .market-card { background: #f7fafc; border-radius: 10px; padding: 20px; border-left: 4px solid #48bb78; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            <h1>📈 Domain Market Analysis</h1>
            <p>Real-time insights into domain market trends</p>
            
            <div class="market-grid">
                <div class="market-card">
                    <h3>Trending Extensions</h3>
                    <p>Most popular domain extensions this month</p>
                </div>
                <div class="market-card">
                    <h3>Price Trends</h3>
                    <p>Historical price data and market movements</p>
                </div>
                <div class="market-card">
                    <h3>Hot Keywords</h3>
                    <p>High-value keywords and niches to watch</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# Force logout route for admin management
@app.route('/force-logout')
def force_logout():
    """Force logout for admin management"""
    if 'username' not in session or not session.get('is_admin', False):
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))
    
    session.clear()
    flash('Forced logout completed.', 'success')
    return redirect(url_for('login'))

# Upgrade route for package upgrades
@app.route('/upgrade-me')
def upgrade_me():
    """Package upgrade route"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upgrade Package - Rizzos AI</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; text-align: center; }
            .upgrade-btn { background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 1.2em; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Upgrade Your Package</h1>
            <p>Unlock more guides and features with our premium packages</p>
            
            <div style="margin-top: 30px;">
                <a href="https://buy.stripe.com/14AbJ299E1os2Jp8Td1oI0h" class="upgrade-btn">Elite Package - $499.99</a>
                <a href="https://buy.stripe.com/9B6eVefy25EI5VB0mH1oI04" class="upgrade-btn">Empire Package - $999.99</a>
            </div>
            
            <br><br>
            <a href="/">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """