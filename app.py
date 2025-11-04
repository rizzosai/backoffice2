from flask import Flask, request, redirect, url_for, session, flash, render_template_string, jsonify
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
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
PACKAGES = {
    'starter': {
        'name': 'Starter Package',
        'price': '$29.99',
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup']
    },
    'pro': {
        'name': 'Pro Package', 
        'price': '$99.99',
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup', 'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 'Market Analysis', 'Negotiation Tactics']
    },
    'elite': {
        'name': 'Elite Package',
        'price': '$499.99', 
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup', 'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 'Market Analysis', 'Negotiation Tactics', 'Empire Building', 'Advanced Analytics', 'Premium Tools', 'Elite Strategies', 'Insider Secrets']
    },
    'empire': {
        'name': 'Empire Package',
        'price': '$999.99',
        'guides': ['Domain Basics', 'First Purchase Guide', 'Quick Setup', 'Advanced Strategies', 'Investment Guide', 'Portfolio Building', 'Market Analysis', 'Negotiation Tactics', 'Empire Building', 'Advanced Analytics', 'Premium Tools', 'Elite Strategies', 'Insider Secrets', 'Master Class', 'Personal Coaching', 'Exclusive Networks']
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
    return PACKAGES['starter']['guides']  # Default to starter

def is_banned_user(username):
    """Check if user is banned"""
    banned_users = load_banned_users()
    return username in banned_users

@app.route('/')
def dashboard():
    """Main dashboard - redirects to login if not authenticated"""
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
    
    # Check if this is empire-trial and if they've hit the limit
    trial_status = ""
    if package == 'empire-trial':
        customers = load_customers()
        guides_accessed = customers.get(username, {}).get('guides_accessed', 0)
        remaining = PACKAGES['empire-trial']['limit'] - guides_accessed
        if remaining <= 0:
            trial_status = f"""
            <div class="trial-expired">
                <h3>🚀 Trial Complete! Ready to Unlock Everything?</h3>
                <p>You've explored {PACKAGES['empire-trial']['limit']} guides. Upgrade to Empire Package for unlimited access to all {len(PACKAGES['empire']['guides'])} premium guides!</p>
                <a href="https://buy.stripe.com/00g8A20Ey6iT0es3cc" class="upgrade-btn">Upgrade to Empire Package - $999.99</a>
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
        <title>Rizzos AI - Domain Empire Backoffice V2</title>
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
                    <h1>🏆 Domain Empire Backoffice V2</h1>
                    <p>Your gateway to domain investing mastery - Fresh & Clean!</p>
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
                    <h2>📚 Your Guides</h2>
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
                        <a href="/market" class="coey-btn">📈 Market</a>
                        <a href="/tools" class="coey-btn">🛠️ Tools</a>
                    </div>
                </div>
                
                <div class="section coey-section">
                    <h2>🤖 Meet Coey - Your AI Domain Advisor</h2>
                    <p>Get personalized domain investing advice from our Claude-like AI assistant</p>
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
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check if user is banned
        if is_banned_user(username):
            flash('Your account has been suspended. Please contact support.', 'error')
            return redirect(url_for('login'))
        
        # Admin login - 3-part authentication
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
        
        flash('Invalid credentials. All fields required for admin access.', 'error')
    
    login_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rizzos AI - Login V2</title>
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
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
                <h1>🏆 Rizzos AI V2</h1>
                <p>Domain Empire Access - Fresh & Clean</p>
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
                <button type="submit" class="login-btn">Access Empire V2</button>
            </form>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(login_html)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/owner-access')
def owner_access():
    """Special route for owner to get Elite package access"""
    # Auto-create owner account with Elite package
    customers = load_customers()
    
    owner_username = "rizzosowner"
    owner_password = "empire2024!"
    
    customers[owner_username] = {
        'password': owner_password,
        'email': 'owner@rizzosai.com',
        'package': 'elite',
        'created_at': datetime.now().isoformat(),
        'session_id': 'owner_direct_v2',
        'guides_accessed': 0,
        'owner': True
    }
    
    save_customers(customers)
    
    # Auto-login
    session['username'] = owner_username
    session['is_admin'] = False
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Owner Access Created V2 - Rizzos AI</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
            .success-box {{ background: white; padding: 40px; border-radius: 15px; text-align: center; max-width: 500px; }}
            .access-btn {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px 30px; border: none; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="success-box">
            <h1>🏆 Owner Access Created V2!</h1>
            <p><strong>Username:</strong> {owner_username}</p>
            <p><strong>Password:</strong> {owner_password}</p>
            <p><strong>Package:</strong> Elite Package ($499.99)</p>
            <p>You now have access to all {len(PACKAGES['elite']['guides'])} Elite guides!</p>
            <p><strong>Fresh Project V2 - No Cache Issues!</strong></p>
            <a href="/" class="access-btn">Access Your Elite Dashboard V2</a>
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
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            <h1>🤖 Coey AI V2 - Coming Soon!</h1>
            <p>Your AI domain advisor will be available soon with the new API integration!</p>
        </div>
    </body>
    </html>
    """

@app.route('/coey/chat', methods=['POST'])
def coey_chat_api():
    """Handle chat messages to Coey AI"""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get response from OpenAI
    messages = [
        {"role": "system", "content": "You are Coey, an expert AI domain investing advisor. Help users build successful domain portfolios."},
        {"role": "user", "content": user_message}
    ]
    
    coey_response = get_clean_openai_response(messages)
    
    if not coey_response:
        coey_response = "I'm having technical difficulties right now, but I can tell you that successful domain investing requires research, patience, and strategic thinking. What specific area would you like to explore?"
    
    return jsonify({'response': coey_response})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))