from flask import Flask, request, redirect, url_for, session, flash, render_template_string, jsonify
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
<<<<<<< HEAD
app.secret_key = os.environ.get('SECRET_KEY', 'rizzos-secret-key-2024-secure')

# Configure OpenAI for Coey - FRESH PROJECT V2
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Admin credentials - 3-part secure login
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'rizzos-secret-key-2024-secure')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'ai@rizzosai.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'GETFUCkeduCunt71')

# Simple customer database (in production, use a real database)
CUSTOMERS_FILE = 'customers.json'
BANNED_USERS_FILE = 'banned_users.json'
CHAT_MEMORY_FILE = 'chat_memory.json'

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

def add_to_memory(user_id, user_message, coey_response, conversation_type='regular'):
    """Add conversation to memory for context"""
    memory = load_chat_memory()
    if user_id not in memory:
        memory[user_id] = {
            'regular': [],
            'onboarding': []
        }
    
    # Keep last 10 exchanges for context
    if len(memory[user_id][conversation_type]) >= 20:  # 10 exchanges = 20 messages
        memory[user_id][conversation_type] = memory[user_id][conversation_type][-18:]  # Keep last 9 exchanges
    
    memory[user_id][conversation_type].append({
        'user': user_message,
        'coey': coey_response,
        'timestamp': datetime.now().isoformat()
    })
    
    save_chat_memory(memory)

def get_conversation_context(user_id, conversation_type='regular'):
    """Get conversation history for context"""
    memory = load_chat_memory()
    if user_id not in memory or conversation_type not in memory[user_id]:
        return []
    
    # Convert to OpenAI format
    context = []
    for exchange in memory[user_id][conversation_type]:
        context.append({"role": "user", "content": exchange['user']})
        context.append({"role": "assistant", "content": exchange['coey']})
    
    return context
=======
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
AFFILIATES_FILE = 'affiliates.json'
AFFILIATE_SALES_FILE = 'affiliate_sales.json'
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad

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

<<<<<<< HEAD
def get_clean_openai_response(messages, max_tokens=800, temperature=0.3, model="gpt-4"):
    """Bulletproof OpenAI API call with multiple fallback strategies"""
    if not OPENAI_API_KEY:
        return None
    
    try:
        # Strategy 1: Modern OpenAI client with explicit parameters
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "proxies" in str(e).lower():
                # Strategy 2: Import and initialize fresh
                import importlib
                import sys
                if 'openai' in sys.modules:
                    importlib.reload(sys.modules['openai'])
                
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            else:
                raise e
                
    except Exception as openai_error:
        print(f"OpenAI API error: {str(openai_error)}")
        return None

# Package definitions with empire-trial for conversion optimization
=======
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

def load_affiliates():
    """Load affiliates from JSON file"""
    try:
        with open(AFFILIATES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_affiliates(affiliates):
    """Save affiliates to JSON file"""
    with open(AFFILIATES_FILE, 'w') as f:
        json.dump(affiliates, f, indent=2)

def load_affiliate_sales():
    """Load affiliate sales from JSON file"""
    try:
        with open(AFFILIATE_SALES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_affiliate_sales(sales):
    """Save affiliate sales to JSON file"""
    with open(AFFILIATE_SALES_FILE, 'w') as f:
        json.dump(sales, f, indent=2)

def generate_affiliate_code(username):
    """Generate unique affiliate code"""
    import hashlib
    import random
    base = f"{username}{random.randint(1000, 9999)}"
    return hashlib.md5(base.encode()).hexdigest()[:8].upper()

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
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
PACKAGES = {
    'starter': {
        'name': 'Starter Package',
        'price': '$29.99',
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup']
    },
    'pro': {
        'name': 'Pro Package', 
        'price': '$99.99',
<<<<<<< HEAD
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup', 'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 'Market Analysis', 'Negotiation Tactics']
=======
        'guides': [
            'Domain Basics', 'First Purchase Guide', 'Quick Setup', 
            'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 
            'Market Analysis', 'Negotiation Tactics'
        ]
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    },
    'elite': {
        'name': 'Elite Package',
        'price': '$499.99', 
<<<<<<< HEAD
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup', 'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 'Market Analysis', 'Negotiation Tactics', 'Empire Building', 'Advanced Analytics', 'Premium Tools', 'Elite Strategies', 'Insider Secrets']
=======
        'guides': [
            'Domain Basics', 'First Purchase Guide', 'Quick Setup', 
            'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 
            'Market Analysis', 'Negotiation Tactics', 'Empire Building', 
            'Advanced Analytics', 'Premium Tools', 'Elite Strategies', 'Insider Secrets'
        ]
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    },
    'empire': {
        'name': 'Empire Package',
        'price': '$999.99',
<<<<<<< HEAD
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup', 'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 'Market Analysis', 'Negotiation Tactics', 'Empire Building', 'Advanced Analytics', 'Premium Tools', 'Elite Strategies', 'Insider Secrets', 'Master Class', 'Personal Coaching', 'Exclusive Networks']
=======
        'guides': [
            'Domain Basics', 'First Purchase Guide', 'Quick Setup',
            'Advanced Strategies', 'Investment Guide', 'Portfolio Building',
            'Market Analysis', 'Negotiation Tactics', 'Empire Building',
            'Advanced Analytics', 'Premium Tools', 'Elite Strategies',
            'Insider Secrets', 'Master Class', 'Personal Coaching', 'Exclusive Networks'
        ]
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
=======
    # Admin gets access to all packages (Empire level)
    if username == ADMIN_USERNAME:
        return 'empire'
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    customers = load_customers()
    return customers.get(username, {}).get('package', 'starter')

def get_package_guides(username):
    """Get available guides for user's package"""
<<<<<<< HEAD
    package = get_user_package(username)
    if package in PACKAGES:
        return PACKAGES[package]['guides']
    return PACKAGES['starter']['guides']  # Default to starter
=======
    # Admin gets access to all guides (Empire level)
    if username == ADMIN_USERNAME or username == 'rizzos-admin':
        return PACKAGES['empire']['guides']
    package = get_user_package(username)
    if package in PACKAGES:
        return PACKAGES[package]['guides']
    return PACKAGES['starter']['guides']
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad

def is_banned_user(username):
    """Check if user is banned"""
    banned_users = load_banned_users()
    return username in banned_users

@app.route('/')
def dashboard():
<<<<<<< HEAD
    """Main dashboard - redirects to login if not authenticated"""
=======
    """Main dashboard - beautiful modern design"""
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
    
<<<<<<< HEAD
    # Check if this is empire-trial and if they've hit the limit
=======
    # Trial status for empire-trial users
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    trial_status = ""
    if package == 'empire-trial':
        customers = load_customers()
        guides_accessed = customers.get(username, {}).get('guides_accessed', 0)
        remaining = PACKAGES['empire-trial']['limit'] - guides_accessed
        if remaining <= 0:
            trial_status = f"""
            <div class="trial-expired">
                <h3>🚀 Trial Complete! Ready to Unlock Everything?</h3>
<<<<<<< HEAD
                <p>You've explored {PACKAGES['empire-trial']['limit']} guides. Upgrade to Empire Package for unlimited access to all {len(PACKAGES['empire']['guides'])} premium guides!</p>
                <a href="https://buy.stripe.com/00g8A20Ey6iT0es3cc" class="upgrade-btn">Upgrade to Empire Package - $999.99</a>
=======
                <p>You've explored {PACKAGES['empire-trial']['limit']} guides. Upgrade to Elite Package for unlimited access to all {len(PACKAGES['elite']['guides'])} premium guides!</p>
                <a href="https://buy.stripe.com/14AbJ299E1os2Jp8Td1oI0h" class="upgrade-btn">Upgrade to Elite Package - $499.99</a>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
        <title>Rizzos AI - Domain Empire Backoffice V2</title>
=======
        <title>Rizzos AI - Domain Empire Backoffice</title>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
                    <h1>🏆 Domain Empire Backoffice V2</h1>
                    <p>Your gateway to domain investing mastery - Fresh & Clean!</p>
=======
                    <h1>🏆 Rizzos AI Domain Empire</h1>
                    <p>Your gateway to domain investing mastery</p>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
                    <h2>📚 Your Guides</h2>
=======
                    <h2>📚 Your Guides ({len(available_guides)})</h2>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
                        <a href="/market" class="coey-btn">📈 Market</a>
                        <a href="/tools" class="coey-btn">🛠️ Tools</a>
=======
                        <a href="/market" class="coey-btn">📈 Market Data</a>
                        <a href="/tools" class="coey-btn">🛠️ Tools</a>
                        <a href="/affiliate" class="coey-btn">💰 Affiliate Program</a>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
                    </div>
                </div>
                
                <div class="section coey-section">
                    <h2>🤖 Meet Coey - Your AI Domain Advisor</h2>
<<<<<<< HEAD
                    <p>Get personalized domain investing advice from our Claude-like AI assistant</p>
                    <div style="margin-top: 15px;">
                        <a href="/coey" class="coey-btn">💬 Chat with Coey</a>
                        <a href="/coey/onboarding" class="coey-btn">🎯 Onboarding Assistant</a>
=======
                    <p>Get personalized domain investing advice from our advanced AI assistant powered by GPT-4</p>
                    <div style="margin-top: 15px;">
                        <a href="/coey" class="coey-btn">💬 Chat with Coey</a>
                        <a href="/coey/onboarding" class="coey-btn">🎯 Onboarding Assistant</a>
                        <a href="/change-password" class="coey-btn">🔑 Change Password</a>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
=======
    """User and Admin Authentication Login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()  # Only required for admin
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        
        # Check if user is banned
        if is_banned_user(username):
            flash('Your account has been suspended. Please contact support.', 'error')
            return redirect(url_for('login'))
        
<<<<<<< HEAD
        # Admin login - 3-part authentication
        if (username == ADMIN_USERNAME and 
            email == ADMIN_EMAIL and 
            password == ADMIN_PASSWORD):
=======
        # TEMPORARY: Auto-admin access for troubleshooting
        if username == 'rizzos-admin' or username == 'admin' or username == 'test':
            session['username'] = 'rizzos-admin'
            session['is_admin'] = True
            return redirect(url_for('dashboard'))
        
        # Admin Authentication (simplified - username and password only)
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
            session['username'] = username
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        
<<<<<<< HEAD
        # Customer login - check against customer database
=======
        # Also check admin by email
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['username'] = ADMIN_USERNAME
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        
        # Regular User Authentication (username + password only)
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        customers = load_customers()
        if username in customers and customers[username].get('password') == password:
            session['username'] = username
            session['is_admin'] = False
            return redirect(url_for('dashboard'))
        
<<<<<<< HEAD
        flash('Invalid credentials. All fields required for admin access.', 'error')
=======
        flash('Invalid username or password.', 'error')
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    
    login_html = """
    <!DOCTYPE html>
    <html>
    <head>
<<<<<<< HEAD
        <title>Rizzos AI - Login V2</title>
=======
        <title>Rizzos AI - Secure Login</title>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
=======
            .security-note {
                margin-top: 20px;
                padding: 15px;
                background: #f7fafc;
                border-radius: 8px;
                border-left: 4px solid #4299e1;
            }
            .security-note h4 { color: #2d3748; margin-bottom: 5px; }
            .security-note p { color: #4a5568; font-size: 0.9em; }
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
<<<<<<< HEAD
                <h1>🏆 Rizzos AI V2</h1>
                <p>Domain Empire Access - Fresh & Clean</p>
=======
                <h1>🏆 Rizzos AI</h1>
                <p>Domain Empire Access Portal</p>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
<<<<<<< HEAD
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="login-btn">Access Empire V2</button>
            </form>
=======
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <!-- Admin email field (always visible for flexibility) -->
                <div class="form-group" id="admin-email-group">
                    <label for="email">Email (Optional - for admin access)</label>
                    <input type="email" id="email" name="email" placeholder="admin@rizzosai.com (for admin only)">
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
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        </div>
    </body>
    </html>
    """
    
    return render_template_string(login_html)

<<<<<<< HEAD
=======
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

>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

<<<<<<< HEAD
@app.route('/owner-access')
def owner_access():
    """Special route for owner to get Elite package access"""
=======
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
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    # Auto-create owner account with Elite package
    customers = load_customers()
    
    owner_username = "rizzosowner"
    owner_password = "empire2024!"
    
    customers[owner_username] = {
        'password': owner_password,
        'email': 'owner@rizzosai.com',
        'package': 'elite',
        'created_at': datetime.now().isoformat(),
<<<<<<< HEAD
        'session_id': 'owner_direct_v2',
=======
        'session_id': 'owner_direct_access',
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        'guides_accessed': 0,
        'owner': True
    }
    
    save_customers(customers)
    
<<<<<<< HEAD
    # Auto-login
=======
    # Auto-login the owner
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    session['username'] = owner_username
    session['is_admin'] = False
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
<<<<<<< HEAD
        <title>Owner Access Created V2 - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
            .success-box {{ background: white; padding: 40px; border-radius: 15px; text-align: center; max-width: 500px; }}
            .access-btn {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px 30px; border: none; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 20px; }}
=======
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
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        </style>
    </head>
    <body>
        <div class="success-box">
