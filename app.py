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
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
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
        if "api_key" in error_msg.lower():
            return "Invalid API key configuration. Please contact support."
        elif "model" in error_msg.lower():
            return "Model access issue. Please contact support."
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
    customers = load_customers()
    return customers.get(username, {}).get('package', 'starter')

def get_package_guides(username):
    """Get available guides for user's package"""
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
    """3-Part Admin Authentication Login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check if user is banned
        if is_banned_user(username):
            flash('Your account has been suspended. Please contact support.', 'error')
            return redirect(url_for('login'))
        
        # 3-Part Admin Authentication
        if (username == ADMIN_USERNAME and 
            email == ADMIN_EMAIL and 
            password == ADMIN_PASSWORD):
            session['username'] = username
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        
        # Customer login - check against customer database
        customers = load_customers()
        if username in customers and customers[username].get('password') == password:
            session['username'] = username
            session['is_admin'] = False
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials. All fields are required for admin access.', 'error')
    
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
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="login-btn">Access Domain Empire</button>
            </form>
            
            <div class="security-note">
                <h4>🔒 Enhanced Security</h4>
                <p>3-part authentication ensures maximum security for your domain empire management.</p>
            </div>
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
    
    # Simple guide content (in a real app, this would come from a database)
    guide_content = f"""
    <h2>{guide_display_name}</h2>
    <p>This is the content for {guide_display_name}. In a production system, this would contain detailed domain investing guidance, strategies, and actionable steps.</p>
    <p>Your current package gives you access to this premium content as part of the Rizzos AI Domain Empire system.</p>
    """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{guide_display_name} - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; }}
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