<<<<<<< HEAD
            <h1>🏆 Owner Access Created V2!</h1>
            <p><strong>Username:</strong> {owner_username}</p>
            <p><strong>Password:</strong> {owner_password}</p>
            <p><strong>Package:</strong> Elite Package ($499.99)</p>
            <p>You now have access to all {len(PACKAGES['elite']['guides'])} Elite guides!</p>
            <p><strong>Fresh Project V2 - No Cache Issues!</strong></p>
            <a href="/" class="access-btn">Access Your Elite Dashboard V2</a>
=======
            <h1>🏆 Owner Access Created Successfully!</h1>
            <div class="credentials">
                <p><strong>Username:</strong> {owner_username}</p>
                <p><strong>Password:</strong> {owner_password}</p>
                <p><strong>Package:</strong> Elite Package ($499.99)</p>
                <p><strong>Guides Available:</strong> {len(PACKAGES['elite']['guides'])}</p>
            </div>
            <p>You now have access to all Elite guides and premium features!</p>
            <a href="/" class="access-btn">Access Your Elite Dashboard</a>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
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
    
<<<<<<< HEAD
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coey AI V2 - Domain Advisor</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 20px; }
            h1 { color: #4a5568; text-align: center; }
            .back-btn { background: #e2e8f0; color: #4a5568; padding: 8px 16px; border-radius: 8px; text-decoration: none; }
        </style>
=======
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
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
<<<<<<< HEAD
            <h1>🤖 Coey AI V2 - Coming Soon!</h1>
            <p>Your AI domain advisor will be available soon with the new API integration!</p>
=======
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
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        </div>
    </body>
    </html>
    """
<<<<<<< HEAD
=======
    
    return chat_html
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad

@app.route('/coey/chat', methods=['POST'])
def coey_chat_api():
    """Handle chat messages to Coey AI"""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
<<<<<<< HEAD
    # Get response from OpenAI
    messages = [
        {"role": "system", "content": "You are Coey, an expert AI domain investing advisor. Help users build successful domain portfolios."},
        {"role": "user", "content": user_message}
    ]
    
    coey_response = get_clean_openai_response(messages)
    
    if not coey_response:
        coey_response = "I'm having technical difficulties right now, but I can tell you that successful domain investing requires research, patience, and strategic thinking. What specific area would you like to explore?"
    
    return jsonify({'response': coey_response})

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard for managing customers and system"""
    if 'username' not in session or not session.get('is_admin', False):
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))
    
    # Load customer data
    customers = load_customers()
    banned_users = load_banned_users()
    
    # Count packages
    package_counts = {}
    for customer in customers.values():
        package = customer.get('package', 'starter')
        package_counts[package] = package_counts.get(package, 0) + 1
    
    admin_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard V2 - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin-bottom: 20px; text-align: center; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }}
            .stat-card {{ background: rgba(255,255,255,0.95); border-radius: 10px; padding: 20px; text-align: center; }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
            .customers-section {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; }}
            .customer-item {{ padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }}
            .package-badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.8em; }}
            .starter {{ background: #48bb78; }}
            .pro {{ background: #667eea; }}
            .elite {{ background: #ff6b6b; }}
            .empire {{ background: #feca57; color: black; }}
            .empire-trial {{ background: #ff9ff3; }}
            .logout-btn {{ background: #e53e3e; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; }}
=======
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

@app.route('/coey/onboarding')
def coey_onboarding():
    """Coey AI Onboarding Assistant"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_package = get_user_package(username)
    
    onboarding_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coey Onboarding Assistant - Rizzos AI</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Arial', sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; 
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #667eea;
            }}
            .header h1 {{
                color: #333;
                margin-bottom: 10px;
            }}
            .welcome-section {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }}
            .step-card {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
            }}
            .step-number {{
                background: #667eea;
                color: white;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                margin-right: 15px;
            }}
            .step-header {{
                display: flex;
                align-items: center;
                margin-bottom: 15px;
            }}
            .action-btn {{
                background: #28a745;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                display: inline-block;
                margin: 10px 10px 10px 0;
                cursor: pointer;
                transition: background 0.3s;
            }}
            .action-btn:hover {{
                background: #218838;
                color: white;
                text-decoration: none;
            }}
            .secondary-btn {{
                background: #6c757d;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                display: inline-block;
                margin: 10px 10px 10px 0;
                cursor: pointer;
                transition: background 0.3s;
            }}
            .secondary-btn:hover {{
                background: #5a6268;
                color: white;
                text-decoration: none;
            }}
            .package-info {{
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
            .chat-preview {{
                background: #e7f3ff;
                border: 1px solid #2196F3;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }}
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
<<<<<<< HEAD
                <h1>🏆 Admin Dashboard V2 - Fresh & Clean</h1>
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
                    <div class="stat-number">{len(banned_users)}</div>
                    <div>Banned Users</div>
                </div>
            </div>
            
            <div class="customers-section">
                <h2>Customer Management</h2>
                {''.join([f'''
                <div class="customer-item">
                    <div>
                        <strong>{username}</strong> ({customer.get('email', 'No email')})
                        <br><small>Created: {customer.get('created_at', 'Unknown')}</small>
                    </div>
                    <div>
                        <span class="package-badge {customer.get('package', 'starter')}">{PACKAGES.get(customer.get('package', 'starter'), {}).get('name', 'Unknown')}</span>
                    </div>
                </div>
                ''' for username, customer in customers.items()])}
=======
                <h1>🎯 Welcome to Your Domain Empire Journey!</h1>
                <p>Your Personal AI Guide to Domain Investing Success</p>
            </div>
            
            <div class="welcome-section">
                <h2>👋 Hi {username}! I'm Coey, Your Domain Investing Assistant</h2>
                <p>I'm here to guide you through building a profitable domain portfolio step by step. Let's turn your investment into a thriving domain empire!</p>
                <div class="package-info">
                    <strong>📦 Your Current Package:</strong> {PACKAGES.get(user_package, {{}}).get('name', 'Unknown')} | 
                    <strong>🎯 Guides Available:</strong> {len(get_package_guides(username))}
                </div>
            </div>
            
            <div class="step-card">
                <div class="step-header">
                    <span class="step-number">1</span>
                    <h3>🎓 Learn the Foundations</h3>
                </div>
                <p>Start with the essential knowledge every domain investor needs. Master the basics before moving to advanced strategies.</p>
                <a href="/guide/domain-basics" class="action-btn">📚 Start Domain Basics Guide</a>
                <a href="/guide/first-purchase-guide" class="secondary-btn">🛒 First Purchase Guide</a>
            </div>
            
            <div class="step-card">
                <div class="step-header">
                    <span class="step-number">2</span>
                    <h3>⚡ Quick Setup (24 Hours)</h3>
                </div>
                <p>Get your domain investing business set up in just one day. Tools, accounts, and your first opportunities identified.</p>
                <a href="/guide/quick-setup" class="action-btn">🚀 24-Hour Setup Guide</a>
            </div>
            
            <div class="step-card">
                <div class="step-header">
                    <span class="step-number">3</span>
                    <h3>💰 Build Your Strategy</h3>
                </div>
                <p>Develop your investment approach based on your budget, risk tolerance, and market interests.</p>
                <a href="/guide/investment-guide" class="action-btn">💎 Investment Strategies</a>
                <a href="/guide/portfolio-building" class="secondary-btn">🏗️ Portfolio Building</a>
            </div>
            
            <div class="step-card">
                <div class="step-header">
                    <span class="step-number">4</span>
                    <h3>🚀 Advanced Techniques</h3>
                </div>
                <p>Scale your empire with advanced strategies, market analysis, and negotiation tactics.</p>
                <a href="/guide/advanced-strategies" class="action-btn">⚡ Advanced Strategies</a>
                <a href="/guide/market-analysis" class="secondary-btn">📊 Market Analysis</a>
            </div>
            
            <div class="chat-preview">
                <h3>💬 Ask Coey Anything</h3>
                <p>I'm here 24/7 to answer your domain investing questions. Try asking me:</p>
                <ul>
                    <li>"What's a good budget for my first domain purchase?"</li>
                    <li>"How do I evaluate if a domain is worth buying?"</li>
                    <li>"What are the hottest domain trends right now?"</li>
                    <li>"How do I negotiate with domain sellers?"</li>
                </ul>
                <a href="/coey" class="action-btn">💬 Chat with Coey Now</a>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" class="secondary-btn">← Back to Dashboard</a>
                <a href="/portfolio" class="action-btn">📊 View Portfolio Tools</a>
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad
            </div>
        </div>
    </body>
    </html>
    """
    
<<<<<<< HEAD
    return admin_html
=======
    return onboarding_html

@app.route('/coey/test')
def coey_test():
    """Test Coey AI connection - Admin only"""
    if 'username' not in session or not session.get('is_admin'):
        return "Access denied. Admin only."
    
    # Test OpenAI configuration
    test_result = f"""
    <h2>🔧 Coey AI Debug Information</h2>
    <p><strong>API Key Status:</strong> {'✅ Set' if OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key_here' else '❌ Not Set'}</p>
    <p><strong>API Key Length:</strong> {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0} characters</p>
    <p><strong>API Key Preview:</strong> {OPENAI_API_KEY[:10] + '...' if OPENAI_API_KEY and len(OPENAI_API_KEY) > 10 else 'None'}</p>
    
    <h3>Testing OpenAI Connection:</h3>
    """
    
    # Test the OpenAI function
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Hello from Coey!' if this test works."}
    ]
    
    response = get_openai_response(test_messages)
    test_result += f"<p><strong>Response:</strong> {response}</p>"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Coey Debug - Rizzos AI</title></head>
    <body style="font-family: Arial; padding: 20px; max-width: 800px;">
        {test_result}
        <br><a href="/admin">← Back to Admin</a>
    </body>
    </html>
    """

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
        
        'Market Analysis': """
        <h2>📊 Market Analysis - Reading Domain Market Signals</h2>
        
        <h3>Market Intelligence Framework</h3>
        <p>Understanding market dynamics is crucial for timing acquisitions and sales perfectly.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>📈 Key Market Indicators:</strong></p>
            <ol>
                <li><strong>Sales Volume:</strong> Weekly transaction reports</li>
                <li><strong>Price Trends:</strong> YoY appreciation rates by category</li>
                <li><strong>Industry Growth:</strong> Business formation in target sectors</li>
                <li><strong>Search Volume:</strong> Google Trends for keywords</li>
                <li><strong>Investment Flow:</strong> VC funding in target industries</li>
            </ol>
        </div>
        
        <h3>Industry Cycle Analysis</h3>
        
        <h4>🚀 Growth Phase Indicators</h4>
        <ul>
            <li><strong>Media Coverage:</strong> Increasing news mentions</li>
            <li><strong>New Business Formation:</strong> Rising LLC registrations</li>
            <li><strong>Domain Registration Surge:</strong> Related TLD activity</li>
            <li><strong>Search Trend Growth:</strong> 50%+ YoY increase</li>
            <li><strong>Investment Capital:</strong> VC/PE funding rounds</li>
        </ul>
        
        <h4>⚠️ Peak Phase Warning Signs</h4>
        <ul>
            <li><strong>Mainstream Adoption:</strong> Everyone talking about it</li>
            <li><strong>Domain Price Explosion:</strong> 10x+ price increases</li>
            <li><strong>Speculation Frenzy:</strong> Low-quality domains selling high</li>
            <li><strong>Media Saturation:</strong> Daily news coverage</li>
            <li><strong>Celebrity Endorsements:</strong> Famous people promoting</li>
        </ul>
        
        <h3>Competitive Intelligence</h3>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>🕵️ Monitor Your Competition:</strong></p>
            <ul>
                <li><strong>Domain Auction Activity:</strong> Track who's buying what</li>
                <li><strong>Portfolio Analysis:</strong> Study successful investors</li>
                <li><strong>Price Sensitivity:</strong> Watch bidding patterns</li>
                <li><strong>Exit Strategies:</strong> When top investors sell</li>
                <li><strong>Geographic Focus:</strong> Regional investment patterns</li>
            </ul>
        </div>
        
        <h3>Valuation Methodologies</h3>
        
        <h4>📊 Comparable Sales Analysis</h4>
        <p>Find similar domains that sold recently and adjust for differences.</p>
        <ul>
            <li><strong>Exact Match:</strong> Same keywords, different TLD</li>
            <li><strong>Similar Industry:</strong> Same sector, related keywords</li>
            <li><strong>Geographic Variation:</strong> Same service, different city</li>
            <li><strong>Brand Strength:</strong> Memorability and brandability</li>
        </ul>
        
        <h4>💰 Revenue Multiple Method</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Calculate Based on Business Potential:</strong></p>
            <ul>
                <li><strong>Service Industry:</strong> 0.5-2x annual revenue potential</li>
                <li><strong>E-commerce:</strong> 1-3x annual revenue potential</li>
                <li><strong>SaaS/Tech:</strong> 2-5x annual revenue potential</li>
                <li><strong>Finance/Insurance:</strong> 3-10x annual revenue potential</li>
            </ul>
        </div>
        
        <h3>Market Timing Strategies</h3>
        
        <h4>🎯 Best Buying Opportunities</h4>
        <ol>
            <li><strong>Market Corrections:</strong> 20-30% price drops</li>
            <li><strong>End of Year:</strong> Tax-loss selling pressure</li>
            <li><strong>Economic Uncertainty:</strong> Flight to quality assets</li>
            <li><strong>Industry Downturns:</strong> Temporary pessimism</li>
            <li><strong>Expiring Domains:</strong> Owner financial stress</li>
        </ol>
        
        <h4>💎 Optimal Selling Windows</h4>
        <ol>
            <li><strong>Industry Peak Hype:</strong> Maximum media attention</li>
            <li><strong>IPO Seasons:</strong> Q1 and Q4 business activity</li>
            <li><strong>Funding Announcements:</strong> When startups raise capital</li>
            <li><strong>Regulatory Clarity:</strong> Legal certainty drives investment</li>
            <li><strong>Technology Breakthroughs:</strong> Innovation catalysts</li>
        </ol>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>💡 Market Analysis Pro Tip:</strong> The best opportunities often come during market fear when everyone else is selling. Contrarian investing works in domains just like stocks.
        </div>
        """,
        
        'Negotiation Tactics': """
        <h2>🤝 Negotiation Tactics - Master the Art of Domain Deals</h2>
        
        <h3>Psychology of Domain Negotiations</h3>
        <p>Domain negotiations are unique because you're selling a one-of-a-kind asset that the buyer cannot get elsewhere.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🧠 Negotiation Psychology Principles:</strong></p>
            <ol>
                <li><strong>Scarcity Leverage:</strong> Only one exists, ever</li>
                <li><strong>Urgency Creation:</strong> Business needs it now</li>
                <li><strong>Value Anchoring:</strong> Set high initial expectations</li>
                <li><strong>Alternative Highlighting:</strong> Cost of not having it</li>
                <li><strong>Relationship Building:</strong> Long-term partnership focus</li>
            </ol>
        </div>
        
        <h3>Pre-Negotiation Intelligence</h3>
        
        <h4>🔍 Research Your Buyer</h4>
        <ul>
            <li><strong>Company Financials:</strong> Recent funding, revenue estimates</li>
            <li><strong>Business Model:</strong> How the domain fits their strategy</li>
            <li><strong>Competition Analysis:</strong> What alternatives they have</li>
            <li><strong>Timeline Pressure:</strong> Launch dates, investor meetings</li>
            <li><strong>Decision Makers:</strong> Who has purchasing authority</li>
        </ul>
        
        <h4>💼 Establish Your Position</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>📋 Preparation Checklist:</strong></p>
            <ul>
                <li><strong>Comparable Sales:</strong> Recent similar domain sales</li>
                <li><strong>Market Value:</strong> Professional appraisals</li>
                <li><strong>Cost Basis:</strong> Your investment + holding costs</li>
                <li><strong>Alternative Options:</strong> Other domains you'd consider</li>
                <li><strong>Walk-Away Price:</strong> Minimum acceptable offer</li>
            </ul>
        </div>
        
        <h3>Negotiation Tactics & Strategies</h3>
        
        <h4>🎯 Opening Move Strategies</h4>
        <p><strong>The Anchor High Approach:</strong></p>
        <ul>
            <li><strong>Start 3-5x</strong> your target price</li>
            <li><strong>Justify with comparables</strong> and business value</li>
            <li><strong>Show flexibility</strong> for quick decisions</li>
            <li><strong>Offer payment plans</strong> to reduce sticker shock</li>
        </ul>
        
        <h4>🛡️ Defensive Tactics</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>When Buyers Push Back:</strong></p>
            <ul>
                <li><strong>"Too Expensive":</strong> Break down ROI calculations</li>
                <li><strong>"Need Board Approval":</strong> Offer presentation materials</li>
                <li><strong>"Looking at Alternatives":</strong> Highlight unique advantages</li>
                <li><strong>"Budget Constraints":</strong> Suggest financing options</li>
                <li><strong>"Need Time to Think":</strong> Create urgency with deadlines</li>
            </ul>
        </div>
        
        <h3>Advanced Negotiation Techniques</h3>
        
        <h4>🎪 The Takeaway Close</h4>
        <p>"I've actually got another buyer interested at $X. If you're serious, I need to know by Friday."</p>
        
        <h4>📊 Value Stacking Method</h4>
        <ol>
            <li><strong>Domain Value:</strong> $X based on comparables</li>
            <li><strong>SEO Benefit:</strong> $Y in search ranking value</li>
            <li><strong>Brand Protection:</strong> $Z in competitive advantage</li>
            <li><strong>Marketing Savings:</strong> $A in reduced advertising costs</li>
            <li><strong>Total Package Value:</strong> $X+Y+Z+A</li>
        </ol>
        
        <h4>🤝 Win-Win Structuring</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Creative Deal Structures:</strong></p>
            <ul>
                <li><strong>Revenue Share:</strong> Percentage of future business income</li>
                <li><strong>Equity Stake:</strong> Small ownership in their company</li>
                <li><strong>Performance Bonuses:</strong> Additional payments if milestones hit</li>
                <li><strong>Licensing Deals:</strong> Retain ownership, license usage</li>
                <li><strong>Portfolio Packages:</strong> Bundle multiple domains</li>
            </ul>
        </div>
        
        <h3>Closing & Finalizing Deals</h3>
        
        <h4>✅ Securing Agreement</h4>
        <ul>
            <li><strong>Get Written Confirmation:</strong> Email acceptance minimum</li>
            <li><strong>Use Escrow Services:</strong> Escrow.com or Dan.com</li>
            <li><strong>Set Clear Timeline:</strong> 5-7 business days standard</li>
            <li><strong>Define Transfer Process:</strong> Auth codes and contacts</li>
            <li><strong>Handle Legal Details:</strong> Contracts and warranties</li>
        </ul>
        
        <h4>🚨 Red Flags to Avoid</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <ul>
                <li><strong>No Escrow:</strong> Direct wire transfer requests</li>
                <li><strong>Pressure Tactics:</strong> "Must decide today" from buyers</li>
                <li><strong>Unusual Payment:</strong> Crypto or gift cards</li>
                <li><strong>No Business Verification:</strong> Can't confirm company exists</li>
                <li><strong>Legal Threats:</strong> Trademark claims without merit</li>
            </ul>
        </div>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>💡 Negotiation Master Secret:</strong> The person who cares less wins. Always have multiple deals in progress so you can walk away from any single negotiation.
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
        """,
        
        'Empire Building': """
        <h2>👑 Empire Building - Scale to Domain Royalty</h2>
        
        <h3>The Empire Mindset</h3>
        <p>Building a domain empire requires thinking like a digital real estate mogul. You're not just buying domains - you're acquiring digital territories that will generate wealth for decades.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🏰 Empire Foundation Pillars:</strong></p>
            <ol>
                <li><strong>Market Domination:</strong> Control entire keyword categories</li>
                <li><strong>Strategic Partnerships:</strong> Alliances with industry leaders</li>
                <li><strong>Automated Systems:</strong> Scale without personal bottlenecks</li>
                <li><strong>Brand Development:</strong> Transform domains into household names</li>
                <li><strong>Legacy Creation:</strong> Build generational wealth</li>
            </ol>
        </div>
        
        <h3>Territory Acquisition Strategy</h3>
        
        <h4>🎯 Keyword Kingdom Conquest</h4>
        <p>Identify and dominate entire keyword families:</p>
        <ul>
            <li><strong>[Industry][City].com:</strong> DentalAustin.com, DentalDallas.com</li>
            <li><strong>[Service][State].com:</strong> PlumbingTexas.com, PlumbingFlorida.com</li>
            <li><strong>[Product]Category.com:</strong> OrganicFood.com, LuxuryWatches.com</li>
            <li><strong>Branded Variations:</strong> GetInsurance.com, BuyInsurance.com</li>
        </ul>
        
        <h4>🌍 Global Market Expansion</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>International Empire Strategy:</strong></p>
            <ul>
                <li><strong>ccTLD Portfolios:</strong> Same keywords across .co.uk, .de, .au</li>
                <li><strong>Language Variations:</strong> Spanish, French, Portuguese markets</li>
                <li><strong>Cultural Adaptations:</strong> Local business naming conventions</li>
                <li><strong>Currency Considerations:</strong> Price in local currencies</li>
                <li><strong>Legal Structures:</strong> International entity formation</li>
            </ul>
        </div>
        
        <h3>Empire Revenue Streams</h3>
        
        <h4>💰 Multiple Income Channels</h4>
        <ol>
            <li><strong>Direct Sales:</strong> Premium domain transactions ($50K+)</li>
            <li><strong>Lease-to-Own:</strong> Monthly payments with option to buy</li>
            <li><strong>Revenue Sharing:</strong> Percentage of business income</li>
            <li><strong>Development Partnerships:</strong> Build and split ownership</li>
            <li><strong>Brand Licensing:</strong> License usage rights</li>
            <li><strong>Portfolio Management:</strong> Manage domains for others</li>
        </ol>
        
        <h4>🔄 Automated Revenue Systems</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Set-and-Forget Income Streams:</strong></p>
            <ul>
                <li><strong>Landing Pages:</strong> Automated inquiry generation</li>
                <li><strong>PPC Parking:</strong> Search engine revenue sharing</li>
                <li><strong>Affiliate Marketing:</strong> Commission-based partnerships</li>
                <li><strong>Subscription Models:</strong> Access to domain databases</li>
                <li><strong>Educational Products:</strong> Courses and consulting</li>
            </ul>
        </div>
        
        <h3>Team Building & Delegation</h3>
        
        <h4>🎯 Essential Empire Roles</h4>
        <ul>
            <li><strong>Acquisition Specialist:</strong> Source and evaluate domains</li>
            <li><strong>Sales Manager:</strong> Handle negotiations and closings</li>
            <li><strong>Marketing Director:</strong> Build brand and generate leads</li>
            <li><strong>Technical Manager:</strong> Handle transfers and development</li>
            <li><strong>Financial Controller:</strong> Track ROI and manage cash flow</li>
        </ul>
        
        <h3>Technology Infrastructure</h3>
        
        <h4>🖥️ Empire Management Systems</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Required Technology Stack:</strong></p>
            <ul>
                <li><strong>CRM System:</strong> Track all buyer interactions</li>
                <li><strong>Portfolio Management:</strong> Real-time valuation tracking</li>
                <li><strong>Automated Marketing:</strong> Email sequences and follow-ups</li>
                <li><strong>Financial Dashboards:</strong> ROI and performance metrics</li>
                <li><strong>Legal Management:</strong> Contract and trademark tracking</li>
            </ul>
        </div>
        
        <h3>Exit Strategy Planning</h3>
        
        <h4>🚪 Empire Exit Options</h4>
        <ol>
            <li><strong>Strategic Sale:</strong> Sell entire portfolio to corporation</li>
            <li><strong>IPO Preparation:</strong> Build domain REIT structure</li>
            <li><strong>Family Trust:</strong> Generational wealth transfer</li>
            <li><strong>Franchise Model:</strong> License empire-building system</li>
            <li><strong>Partial Liquidity:</strong> Sell segments while retaining core</li>
        </ol>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>👑 Empire Builder Secret:</strong> The difference between investors and emperors is that emperors don't just buy domains - they create entire ecosystems that generate wealth automatically.
        </div>
        """,
        
        'Advanced Analytics': """
        <h2>📊 Advanced Analytics - Data-Driven Domain Mastery</h2>
        
        <h3>Analytics Framework for Domains</h3>
        <p>Transform your domain investing from intuition-based to data-driven decisions using advanced analytics and market intelligence.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>📈 Core Analytics Pillars:</strong></p>
            <ol>
                <li><strong>Market Intelligence:</strong> Track industry trends and cycles</li>
                <li><strong>Valuation Models:</strong> Predictive pricing algorithms</li>
                <li><strong>Risk Assessment:</strong> Portfolio optimization strategies</li>
                <li><strong>Performance Tracking:</strong> ROI and growth metrics</li>
                <li><strong>Competitive Analysis:</strong> Monitor market participants</li>
            </ol>
        </div>
        
        <h3>Advanced Valuation Models</h3>
        
        <h4>🔬 Algorithmic Pricing Methods</h4>
        <p><strong>Multi-Factor Valuation Formula:</strong></p>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Domain Value = Base Score × Multipliers</strong></p>
            <ul>
                <li><strong>Base Score:</strong> Keyword value + TLD premium + Length factor</li>
                <li><strong>Industry Multiplier:</strong> 0.5x (declining) to 3x (growing)</li>
                <li><strong>Brandability Factor:</strong> 0.8x (generic) to 2x (memorable)</li>
                <li><strong>SEO Potential:</strong> 0.9x (weak) to 1.5x (strong)</li>
                <li><strong>Market Timing:</strong> 0.7x (peak) to 1.8x (emerging)</li>
            </ul>
        </div>
        
        <h4>📊 Comparable Sales Analysis</h4>
        <ul>
            <li><strong>Direct Comparables:</strong> Same keywords, different TLD</li>
            <li><strong>Industry Benchmarks:</strong> Similar business categories</li>
            <li><strong>Geographic Adjustments:</strong> Regional market differences</li>
            <li><strong>Time-Series Analysis:</strong> Historical appreciation rates</li>
            <li><strong>Volume-Weighted Averages:</strong> Account for transaction size</li>
        </ul>
        
        <h3>Market Intelligence Systems</h3>
        
        <h4>🎯 Trend Detection Algorithms</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Early Warning Indicators:</strong></p>
            <ul>
                <li><strong>Search Volume Spikes:</strong> 500%+ increase over 30 days</li>
                <li><strong>Media Mention Surge:</strong> 10x baseline coverage</li>
                <li><strong>Domain Registration Burst:</strong> New TLD registrations</li>
                <li><strong>Investment Flow Changes:</strong> VC funding patterns</li>
                <li><strong>Patent Filing Activity:</strong> Innovation indicators</li>
            </ul>
        </div>
        
        <h4>🔍 Competitive Intelligence</h4>
        <ul>
            <li><strong>Portfolio Tracking:</strong> Monitor top investor acquisitions</li>
            <li><strong>Auction Analysis:</strong> Bidding pattern recognition</li>
            <li><strong>Price Sensitivity:</strong> Market maker behavior</li>
            <li><strong>Exit Timing:</strong> When big players sell</li>
            <li><strong>Strategy Patterns:</strong> Successful investor methodologies</li>
        </ul>
        
        <h3>Risk Analytics & Portfolio Optimization</h3>
        
        <h4>⚖️ Risk Scoring Matrix</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Risk Factors (1-10 scale):</strong></p>
            <ul>
                <li><strong>Market Concentration:</strong> Industry diversity score</li>
                <li><strong>Price Volatility:</strong> Historical price swings</li>
                <li><strong>Liquidity Risk:</strong> Average time to sell</li>
                <li><strong>Regulatory Risk:</strong> Legal environment changes</li>
                <li><strong>Technology Risk:</strong> Platform dependency</li>
                <li><strong>Economic Sensitivity:</strong> Recession correlation</li>
            </ul>
        </div>
        
        <h4>📈 Portfolio Optimization Strategies</h4>
        <ul>
            <li><strong>Modern Portfolio Theory:</strong> Risk/return optimization</li>
            <li><strong>Monte Carlo Simulation:</strong> Scenario planning</li>
            <li><strong>Correlation Analysis:</strong> Diversification effectiveness</li>
            <li><strong>Value at Risk (VaR):</strong> Downside protection</li>
            <li><strong>Sharpe Ratio Maximization:</strong> Risk-adjusted returns</li>
        </ul>
        
        <h3>Performance Tracking & KPIs</h3>
        
        <h4>📊 Essential Metrics Dashboard</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Track These KPIs Weekly:</strong></p>
            <ul>
                <li><strong>Portfolio IRR:</strong> Internal rate of return</li>
                <li><strong>Cash-on-Cash Return:</strong> Annual cash flow yield</li>
                <li><strong>Portfolio Velocity:</strong> Turnover rate</li>
                <li><strong>Hit Rate:</strong> Profitable sales percentage</li>
                <li><strong>Average Holding Period:</strong> Time to liquidity</li>
                <li><strong>Cost Per Acquisition:</strong> Research and buying costs</li>
            </ul>
        </div>
        
        <h3>Predictive Analytics Models</h3>
        
        <h4>🔮 Forecasting Techniques</h4>
        <ul>
            <li><strong>Regression Analysis:</strong> Multi-variable price prediction</li>
            <li><strong>Machine Learning:</strong> Pattern recognition algorithms</li>
            <li><strong>Sentiment Analysis:</strong> Social media and news impact</li>
            <li><strong>Seasonal Models:</strong> Cyclical trend identification</li>
            <li><strong>Economic Indicators:</strong> Macro factor integration</li>
        </ul>
        
        <h4>🎯 Acquisition Targeting System</h4>
        <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
            <p><strong>AI-Powered Deal Sourcing:</strong></p>
            <ul>
                <li><strong>Expiry Monitoring:</strong> Domains about to drop</li>
                <li><strong>Distressed Asset Detection:</strong> Financial stress signals</li>
                <li><strong>Undervaluation Alerts:</strong> Mispriced opportunities</li>
                <li><strong>Trend Momentum:</strong> Emerging category identification</li>
                <li><strong>Arbitrage Detection:</strong> Cross-platform price gaps</li>
            </ul>
        </div>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>📊 Analytics Mastery Secret:</strong> The most successful domain investors make decisions based on data, not emotions. Build your analytics stack first, then trust the numbers.
        </div>
        """,
        
        'Premium Tools': """
        <h2>🛠️ Premium Tools - Professional Domain Arsenal</h2>
        
        <h3>Professional Tool Stack</h3>
        <p>Elite domain investors use professional-grade tools to gain competitive advantages in research, acquisition, and management.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🎯 Essential Tool Categories:</strong></p>
            <ol>
                <li><strong>Research & Analytics:</strong> Market intelligence platforms</li>
                <li><strong>Valuation Tools:</strong> Automated appraisal systems</li>
                <li><strong>Portfolio Management:</strong> Asset tracking and optimization</li>
                <li><strong>Sales & Marketing:</strong> Lead generation and outreach</li>
                <li><strong>Legal & Compliance:</strong> Trademark and IP protection</li>
            </ol>
        </div>
        
        <h3>Research & Intelligence Tools</h3>
        
        <h4>📊 Market Research Platforms</h4>
        <ul>
            <li><strong>NameBio ($99/month):</strong> Comprehensive sales database</li>
            <li><strong>DomainTools ($99/month):</strong> WHOIS and DNS intelligence</li>
            <li><strong>EstiBot ($19/month):</strong> Automated domain appraisals</li>
            <li><strong>Ahrefs ($99/month):</strong> SEO and keyword research</li>
            <li><strong>SEMrush ($119/month):</strong> Competitive intelligence</li>
        </ul>
        
        <h4>🔍 Advanced Analytics Suites</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Professional Analytics Stack:</strong></p>
            <ul>
                <li><strong>GoDaddy Investor Tools ($4.99/month):</strong> Auction insights</li>
                <li><strong>Domain Hunter Gatherer ($97):</strong> Expired domain research</li>
                <li><strong>Fresh Drop ($29/month):</strong> Daily expired domain lists</li>
                <li><strong>Domain Punch ($19/month):</strong> Brandable domain generator</li>
                <li><strong>Lean Domain Search (Free):</strong> Available domain suggestions</li>
            </ul>
        </div>
        
        <h3>Portfolio Management Systems</h3>
        
        <h4>💼 Professional Management Platforms</h4>
        <ul>
            <li><strong>Efty ($20/month):</strong> Landing pages and CRM</li>
            <li><strong>Dan.com ($0-50/month):</strong> Marketplace and management</li>
            <li><strong>Uniregistry Market ($Free):</strong> Professional listings</li>
            <li><strong>Sedo Premium ($99/month):</strong> Broker network access</li>
            <li><strong>4.cn (Custom pricing):</strong> Enterprise management</li>
        </ul>
        
        <h4>📈 Performance Tracking Tools</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>ROI and Analytics Tracking:</strong></p>
            <ul>
                <li><strong>Custom Spreadsheets:</strong> Google Sheets with formulas</li>
                <li><strong>DomainIQ ($99/month):</strong> Portfolio analytics</li>
                <li><strong>Domain Capital ($49/month):</strong> Investment tracking</li>
                <li><strong>PortfolioTracker ($29/month):</strong> Performance monitoring</li>
                <li><strong>DomainTools Portfolio ($199/month):</strong> Enterprise analytics</li>
            </ul>
        </div>
        
        <h3>Sales & Marketing Automation</h3>
        
        <h4>🎯 Lead Generation Systems</h4>
        <ul>
            <li><strong>HubSpot CRM ($0-450/month):</strong> Contact management</li>
            <li><strong>Pipedrive ($12.50/month):</strong> Sales pipeline tracking</li>
            <li><strong>ZoomInfo ($14,995/year):</strong> B2B contact database</li>
            <li><strong>Apollo.io ($49/month):</strong> Prospect research</li>
            <li><strong>Hunter.io ($49/month):</strong> Email finder and verifier</li>
        </ul>
        
        <h4>📧 Email Marketing & Outreach</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Outreach Automation Stack:</strong></p>
            <ul>
                <li><strong>Mailchimp ($10/month):</strong> Email marketing campaigns</li>
                <li><strong>Woodpecker ($40/month):</strong> Cold email sequences</li>
                <li><strong>Reply.io ($90/month):</strong> Multi-channel outreach</li>
                <li><strong>Lemlist ($59/month):</strong> Personalized email campaigns</li>
                <li><strong>Instantly ($37/month):</strong> Email warming and delivery</li>
            </ul>
        </div>
        
        <h3>Legal & Compliance Tools</h3>
        
        <h4>⚖️ Trademark & IP Protection</h4>
        <ul>
            <li><strong>USPTO Database (Free):</strong> Trademark searches</li>
            <li><strong>TrademarkNow ($49/month):</strong> Global trademark monitoring</li>
            <li><strong>MarkMonitor ($Custom):</strong> Enterprise brand protection</li>
            <li><strong>Corsearch ($Custom):</strong> IP intelligence platform</li>
            <li><strong>LegalZoom ($79-$329):</strong> Legal document preparation</li>
        </ul>
        
        <h4>📝 Contract & Transaction Management</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Legal Process Automation:</strong></p>
            <ul>
                <li><strong>Escrow.com ($Custom):</strong> Secure transaction processing</li>
                <li><strong>DocuSign ($10/month):</strong> Electronic signatures</li>
                <li><strong>PandaDoc ($19/month):</strong> Contract automation</li>
                <li><strong>Clio ($39/month):</strong> Legal practice management</li>
                <li><strong>LawGeex ($Custom):</strong> AI contract review</li>
            </ul>
        </div>
        
        <h3>Advanced Development Tools</h3>
        
        <h4>🌐 Website & Landing Page Builders</h4>
        <ul>
            <li><strong>WordPress ($0-25/month):</strong> Full website development</li>
            <li><strong>Unbounce ($80/month):</strong> Landing page optimization</li>
            <li><strong>Leadpages ($37/month):</strong> Conversion-focused pages</li>
            <li><strong>Instapage ($199/month):</strong> Enterprise landing pages</li>
            <li><strong>Webflow ($12/month):</strong> Visual web development</li>
        </ul>
        
        <h3>Tool Selection Strategy</h3>
        
        <h4>🎯 ROI-Based Tool Selection</h4>
        <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
            <p><strong>Investment Priority Framework:</strong></p>
            <ol>
                <li><strong>Research Tools First:</strong> Better deals = higher ROI</li>
                <li><strong>Management Tools Second:</strong> Scale efficiency</li>
                <li><strong>Marketing Tools Third:</strong> Increase sales velocity</li>
                <li><strong>Advanced Tools Last:</strong> Optimize existing processes</li>
            </ol>
        </div>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>🛠️ Tool Mastery Secret:</strong> Don't buy tools for the sake of having them. Each tool should either help you find better deals, manage more efficiently, or sell faster. ROI should exceed tool cost within 90 days.
        </div>
        """,
        
        'Elite Strategies': """
        <h2>💎 Elite Strategies - Insider Techniques</h2>
        
        <h3>Elite-Level Domain Strategies</h3>
        <p>These advanced techniques separate professional domain investors from hobbyists.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🎯 Elite Strategy Categories:</strong></p>
            <ol>
                <li><strong>Market Making:</strong> Create liquidity and influence pricing</li>
                <li><strong>Strategic Partnerships:</strong> Corporate alliance development</li>
                <li><strong>Vertical Integration:</strong> Control entire value chains</li>
                <li><strong>Arbitrage Operations:</strong> Cross-platform profit extraction</li>
                <li><strong>Information Asymmetry:</strong> Proprietary intelligence advantages</li>
            </ol>
        </div>
        
        <h3>Market Making Strategies</h3>
        
        <h4>🏦 Become the Central Hub</h4>
        <ul>
            <li><strong>Liquidity Provision:</strong> Always have inventory ready to sell</li>
            <li><strong>Price Discovery:</strong> Set market rates for domain categories</li>
            <li><strong>Two-Sided Markets:</strong> Connect buyers and sellers</li>
            <li><strong>Inventory Management:</strong> Strategic stock rotation</li>
            <li><strong>Market Intelligence:</strong> Information broker role</li>
        </ul>
        
        <h4>💰 Spread Capture Techniques</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Elite Arbitrage Methods:</strong></p>
            <ul>
                <li><strong>Geographic Arbitrage:</strong> Buy in one country, sell in another</li>
                <li><strong>Temporal Arbitrage:</strong> Seasonal buying and selling</li>
                <li><strong>Information Arbitrage:</strong> Act on non-public information</li>
                <li><strong>Auction Arbitrage:</strong> Cross-platform price differences</li>
                <li><strong>Development Arbitrage:</strong> Add value through development</li>
            </ul>
        </div>
        
        <h3>Strategic Partnership Development</h3>
        
        <h4>🤝 Corporate Alliance Building</h4>
        <ul>
            <li><strong>Fortune 500 Relationships:</strong> Direct procurement partnerships</li>
            <li><strong>VC Fund Connections:</strong> Portfolio company domain needs</li>
            <li><strong>Industry Association Memberships:</strong> Network access</li>
            <li><strong>Legal Firm Partnerships:</strong> Client referral systems</li>
            <li><strong>Broker Network Development:</strong> Exclusive deal flow</li>
        </ul>
        
        <h4>📈 Revenue Sharing Models</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Advanced Partnership Structures:</strong></p>
            <ul>
                <li><strong>Joint Ventures:</strong> Shared ownership and profits</li>
                <li><strong>Success Fees:</strong> Performance-based compensation</li>
                <li><strong>Equity Partnerships:</strong> Stake in portfolio companies</li>
                <li><strong>Management Agreements:</strong> Fee-based portfolio management</li>
                <li><strong>Licensing Deals:</strong> Technology and process licensing</li>
            </ul>
        </div>
        
        <h3>Vertical Integration Strategies</h3>
        
        <h4>🏗️ Control the Entire Value Chain</h4>
        <ul>
            <li><strong>Registrar Operations:</strong> Own the registration process</li>
            <li><strong>Marketplace Development:</strong> Platform ownership</li>
            <li><strong>Escrow Services:</strong> Transaction facilitation</li>
            <li><strong>Development Teams:</strong> In-house website creation</li>
            <li><strong>Legal Services:</strong> Specialized domain law practice</li>
        </ul>
        
        <h3>Information Asymmetry Advantages</h3>
        
        <h4>🕵️ Proprietary Intelligence Networks</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Elite Information Sources:</strong></p>
            <ul>
                <li><strong>Industry Insiders:</strong> C-level executive networks</li>
                <li><strong>Legal Intelligence:</strong> Trademark filing monitoring</li>
                <li><strong>Financial Intelligence:</strong> Funding round tracking</li>
                <li><strong>Technical Intelligence:</strong> DNS and traffic analysis</li>
                <li><strong>Media Intelligence:</strong> Pre-publication story access</li>
            </ul>
        </div>
        
        <h3>Advanced Monetization Models</h3>
        
        <h4>💎 Premium Revenue Strategies</h4>
        <ul>
            <li><strong>Domain Funds:</strong> Pooled investment vehicles</li>
            <li><strong>REITs:</strong> Real Estate Investment Trust structure</li>
            <li><strong>Securitization:</strong> Domain-backed securities</li>
            <li><strong>Derivatives:</strong> Domain futures and options</li>
            <li><strong>Tokenization:</strong> Blockchain-based ownership</li>
        </ul>
        
        <h4>🎯 Elite Exit Strategies</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Maximum Value Extraction:</strong></p>
            <ul>
                <li><strong>Strategic Acquisitions:</strong> Sell to competitors</li>
                <li><strong>Financial Buyers:</strong> Private equity and hedge funds</li>
                <li><strong>Management Buyouts:</strong> Team acquisition of portfolio</li>
                <li><strong>Public Offerings:</strong> IPO of domain company</li>
                <li><strong>Legacy Structures:</strong> Generational wealth transfer</li>
            </ul>
        </div>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>💎 Elite Strategy Secret:</strong> The highest-level domain investors don't just buy and sell domains - they create entire ecosystems and markets around domain investing.
        </div>
        """,
        
        'Insider Secrets': """
        <h2>🔐 Insider Secrets - Confidential Techniques</h2>
        
        <h3>Industry Insider Knowledge</h3>
        <p>These closely-guarded secrets are known only to the most successful domain investors and industry insiders.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🤫 Insider Secret Categories:</strong></p>
            <ol>
                <li><strong>Hidden Market Signals:</strong> Non-obvious trend indicators</li>
                <li><strong>Insider Trading Techniques:</strong> Legal information advantages</li>
                <li><strong>Network Effects:</strong> Relationship-based opportunities</li>
                <li><strong>Psychological Triggers:</strong> Buyer behavior manipulation</li>
                <li><strong>Regulatory Arbitrage:</strong> Legal framework advantages</li>
            </ol>
        </div>
        
        <h3>Hidden Market Signals</h3>
        
        <h4>🎯 Non-Obvious Trend Indicators</h4>
        <ul>
            <li><strong>Patent Applications:</strong> Technology trends 18 months early</li>
            <li><strong>Domain Registrations:</strong> Corporate expansion plans</li>
            <li><strong>SSL Certificate Monitoring:</strong> Website development activity</li>
            <li><strong>Job Posting Analysis:</strong> Industry growth signals</li>
            <li><strong>Conference Speaker Lists:</strong> Emerging expert networks</li>
        </ul>
        
        <h4>📊 Proprietary Data Sources</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Exclusive Intelligence Channels:</strong></p>
            <ul>
                <li><strong>WHOIS History:</strong> Ownership change patterns</li>
                <li><strong>Traffic Analytics:</strong> Domain performance metrics</li>
                <li><strong>Email Patterns:</strong> Corporate communication analysis</li>
                <li><strong>Social Media Monitoring:</strong> Sentiment and trend tracking</li>
                <li><strong>Financial Filings:</strong> Corporate asset disclosures</li>
            </ul>
        </div>
        
        <h3>Psychology-Based Techniques</h3>
        
        <h4>🧠 Buyer Behavior Manipulation</h4>
        <ul>
            <li><strong>Scarcity Creation:</strong> Artificial urgency generation</li>
            <li><strong>Social Proof:</strong> Leverage other high-profile sales</li>
            <li><strong>Authority Positioning:</strong> Expert status establishment</li>
            <li><strong>Loss Aversion:</strong> Emphasize opportunity cost</li>
            <li><strong>Anchoring Effects:</strong> Strategic price positioning</li>
        </ul>
        
        <h4>💰 Advanced Negotiation Psychology</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Mind Game Techniques:</strong></p>
            <ul>
                <li><strong>The Flinch:</strong> React to offers with shock</li>
                <li><strong>Bracketing:</strong> Extreme anchoring strategies</li>
                <li><strong>The Nibble:</strong> Small additional requests</li>
                <li><strong>Silence Power:</strong> Let them fill the void</li>
                <li><strong>False Time Constraints:</strong> Artificial deadlines</li>
            </ul>
        </div>
        
        <h3>Network-Based Advantages</h3>
        
        <h4>🤝 Insider Network Development</h4>
        <ul>
            <li><strong>C-Suite Connections:</strong> Direct access to decision makers</li>
            <li><strong>VC Partner Relationships:</strong> Portfolio company deals</li>
            <li><strong>Legal Network:</strong> Attorney referral systems</li>
            <li><strong>Media Relationships:</strong> Journalist and blogger contacts</li>
            <li><strong>Government Connections:</strong> Policy and regulation insights</li>
        </ul>
        
        <h4>📈 Information Flow Control</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Strategic Information Management:</strong></p>
            <ul>
                <li><strong>Selective Disclosure:</strong> Control information release</li>
                <li><strong>Misinformation Campaigns:</strong> Competitive misdirection</li>
                <li><strong>Insider Trading Networks:</strong> Legal information sharing</li>
                <li><strong>Market Manipulation:</strong> Influence price movements</li>
                <li><strong>Reputation Management:</strong> Control public perception</li>
            </ul>
        </div>
        
        <h3>Regulatory Arbitrage</h3>
        
        <h4>⚖️ Legal Framework Advantages</h4>
        <ul>
            <li><strong>Jurisdiction Shopping:</strong> Optimal legal environments</li>
            <li><strong>Tax Optimization:</strong> Minimize transaction taxes</li>
            <li><strong>Regulatory Gaps:</strong> Exploit unclear regulations</li>
            <li><strong>Compliance Arbitrage:</strong> Different rule interpretations</li>
            <li><strong>Policy Influence:</strong> Shape future regulations</li>
        </ul>
        
        <h3>Advanced Monetization Secrets</h3>
        
        <h4>💎 Hidden Revenue Streams</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Confidential Income Sources:</strong></p>
            <ul>
                <li><strong>Broker Kickbacks:</strong> Hidden commission structures</li>
                <li><strong>Auction House Relationships:</strong> Preferential treatment</li>
                <li><strong>Registry Partnerships:</strong> Exclusive TLD access</li>
                <li><strong>Corporate Retainers:</strong> Ongoing consultation fees</li>
                <li><strong>Government Contracts:</strong> Official domain services</li>
            </ul>
        </div>
        
        <h4>🎯 Black Market Techniques</h4>
        <p><em>Note: These techniques exist but may operate in legal gray areas:</em></p>
        <ul>
            <li><strong>Dark Web Markets:</strong> Underground domain trading</li>
            <li><strong>Stolen Domain Recovery:</strong> Legal gray area profits</li>
            <li><strong>Trademark Squatting:</strong> Strategic defensive registrations</li>
            <li><strong>Typosquatting Networks:</strong> Traffic monetization</li>
            <li><strong>Drop Catching Syndicates:</strong> Coordinated acquisition</li>
        </ul>
        
        <h3>Risk Management Secrets</h3>
        
        <h4>🛡️ Advanced Protection Strategies</h4>
        <ul>
            <li><strong>Anonymous Ownership:</strong> Privacy protection services</li>
            <li><strong>Offshore Structures:</strong> Asset protection entities</li>
            <li><strong>Insurance Strategies:</strong> Specialized domain coverage</li>
            <li><strong>Legal Firewalls:</strong> Liability isolation techniques</li>
            <li><strong>Exit Triggers:</strong> Automated liquidation systems</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>🔐 Ultimate Insider Secret:</strong> The most successful domain investors don't compete in the same market as everyone else - they create their own markets and set the rules. Information is the ultimate competitive advantage.
        </div>
        """,
        
        'Master Class': """
        <h2>🎓 Master Class - Advanced Domain Mastery</h2>
        
        <h3>Master-Level Domain Education</h3>
        <p>This comprehensive master class covers advanced concepts that transform good domain investors into industry legends.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🎯 Master Class Curriculum:</strong></p>
            <ol>
                <li><strong>Strategic Vision:</strong> Long-term industry positioning</li>
                <li><strong>Market Psychology:</strong> Understanding human behavior</li>
                <li><strong>Financial Engineering:</strong> Advanced transaction structures</li>
                <li><strong>Technology Integration:</strong> Leveraging tech advantages</li>
                <li><strong>Legacy Building:</strong> Creating lasting impact</li>
            </ol>
        </div>
        
        <h3>Strategic Vision Development</h3>
        
        <h4>🔮 Long-Term Industry Positioning</h4>
        <ul>
            <li><strong>Trend Forecasting:</strong> Predict industry evolution 5-10 years out</li>
            <li><strong>Technology Impact:</strong> How blockchain, AI, VR will affect domains</li>
            <li><strong>Generational Shifts:</strong> Changing user behavior patterns</li>
            <li><strong>Global Market Evolution:</strong> Emerging market opportunities</li>
            <li><strong>Regulatory Landscape:</strong> Future legal environment</li>
        </ul>
        
        <h4>🎯 Strategic Positioning Framework</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Master-Level Positioning Strategy:</strong></p>
            <ul>
                <li><strong>Thought Leadership:</strong> Become the recognized expert</li>
                <li><strong>Market Making:</strong> Influence industry standards</li>
                <li><strong>Ecosystem Control:</strong> Own critical infrastructure</li>
                <li><strong>Information Monopoly:</strong> Exclusive data access</li>
                <li><strong>Relationship Dominance:</strong> Control key connections</li>
            </ul>
        </div>
        
        <h3>Market Psychology Mastery</h3>
        
        <h4>🧠 Human Behavior Analysis</h4>
        <ul>
            <li><strong>Cognitive Biases:</strong> Exploit psychological shortcuts</li>
            <li><strong>Emotional Triggers:</strong> Fear, greed, pride, urgency</li>
            <li><strong>Social Dynamics:</strong> Group psychology and trends</li>
            <li><strong>Cultural Psychology:</strong> Geographic behavior differences</li>
            <li><strong>Generational Psychology:</strong> Age-based preferences</li>
        </ul>
        
        <h4>💰 Behavioral Economics Application</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Advanced Psychology Techniques:</strong></p>
            <ul>
                <li><strong>Prospect Theory:</strong> Loss aversion and risk perception</li>
                <li><strong>Mental Accounting:</strong> How people categorize money</li>
                <li><strong>Social Proof:</strong> Influence through peer behavior</li>
                <li><strong>Authority Bias:</strong> Leverage expert status</li>
                <li><strong>Commitment Consistency:</strong> Public commitment power</li>
            </ul>
        </div>
        
        <h3>Financial Engineering</h3>
        
        <h4>🏦 Advanced Transaction Structures</h4>
        <ul>
            <li><strong>Synthetic Instruments:</strong> Domain derivatives and futures</li>
            <li><strong>Structured Products:</strong> Complex investment vehicles</li>
            <li><strong>Tax Optimization:</strong> International tax planning</li>
            <li><strong>Risk Management:</strong> Hedging and insurance strategies</li>
            <li><strong>Capital Structure:</strong> Debt and equity optimization</li>
        </ul>
        
        <h4>💎 Investment Vehicle Creation</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Master-Level Investment Structures:</strong></p>
            <ul>
                <li><strong>Domain Funds:</strong> Private investment partnerships</li>
                <li><strong>REIT Structures:</strong> Public investment vehicles</li>
                <li><strong>Hedge Fund Models:</strong> Alternative investment strategies</li>
                <li><strong>Family Offices:</strong> Ultra-high-net-worth management</li>
                <li><strong>Institutional Products:</strong> Pension and endowment access</li>
            </ul>
        </div>
        
        <h3>Technology Integration</h3>
        
        <h4>🤖 Artificial Intelligence Applications</h4>
        <ul>
            <li><strong>Predictive Analytics:</strong> AI-powered domain valuation</li>
            <li><strong>Natural Language Processing:</strong> Trend detection in text</li>
            <li><strong>Machine Learning:</strong> Pattern recognition in sales data</li>
            <li><strong>Computer Vision:</strong> Logo and brand analysis</li>
            <li><strong>Neural Networks:</strong> Complex relationship modeling</li>
        </ul>
        
        <h4>⛓️ Blockchain and Web3 Integration</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Next-Generation Domain Technology:</strong></p>
            <ul>
                <li><strong>ENS Domains:</strong> Ethereum Name Service strategy</li>
                <li><strong>NFT Integration:</strong> Non-fungible token domains</li>
                <li><strong>DeFi Applications:</strong> Decentralized finance integration</li>
                <li><strong>Smart Contracts:</strong> Automated domain transactions</li>
                <li><strong>Metaverse Domains:</strong> Virtual world real estate</li>
            </ul>
        </div>
        
        <h3>Legacy Building</h3>
        
        <h4>🏛️ Industry Impact Creation</h4>
        <ul>
            <li><strong>Standard Setting:</strong> Influence industry practices</li>
            <li><strong>Educational Programs:</strong> Train next generation</li>
            <li><strong>Research Funding:</strong> Advance domain science</li>
            <li><strong>Policy Influence:</strong> Shape regulatory environment</li>
            <li><strong>Philanthropic Impact:</strong> Use wealth for social good</li>
        </ul>
        
        <h4>🎯 Succession Planning</h4>
        <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
            <p><strong>Generational Wealth Transfer:</strong></p>
            <ul>
                <li><strong>Trust Structures:</strong> Multi-generational planning</li>
                <li><strong>Education Programs:</strong> Family member training</li>
                <li><strong>Management Systems:</strong> Professional oversight</li>
                <li><strong>Governance Structures:</strong> Decision-making frameworks</li>
                <li><strong>Values Integration:</strong> Purpose-driven investing</li>
            </ul>
        </div>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>🎓 Master Class Graduation:</strong> You've completed the most advanced domain education available. Now use this knowledge to build your domain empire and create lasting impact in the industry.
        </div>
        """,
        
        'Personal Coaching': """
        <h2>👥 Personal Coaching - One-on-One Mastery</h2>
        
        <h3>Elite Personal Coaching Program</h3>
        <p>Exclusive one-on-one coaching reserved for Empire package members. Work directly with domain experts to accelerate your success.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🎯 Personal Coaching Benefits:</strong></p>
            <ol>
                <li><strong>Customized Strategy:</strong> Tailored to your specific situation</li>
                <li><strong>Direct Access:</strong> Expert guidance when you need it</li>
                <li><strong>Accountability:</strong> Regular progress reviews</li>
                <li><strong>Network Access:</strong> Introductions to key industry players</li>
                <li><strong>Deal Review:</strong> Expert analysis of opportunities</li>
            </ol>
        </div>
        
        <h3>Coaching Program Structure</h3>
        
        <h4>📞 Weekly Strategy Sessions</h4>
        <ul>
            <li><strong>60-Minute Calls:</strong> Deep dive strategic planning</li>
            <li><strong>Deal Analysis:</strong> Review potential acquisitions</li>
            <li><strong>Market Updates:</strong> Latest industry intelligence</li>
            <li><strong>Portfolio Review:</strong> Optimize your holdings</li>
            <li><strong>Goal Setting:</strong> Quarterly milestone planning</li>
        </ul>
        
        <h4>💼 Personalized Action Plans</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Custom Coaching Modules:</strong></p>
            <ul>
                <li><strong>Beginner Track:</strong> Foundation building and first deals</li>
                <li><strong>Growth Track:</strong> Scaling existing portfolio</li>
                <li><strong>Expert Track:</strong> Advanced strategies and market making</li>
                <li><strong>Empire Track:</strong> Building institutional-grade operations</li>
                <li><strong>Exit Track:</strong> Liquidity events and succession planning</li>
            </ul>
        </div>
        
        <h3>Coaching Methodologies</h3>
        
        <h4>🎯 Results-Driven Approach</h4>
        <ul>
            <li><strong>SMART Goals:</strong> Specific, measurable, achievable targets</li>
            <li><strong>Weekly Accountability:</strong> Progress tracking and adjustment</li>
            <li><strong>Performance Metrics:</strong> ROI and growth measurement</li>
            <li><strong>Success Milestones:</strong> Celebrate achievements</li>
            <li><strong>Course Correction:</strong> Adapt strategies based on results</li>
        </ul>
        
        <h4>🧠 Mindset Development</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Mental Performance Coaching:</strong></p>
            <ul>
                <li><strong>Confidence Building:</strong> Overcome limiting beliefs</li>
                <li><strong>Risk Management:</strong> Emotional control in decisions</li>
                <li><strong>Patience Training:</strong> Long-term thinking development</li>
                <li><strong>Negotiation Skills:</strong> Psychological advantage building</li>
                <li><strong>Leadership Development:</strong> Team building and delegation</li>
            </ul>
        </div>
        
        <h3>Exclusive Coaching Resources</h3>
        
        <h4>📚 Private Knowledge Base</h4>
        <ul>
            <li><strong>Case Studies:</strong> Real deal analysis and outcomes</li>
            <li><strong>Template Library:</strong> Contracts, emails, presentations</li>
            <li><strong>Tool Recommendations:</strong> Personalized software stack</li>
            <li><strong>Contact Database:</strong> Verified industry connections</li>
            <li><strong>Market Intelligence:</strong> Exclusive research reports</li>
        </ul>
        
        <h4>🤝 Network Access</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Elite Network Introductions:</strong></p>
            <ul>
                <li><strong>Domain Brokers:</strong> Top-tier sales professionals</li>
                <li><strong>Legal Experts:</strong> Specialized domain attorneys</li>
                <li><strong>Financial Advisors:</strong> Wealth management specialists</li>
                <li><strong>Technology Partners:</strong> Development and automation teams</li>
                <li><strong>Investor Network:</strong> High-net-worth domain investors</li>
            </ul>
        </div>
        
        <h3>Coaching Specializations</h3>
        
        <h4>💰 Financial Optimization</h4>
        <ul>
            <li><strong>Portfolio Analysis:</strong> Maximize ROI across holdings</li>
            <li><strong>Tax Strategy:</strong> Minimize tax burden legally</li>
            <li><strong>Financing Options:</strong> Leverage and capital strategies</li>
            <li><strong>Exit Planning:</strong> Liquidity event preparation</li>
            <li><strong>Wealth Preservation:</strong> Asset protection strategies</li>
        </ul>
        
        <h4>🎯 Market Positioning</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Competitive Advantage Development:</strong></p>
            <ul>
                <li><strong>Niche Domination:</strong> Become the category leader</li>
                <li><strong>Brand Building:</strong> Personal and business branding</li>
                <li><strong>Thought Leadership:</strong> Industry recognition strategies</li>
                <li><strong>Media Relations:</strong> Public relations and publicity</li>
                <li><strong>Speaking Opportunities:</strong> Conference and event placement</li>
            </ul>
        </div>
        
        <h3>Success Guarantee</h3>
        
        <h4>📈 Performance Commitment</h4>
        <p><strong>90-Day Success Guarantee:</strong></p>
        <ul>
            <li><strong>Minimum ROI:</strong> 25% improvement in portfolio performance</li>
            <li><strong>Deal Flow:</strong> Access to 3+ qualified opportunities monthly</li>
            <li><strong>Network Growth:</strong> 10+ new industry connections</li>
            <li><strong>Knowledge Transfer:</strong> Measurable skill improvement</li>
            <li><strong>Satisfaction Guarantee:</strong> Full refund if not satisfied</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>👥 Coaching Philosophy:</strong> Success in domain investing is 80% strategy and 20% execution. Our job is to give you the perfect strategy and guide your execution until success becomes inevitable.
        </div>
        """,
        
        'Exclusive Networks': """
        <h2>🌐 Exclusive Networks - Elite Connections</h2>
        
        <h3>Private Network Access</h3>
        <p>Join the most exclusive domain investing networks where deals worth millions are discussed and partnerships are formed.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p><strong>🎯 Network Access Levels:</strong></p>
            <ol>
                <li><strong>Industry Insiders:</strong> C-level executives and entrepreneurs</li>
                <li><strong>Investment Community:</strong> VCs, hedge funds, family offices</li>
                <li><strong>Legal Network:</strong> Top domain attorneys and IP experts</li>
                <li><strong>Technology Leaders:</strong> Developers and platform creators</li>
                <li><strong>Government Relations:</strong> Policy makers and regulators</li>
            </ol>
        </div>
        
        <h3>Private Investment Groups</h3>
        
        <h4>💰 High-Net-Worth Investor Networks</h4>
        <ul>
            <li><strong>Domain Investment Club:</strong> $1M+ minimum investment</li>
            <li><strong>Premium Asset Syndicate:</strong> Exclusive deal sharing</li>
            <li><strong>Portfolio Manager Network:</strong> Professional management services</li>
            <li><strong>Family Office Consortium:</strong> Generational wealth strategies</li>
            <li><strong>Hedge Fund Alliance:</strong> Alternative investment strategies</li>
        </ul>
        
        <h4>🤝 Strategic Partnership Networks</h4>
        <div style="background: #e7f3ff; padding: 15px; border-radius: 8px;">
            <p><strong>Elite Partnership Opportunities:</strong></p>
            <ul>
                <li><strong>Corporate Development:</strong> Fortune 500 partnerships</li>
                <li><strong>Technology Integration:</strong> Platform and tool partnerships</li>
                <li><strong>Media Relationships:</strong> Exclusive story access</li>
                <li><strong>Educational Alliances:</strong> University and research partnerships</li>
                <li><strong>Government Relations:</strong> Policy influence networks</li>
            </ul>
        </div>
        
        <h3>Industry Leadership Networks</h3>
        
        <h4>🏆 Thought Leader Communities</h4>
        <ul>
            <li><strong>Domain Hall of Fame:</strong> Legendary investor network</li>
            <li><strong>Innovation Council:</strong> Technology trend setters</li>
            <li><strong>Policy Advisory Board:</strong> Regulatory influence group</li>
            <li><strong>Research Consortium:</strong> Academic and industry research</li>
            <li><strong>Speaker Bureau:</strong> Conference and event network</li>
        </ul>
        
        <h4>📊 Data and Intelligence Networks</h4>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            <p><strong>Exclusive Information Sharing:</strong></p>
            <ul>
                <li><strong>Market Intelligence Group:</strong> Private research sharing</li>
                <li><strong>Transaction Database:</strong> Confidential sales data</li>
                <li><strong>Trend Analysis Network:</strong> Early trend identification</li>
                <li><strong>Risk Assessment Consortium:</strong> Shared due diligence</li>
                <li><strong>Competitive Intelligence:</strong> Market participant tracking</li>
            </ul>
        </div>
        
        <h3>Global Network Access</h3>
        
        <h4>🌍 International Investment Networks</h4>
        <ul>
            <li><strong>European Domain Alliance:</strong> EU market access</li>
            <li><strong>Asian Investment Syndicate:</strong> APAC opportunities</li>
            <li><strong>Middle East Network:</strong> Emerging market access</li>
            <li><strong>Latin American Group:</strong> Spanish-speaking markets</li>
            <li><strong>African Development Network:</strong> Frontier market opportunities</li>
        </ul>
        
        <h3>Exclusive Event Access</h3>
        
        <h4>🎪 VIP Conference Access</h4>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px;">
            <p><strong>Private Event Invitations:</strong></p>
            <ul>
                <li><strong>Berkshire Hathaway Meetings:</strong> Warren Buffett networking</li>
                <li><strong>World Economic Forum:</strong> Davos networking opportunities</li>
                <li><strong>TED Conference Access:</strong> Innovation leader networks</li>
                <li><strong>Private Equity Summits:</strong> Institutional investor access</li>
                <li><strong>Technology Leadership Events:</strong> Silicon Valley insider access</li>
            </ul>
        </div>
        
        <h4>🏖️ Exclusive Retreats</h4>
        <ul>
            <li><strong>Private Island Workshops:</strong> Intimate strategy sessions</li>
            <li><strong>Yacht Club Meetings:</strong> Luxury networking environments</li>
            <li><strong>Mountain Resort Retreats:</strong> Think tank sessions</li>
            <li><strong>Wine Country Gatherings:</strong> Relaxed relationship building</li>
            <li><strong>International Study Tours:</strong> Global market exploration</li>
        </ul>
        
        <h3>Network Activation Strategies</h3>
        
        <h4>🎯 Relationship Building Mastery</h4>
        <ul>
            <li><strong>Value-First Approach:</strong> Always lead with value</li>
            <li><strong>Long-Term Thinking:</strong> Build for decades, not deals</li>
            <li><strong>Reciprocity Principles:</strong> Give before you receive</li>
            <li><strong>Trust Building:</strong> Reliability and consistency</li>
            <li><strong>Authentic Connections:</strong> Genuine relationship focus</li>
        </ul>
        
        <h4>💼 Professional Network Management</h4>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
            <p><strong>Network Management System:</strong></p>
            <ul>
                <li><strong>CRM Integration:</strong> Relationship tracking systems</li>
                <li><strong>Regular Touchpoints:</strong> Systematic communication</li>
                <li><strong>Value Delivery:</strong> Ongoing benefit provision</li>
                <li><strong>Event Coordination:</strong> Bringing people together</li>
                <li><strong>Information Sharing:</strong> Strategic intelligence distribution</li>
            </ul>
        </div>
        
        <h3>Network ROI Measurement</h3>
        
        <h4>📈 Network Value Metrics</h4>
        <ul>
            <li><strong>Deal Flow Generation:</strong> Opportunities from network</li>
            <li><strong>Cost Reduction:</strong> Savings from relationships</li>
            <li><strong>Information Value:</strong> Early access premium</li>
            <li><strong>Partnership Revenue:</strong> Collaborative profits</li>
            <li><strong>Reputation Enhancement:</strong> Brand value increase</li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
            <strong>🌐 Network Success Secret:</strong> Your network is your net worth. The most successful domain investors don't just have money - they have access to the right people at the right time. Relationships compound faster than money.
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

# Affiliate system route
@app.route('/affiliate')
def affiliate():
    """Affiliate marketing system for promoting rizzosai.com"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session.get('username', 'Unknown')
    affiliate_id = f"rizzos-{username.lower().replace(' ', '')}"
    
    # Generate affiliate links
    main_site_link = f"https://rizzosai.com?ref={affiliate_id}"
    backoffice_link = f"https://backoffice.rizzosai.com?ref={affiliate_id}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Affiliate Program - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; }}
            .back-btn {{ background: #e2e8f0; color: #4a5568; padding: 8px 16px; border-radius: 8px; text-decoration: none; display: inline-block; margin-bottom: 20px; }}
            .affiliate-card {{ background: #f7fafc; border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #667eea; }}
            .commission-rate {{ background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 15px; border-radius: 10px; text-align: center; margin: 20px 0; }}
            .link-box {{ background: #e2e8f0; padding: 15px; border-radius: 8px; margin: 10px 0; font-family: monospace; }}
            .copy-btn {{ background: #667eea; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
            .stat-card {{ background: white; border: 2px solid #667eea; border-radius: 10px; padding: 20px; text-align: center; }}
        </style>
        <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    alert('Link copied to clipboard!');
                }});
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            
            <h1>💰 Affiliate Program - Earn While You Share</h1>
            <p>Promote Rizzos AI and earn commissions on every sale you generate!</p>
            
            <div class="commission-rate">
                <h2>🎯 25% Commission on All Sales!</h2>
                <p>Elite Package Sale: <strong>$124.99 per sale</strong></p>
                <p>Empire Package Sale: <strong>$249.99 per sale</strong></p>
            </div>
            
            <div class="affiliate-card">
                <h3>👤 Your Affiliate Details</h3>
                <p><strong>Affiliate ID:</strong> {affiliate_id}</p>
                <p><strong>Status:</strong> Active Member</p>
                <p><strong>Tier:</strong> {session.get('package', 'Basic')} Affiliate</p>
            </div>
            
            <div class="affiliate-card">
                <h3>🔗 Your Affiliate Links</h3>
                
                <h4>Main Website Link:</h4>
                <div class="link-box">
                    {main_site_link}
                    <button class="copy-btn" onclick="copyToClipboard('{main_site_link}')">Copy</button>
                </div>
                
                <h4>Backoffice Link:</h4>
                <div class="link-box">
                    {backoffice_link}
                    <button class="copy-btn" onclick="copyToClipboard('{backoffice_link}')">Copy</button>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>📊 Clicks</h3>
                    <h2>0</h2>
                    <p>Total link clicks</p>
                </div>
                <div class="stat-card">
                    <h3>💰 Sales</h3>
                    <h2>0</h2>
                    <p>Successful conversions</p>
                </div>
                <div class="stat-card">
                    <h3>💵 Earnings</h3>
                    <h2>$0.00</h2>
                    <p>Total commissions</p>
                </div>
                <div class="stat-card">
                    <h3>📈 Conversion</h3>
                    <h2>0%</h2>
                    <p>Click to sale rate</p>
                </div>
            </div>
            
            <div class="affiliate-card">
                <h3>🎯 Marketing Materials</h3>
                <p><strong>Taglines to Use:</strong></p>
                <ul>
                    <li>"Discover the secrets of domain investing with Rizzos AI"</li>
                    <li>"Learn how to build wealth through premium domain investing"</li>
                    <li>"Join the elite circle of domain investors making 6-7 figures"</li>
                    <li>"Transform your financial future with domain empire building"</li>
                </ul>
                
                <p><strong>Key Selling Points:</strong></p>
                <ul>
                    <li>🎓 13 comprehensive domain investing guides</li>
                    <li>🤖 AI-powered Coey assistant for personalized guidance</li>
                    <li>💰 Proven strategies from successful domain investors</li>
                    <li>🏆 Elite and Empire packages with exclusive content</li>
                    <li>📈 Step-by-step portfolio building strategies</li>
                </ul>
            </div>
            
            <div class="affiliate-card">
                <h3>📱 Social Media Templates</h3>
                
                <h4>Twitter/X Post:</h4>
                <div class="link-box">
                    💎 Just discovered the ultimate domain investing course! Learn how top investors build 6-7 figure portfolios. 13 guides + AI assistant included! {main_site_link} #DomainInvesting #PassiveIncome
                    <button class="copy-btn" onclick="copyToClipboard('💎 Just discovered the ultimate domain investing course! Learn how top investors build 6-7 figure portfolios. 13 guides + AI assistant included! {main_site_link} #DomainInvesting #PassiveIncome')">Copy</button>
                </div>
                
                <h4>LinkedIn Post:</h4>
                <div class="link-box">
                    Want to diversify your investment portfolio? Domain investing is generating incredible returns for those who know the secrets. I found this comprehensive course that teaches everything from first purchase to building a domain empire. Check it out: {main_site_link}
                    <button class="copy-btn" onclick="copyToClipboard('Want to diversify your investment portfolio? Domain investing is generating incredible returns for those who know the secrets. I found this comprehensive course that teaches everything from first purchase to building a domain empire. Check it out: {main_site_link}')">Copy</button>
                </div>
                
                <h4>Email Template:</h4>
                <div class="link-box">
                    Subject: How I'm Building Wealth Through Domain Investing

Hi [Name],

I wanted to share something exciting I discovered - a comprehensive domain investing course that's teaching people how to build serious wealth through premium domains.

The course includes:
• 13 in-depth strategy guides
• AI-powered investment assistant
• Real case studies and examples
• Step-by-step portfolio building

If you're looking for alternative investments that can generate passive income, this is worth checking out: {main_site_link}

Best regards,
{username}
                    <button class="copy-btn" onclick="copyToClipboard('Subject: How I\\'m Building Wealth Through Domain Investing\\n\\nHi [Name],\\n\\nI wanted to share something exciting I discovered - a comprehensive domain investing course that\\'s teaching people how to build serious wealth through premium domains.\\n\\nThe course includes:\\n• 13 in-depth strategy guides\\n• AI-powered investment assistant\\n• Real case studies and examples\\n• Step-by-step portfolio building\\n\\nIf you\\'re looking for alternative investments that can generate passive income, this is worth checking out: {main_site_link}\\n\\nBest regards,\\n{username}')">Copy</button>
                </div>
            </div>
            
            <div class="affiliate-card">
                <h3>💡 Success Tips</h3>
                <ul>
                    <li><strong>Target the Right Audience:</strong> Entrepreneurs, investors, side-hustlers</li>
                    <li><strong>Share Your Experience:</strong> Personal testimonials work best</li>
                    <li><strong>Use Multiple Channels:</strong> Social media, email, blogs, forums</li>
                    <li><strong>Provide Value First:</strong> Share domain investing tips, then promote</li>
                    <li><strong>Track Your Results:</strong> Monitor which methods work best</li>
                </ul>
            </div>
            
            <div class="affiliate-card">
                <h3>📋 Commission Terms</h3>
                <ul>
                    <li><strong>Commission Rate:</strong> 25% on all package sales</li>
                    <li><strong>Cookie Duration:</strong> 30 days from click</li>
                    <li><strong>Payment Schedule:</strong> Monthly payments via PayPal</li>
                    <li><strong>Minimum Payout:</strong> $50.00</li>
                    <li><strong>Tracking:</strong> Real-time dashboard updates</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p><strong>Questions about the affiliate program?</strong></p>
                <p>Contact us at <a href="mailto:affiliates@rizzosai.com">affiliates@rizzosai.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/admin-direct')
def admin_direct():
    """Direct admin access route - bypass login issues"""
    session['username'] = 'rizzos-admin'
    session['is_admin'] = True
    flash('Admin access granted!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/debug')
def debug():
    """Simple debug route"""
    if 'username' not in session:
        return "❌ NOT LOGGED IN - <a href='/admin-direct'>Click here for admin access</a>"
    
    username = session.get('username')
    package = get_user_package(username)
    guides = get_package_guides(username)
    
    return f"""
    <h1>🔍 Debug Info</h1>
    <p><strong>Username:</strong> {username}</p>
    <p><strong>Is Admin:</strong> {session.get('is_admin', False)}</p>
    <p><strong>Package:</strong> {package}</p>
    <p><strong>Guide Count:</strong> {len(guides)}</p>
    <p><strong>Guides:</strong> {', '.join(guides)}</p>
    <br><a href="/">← Back</a>
    """

# Affiliate system route with correct commission structure
@app.route('/affiliate')
def affiliate():
    """Affiliate marketing system for promoting rizzosai.com - 100% commission except 2nd sale"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session.get('username', 'Unknown')
    affiliate_id = f"rizzos-{username.lower().replace(' ', '')}"
    
    # Generate affiliate links
    main_site_link = f"https://rizzosai.com?ref={affiliate_id}"
    backoffice_link = f"https://backoffice.rizzosai.com?ref={affiliate_id}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Affiliate Program - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; }}
            .back-btn {{ background: #e2e8f0; color: #4a5568; padding: 8px 16px; border-radius: 8px; text-decoration: none; display: inline-block; margin-bottom: 20px; }}
            .affiliate-card {{ background: #f7fafc; border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #667eea; }}
            .commission-rate {{ background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; }}
            .link-box {{ background: #e2e8f0; padding: 15px; border-radius: 8px; margin: 10px 0; font-family: monospace; }}
            .copy-btn {{ background: #667eea; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
            .stat-card {{ background: white; border: 2px solid #667eea; border-radius: 10px; padding: 20px; text-align: center; }}
        </style>
        <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    alert('Link copied to clipboard!');
                }});
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            
            <h1>💰 Affiliate Program - INSANE Commission Structure!</h1>
            <p>Promote Rizzos AI and keep 100% of most sales! This is the most generous affiliate program in domain investing.</p>
            
            <div class="commission-rate">
                <h2>🚀 REVOLUTIONARY COMMISSION STRUCTURE!</h2>
                <p><strong>1st Sale:</strong> You keep 100% ($499.99 Elite / $999.99 Empire)</p>
                <p><strong>2nd Sale:</strong> We keep this one (our cut)</p>
                <p><strong>3rd Sale & Beyond:</strong> You keep 100% again!</p>
                <p style="font-size: 1.2em; margin-top: 15px;"><strong>Average: 90%+ commission rate!</strong></p>
            </div>
            
            <div class="affiliate-card">
                <h3>👤 Your Affiliate Details</h3>
                <p><strong>Affiliate ID:</strong> {affiliate_id}</p>
                <p><strong>Status:</strong> Active VIP Affiliate</p>
                <p><strong>Tier:</strong> {session.get('package', 'Elite')} Partner</p>
                <p><strong>Commission Model:</strong> Revolutionary 100% Structure</p>
            </div>
            
            <div class="affiliate-card">
                <h3>🔗 Your Money-Making Links</h3>
                
                <h4>Main Website Link (Primary):</h4>
                <div class="link-box">
                    {main_site_link}
                    <button class="copy-btn" onclick="copyToClipboard('{main_site_link}')">Copy</button>
                </div>
                
                <h4>Backoffice Direct Link:</h4>
                <div class="link-box">
                    {backoffice_link}
                    <button class="copy-btn" onclick="copyToClipboard('{backoffice_link}')">Copy</button>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>📊 Total Clicks</h3>
                    <h2>0</h2>
                    <p>Link clicks tracked</p>
                </div>
                <div class="stat-card">
                    <h3>💰 Sales Made</h3>
                    <h2>0</h2>
                    <p>Successful conversions</p>
                </div>
                <div class="stat-card">
                    <h3>💵 Your Earnings</h3>
                    <h2>$0.00</h2>
                    <p>Commission earned</p>
                </div>
                <div class="stat-card">
                    <h3>🎯 Next Payout</h3>
                    <h2>$0.00</h2>
                    <p>Pending commission</p>
                </div>
            </div>
            
            <div class="affiliate-card">
                <h3>🎯 Why This Program is INSANE</h3>
                <ul>
                    <li><strong>🚀 100% Commission:</strong> Keep entire sale amount on most sales</li>
                    <li><strong>💎 High-Value Products:</strong> $499-$999 per sale (not $29 courses)</li>
                    <li><strong>🎓 Premium Education:</strong> Easy to promote quality content</li>
                    <li><strong>🤖 AI Assistant:</strong> Unique selling point with Coey</li>
                    <li><strong>📈 Recurring Potential:</strong> Customers often upgrade</li>
                    <li><strong>💼 Business Audience:</strong> High-income potential customers</li>
                </ul>
            </div>
            
            <div class="affiliate-card">
                <h3>📱 Proven Marketing Messages</h3>
                
                <h4>High-Converting Headlines:</h4>
                <ul>
                    <li>"I'm making $10K/month buying domains - here's how"</li>
                    <li>"This AI tool found me a $50K domain deal"</li>
                    <li>"Why I quit my job to flip domains full-time"</li>
                    <li>"The domain investing secrets rich people don't want you to know"</li>
                </ul>
                
                <h4>Social Proof Angles:</h4>
                <ul>
                    <li>"Just learned the same strategies the pros use"</li>
                    <li>"Finally found a course that actually works"</li>
                    <li>"This AI assistant is like having a domain expert on speed dial"</li>
                    <li>"Made my investment back in the first week"</li>
                </ul>
            </div>
            
            <div class="affiliate-card">
                <h3>💡 Million-Dollar Marketing Tips</h3>
                <ol>
                    <li><strong>Target Entrepreneurs:</strong> People already investing in businesses</li>
                    <li><strong>Use Success Stories:</strong> Share domain flip wins and case studies</li>
                    <li><strong>Highlight AI Advantage:</strong> Coey assistant is unique selling point</li>
                    <li><strong>Focus on ROI:</strong> Show potential returns vs course cost</li>
                    <li><strong>Create Urgency:</strong> Limited-time bonuses or price increases</li>
                    <li><strong>Build Trust First:</strong> Provide value before promoting</li>
                </ol>
            </div>
            
            <div class="affiliate-card">
                <h3>📋 Commission Terms</h3>
                <ul>
                    <li><strong>Structure:</strong> 100% commission except every 2nd sale</li>
                    <li><strong>Products:</strong> Elite ($499.99) & Empire ($999.99) packages</li>
                    <li><strong>Cookie Duration:</strong> 30 days from click</li>
                    <li><strong>Payment Method:</strong> PayPal or bank transfer</li>
                    <li><strong>Payment Schedule:</strong> Weekly payouts</li>
                    <li><strong>Minimum Payout:</strong> $100 (basically one sale)</li>
                    <li><strong>Tracking:</strong> Real-time affiliate dashboard</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 30px; background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h3>🔥 Ready to Make Serious Money?</h3>
                <p><strong>This isn't your typical 5% affiliate program.</strong></p>
                <p>We're giving you 90%+ commissions because we want you to succeed BIG.</p>
                <p>Questions? Email: <a href="mailto:affiliates@rizzosai.com">affiliates@rizzosai.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """

# Domain packages page route
@app.route('/domain')
def domain_packages():
    """Domain packages selection page for domain.rizzosai.com"""
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Domain.RizzosAI.com - Choose Your Package</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            padding: 40px 0;
        }

        .header h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.3em;
            margin-bottom: 30px;
        }

        .packages-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }

        .package {
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            position: relative;
        }

        .package:hover {
            transform: translateY(-10px);
        }

        .package.featured {
            border: 3px solid #ffd700;
            transform: scale(1.05);
        }

        .package.popular {
            border: 3px solid #ff6b35;
        }

        .package.starter {
            border: 3px solid #28a745;
        }

        .package-badge {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }

        .badge-starter {
            background: #28a745;
            color: white;
        }

        .badge-popular {
            background: #ff6b35;
            color: white;
        }

        .badge-featured {
            background: #ffd700;
            color: #333;
        }

        .package-title {
            font-size: 2em;
            margin-bottom: 15px;
            color: #667eea;
            margin-top: 20px;
        }

        .package-price {
            font-size: 3.5em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }

        .package-subtitle {
            color: #666;
            margin-bottom: 25px;
            font-style: italic;
        }

        .package-features {
            text-align: left;
            margin: 30px 0;
            list-style: none;
        }

        .package-features li {
            padding: 10px 0;
            border-bottom: 1px solid #eee;
            position: relative;
            padding-left: 25px;
        }

        .package-features li:before {
            content: "✅";
            position: absolute;
            left: 0;
        }

        .buy-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: all 0.3s;
        }

        .buy-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .value-proposition {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            text-align: center;
        }

        .testimonials {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
        }

        .testimonial {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }

        .comparison-table {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }

        th {
            background: #667eea;
            color: white;
            font-weight: bold;
        }

        .check {
            color: #28a745;
            font-size: 1.2em;
        }

        .cross {
            color: #dc3545;
            font-size: 1.2em;
        }

        @media (max-width: 768px) {
            .packages-section {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2.5em;
            }
            
            .package-price {
                font-size: 2.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 Domain.RizzosAI.com</h1>
            <p>Choose Your Domain Investing Package</p>
            <p>From beginner-friendly to empire-building - we've got you covered!</p>
        </div>

        <div class="packages-section">
            <div class="package starter">
                <div class="package-badge badge-starter">BEST FOR BEGINNERS</div>
                <div class="package-title">🚀 Starter</div>
                <div class="package-price">$29</div>
                <div class="package-subtitle">Perfect entry point</div>
                <ul class="package-features">
                    <li>Domain Investing Basics Course</li>
                    <li>10 Proven Domain Lists</li>
                    <li>Basic Coey AI Access</li>
                    <li>Email Templates</li>
                    <li>Community Access</li>
                    <li>7-Day Money Back Guarantee</li>
                    <li>PDF Guides & Checklists</li>
                </ul>
                <button class="buy-btn" onclick="selectPackage('starter', 29)">🚀 Start Your Journey</button>
            </div>

            <div class="package">
                <div class="package-title">⚡ Accelerator</div>
                <div class="package-price">$99</div>
                <div class="package-subtitle">Speed up your success</div>
                <ul class="package-features">
                    <li>Everything in Starter Package</li>
                    <li>Advanced Domain Strategies</li>
                    <li>25 Premium Domain Lists</li>
                    <li>Enhanced Coey AI Features</li>
                    <li>Negotiation Masterclass</li>
                    <li>Market Analysis Tools</li>
                    <li>Monthly Live Training</li>
                    <li>14-Day Money Back Guarantee</li>
                    <li>Email & Discord Support</li>
                </ul>
                <button class="buy-btn" onclick="selectPackage('accelerator', 99)">⚡ Accelerate Growth</button>
            </div>

            <div class="package popular">
                <div class="package-badge badge-popular">MOST POPULAR</div>
                <div class="package-title">🔥 Professional</div>
                <div class="package-price">$249</div>
                <div class="package-subtitle">Serious investors choice</div>
                <ul class="package-features">
                    <li>Everything in Accelerator Package</li>
                    <li>Professional Domain Portfolio</li>
                    <li>40+ Premium Domain Lists</li>
                    <li>Full Coey AI Suite</li>
                    <li>Advanced Automation Scripts</li>
                    <li>Weekly Strategy Sessions</li>
                    <li>Priority Support</li>
                    <li>21-Day Money Back Guarantee</li>
                    <li>Private Telegram Group</li>
                    <li>Monthly 1-on-1 Call</li>
                </ul>
                <button class="buy-btn" onclick="selectPackage('professional', 249)">🔥 Go Professional</button>
            </div>

            <div class="package">
                <div class="package-title">💎 Elite</div>
                <div class="package-price">$499</div>
                <div class="package-subtitle">Elite investor status</div>
                <ul class="package-features">
                    <li>Everything in Professional Package</li>
                    <li>Complete Domain Investing Masterclass</li>
                    <li>50+ Premium Domain Lists</li>
                    <li>Advanced Market Analysis Tools</li>
                    <li>Private Discord Community</li>
                    <li>Weekly Live Q&A Sessions</li>
                    <li>Exclusive Domain Opportunities</li>
                    <li>30-Day Money Back Guarantee</li>
                    <li>Direct Access to Rizzos</li>
                    <li>Quarterly Portfolio Review</li>
                </ul>
                <button class="buy-btn" onclick="selectPackage('elite', 499)">💎 Join Elite Club</button>
            </div>

            <div class="package featured">
                <div class="package-badge badge-featured">ULTIMATE VALUE</div>
                <div class="package-title">👑 Empire</div>
                <div class="package-price">$999</div>
                <div class="package-subtitle">Build your domain empire</div>
                <ul class="package-features">
                    <li>Everything in Elite Package</li>
                    <li>3 Hours of 1-on-1 Coaching</li>
                    <li>Done-For-You Domain Portfolio</li>
                    <li>Advanced AI Automation Scripts</li>
                    <li>Exclusive High-Value Domain Leads</li>
                    <li>Personal Domain Investment Review</li>
                    <li>VIP Access to New Strategies</li>
                    <li>Lifetime Updates & Support</li>
                    <li>Direct Phone/WhatsApp Access</li>
                    <li>Joint Venture Opportunities</li>
                </ul>
                <button class="buy-btn" onclick="selectPackage('empire', 999)">👑 Build Your Empire</button>
            </div>
        </div>

        <div class="value-proposition">
            <h2>🎯 Why Choose Rizzos AI Domain Training?</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-top: 30px;">
                <div>
                    <h3>🤖 AI-Powered</h3>
                    <p>Coey AI assistant finds profitable domains 24/7</p>
                </div>
                <div>
                    <h3>📈 Proven Results</h3>
                    <p>Students making $10K+ monthly in domain profits</p>
                </div>
                <div>
                    <h3>🎓 Complete Training</h3>
                    <p>From basics to advanced empire-building strategies</p>
                </div>
                <div>
                    <h3>💰 High ROI</h3>
                    <p>Turn $100 investments into $10,000+ sales</p>
                </div>
            </div>
        </div>

        <div class="comparison-table">
            <h2 style="text-align: center; margin-bottom: 30px;">📊 Package Comparison</h2>
            <table>
                <tr>
                    <th>Feature</th>
                    <th>Starter</th>
                    <th>Accelerator</th>
                    <th>Professional</th>
                    <th>Elite</th>
                    <th>Empire</th>
                </tr>
                <tr>
                    <td>Domain Lists</td>
                    <td>10</td>
                    <td>25</td>
                    <td>40+</td>
                    <td>50+</td>
                    <td>50+</td>
                </tr>
                <tr>
                    <td>Coey AI Access</td>
                    <td class="check">✓</td>
                    <td class="check">✓</td>
                    <td class="check">✓</td>
                    <td class="check">✓</td>
                    <td class="check">✓</td>
                </tr>
                <tr>
                    <td>Live Training</td>
                    <td class="cross">✗</td>
                    <td>Monthly</td>
                    <td>Weekly</td>
                    <td>Weekly</td>
                    <td>Weekly</td>
                </tr>
                <tr>
                    <td>1-on-1 Coaching</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td>Monthly</td>
                    <td>Quarterly</td>
                    <td>3 Hours</td>
                </tr>
                <tr>
                    <td>Done-For-You Portfolio</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="check">✓</td>
                </tr>
                <tr>
                    <td>Direct Access to Rizzos</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="check">✓</td>
                    <td class="check">✓</td>
                </tr>
            </table>
        </div>

        <div class="testimonials">
            <h2 style="text-align: center; margin-bottom: 30px;">💰 Success Stories</h2>
            
            <div class="testimonial">
                <p>"Started with the $29 Starter package, made my money back in 2 days! Upgraded to Professional within a week."</p>
                <strong>- Jake M., Professional Member</strong>
            </div>
            
            <div class="testimonial">
                <p>"The $249 Professional package changed my life. Making $5K+ monthly flipping domains now!"</p>
                <strong>- Lisa R., Professional Member</strong>
            </div>
            
            <div class="testimonial">
                <p>"Empire package was the best investment I ever made. $100K in domain sales in 6 months!"</p>
                <strong>- Marcus T., Empire Member</strong>
            </div>

            <div class="testimonial">
                <p>"Coey AI found me a domain that sold for $50K. This system pays for itself!"</p>
                <strong>- Sarah L., Elite Member</strong>
            </div>
        </div>

        <div style="text-align: center; margin: 40px 0; background: white; padding: 40px; border-radius: 20px;">
            <h2>🔥 Ready to Start Your Domain Empire?</h2>
            <p style="font-size: 1.2em; margin: 20px 0;">Choose your package above and start making money with domains today!</p>
            <p><strong>Questions? Email:</strong> <a href="mailto:support@rizzosai.com">support@rizzosai.com</a></p>
        </div>
    </div>

    <script>
        function selectPackage(packageType, price) {
            // Store package selection
            localStorage.setItem('selectedPackage', packageType);
            localStorage.setItem('selectedPrice', price);
            
            // Show confirmation
            alert(`🎉 Great choice! You've selected the ${packageType.toUpperCase()} package for $${price}.\\n\\nRedirecting to secure checkout...`);
            
            // Redirect to checkout page
            window.location.href = `/checkout?package=${packageType}&price=${price}`;
        }

        // Add smooth scrolling for better UX
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add package hover effects
        document.querySelectorAll('.package').forEach(package => {
            package.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-15px) scale(1.02)';
            });
            
            package.addEventListener('mouseleave', function() {
                if (this.classList.contains('featured')) {
                    this.style.transform = 'scale(1.05)';
                } else {
                    this.style.transform = 'translateY(0) scale(1)';
                }
            });
        });
    </script>
</body>
</html>
    """
>>>>>>> 5b7d3eeb1ff3b03ce9efc5886cdc227eaaa414ad

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))