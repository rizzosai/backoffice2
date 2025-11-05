from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# File paths
CUSTOMERS_FILE = 'customers.json'
PACKAGES_FILE = 'packages.json'
COMMISSIONS_FILE = 'commissions.json'
COMMISSION_QUEUE_FILE = 'commission_queue.json'
TRIAL_CUSTOMERS_FILE = 'trial_customers.json'
LEADS_FILE = 'leads.json'

# Helper functions
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_commission_queue():
    if os.path.exists(COMMISSION_QUEUE_FILE):
        with open(COMMISSION_QUEUE_FILE, 'r') as f:
            return json.load(f)

# --- SALES AFFILIATE ROUTE (moved after app definition) ---
@app.route('/sales/aff=<affiliate_code>', methods=['GET'])
def sales_affiliate_page(affiliate_code):
    # Optionally, look up affiliate info for display
    customers = load_json(CUSTOMERS_FILE)
    affiliate_email = None
    for email, data in customers.items():
        if email.split('@')[0] == affiliate_code:
            affiliate_email = email
            break
    return render_template('sales/index.html', affiliate_code=affiliate_code, affiliate_email=affiliate_email)
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# File paths
CUSTOMERS_FILE = 'customers.json'
PACKAGES_FILE = 'packages.json'
COMMISSIONS_FILE = 'commissions.json'
COMMISSION_QUEUE_FILE = 'commission_queue.json'
TRIAL_CUSTOMERS_FILE = 'trial_customers.json'
LEADS_FILE = 'leads.json'

# Helper functions
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_commission_queue():
    if os.path.exists(COMMISSION_QUEUE_FILE):
        with open(COMMISSION_QUEUE_FILE, 'r') as f:
            return json.load(f)
    return {"queue": [], "completed": [], "total_signups_processed": 0}

def save_commission_queue(queue_data):
    with open(COMMISSION_QUEUE_FILE, 'w') as f:
        json.dump(queue_data, f, indent=2)

def add_to_commission_queue(customer_email, package_level):
    queue_data = load_commission_queue()
    
    # Add to queue if not already there
    if customer_email not in [item['email'] for item in queue_data['queue']]:
        queue_data['queue'].append({
            'email': customer_email,
            'package_level': package_level,
            'joined_queue': datetime.now().isoformat(),
            'queue_position': len(queue_data['queue']) + 1
        })
        save_commission_queue(queue_data)

def process_next_5_commission(purchase_amount, package_level):
    queue_data = load_commission_queue()
    
    # Get next 5 people from queue
    next_5 = queue_data['queue'][:5]
    
    if len(next_5) > 0:
        # Calculate commission per person
        commission_per_person = purchase_amount / len(next_5)
        
        # Process commissions
        commissions = load_json(COMMISSIONS_FILE)
        
        for person in next_5:
            email = person['email']
            if email not in commissions:
                commissions[email] = {'total_earned': 0, 'payments': []}
            
            # Add commission
            commissions[email]['total_earned'] += commission_per_person
            commissions[email]['payments'].append({
                'amount': commission_per_person,
                'date': datetime.now().isoformat(),
                'from_package_level': package_level,
                'purchase_amount': purchase_amount
            })
        
        # Move processed people to completed
        queue_data['completed'].extend(next_5)
        queue_data['queue'] = queue_data['queue'][5:]  # Remove first 5
        queue_data['total_signups_processed'] += 1
        
        # Update queue positions
        for i, person in enumerate(queue_data['queue']):
            person['queue_position'] = i + 1
        
        # Save data
        save_json(COMMISSIONS_FILE, commissions)
        save_commission_queue(queue_data)
        
        return next_5
    
    return []

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/aff=<affiliate_code>')
def main_affiliate_page(affiliate_code):
    # Find affiliate by email prefix
    customers = load_json(CUSTOMERS_FILE)
    affiliate_email = None
    
    for email, data in customers.items():
        if email.split('@')[0] == affiliate_code:
            affiliate_email = email
            break
    
    if not affiliate_email:
        # If affiliate not found, redirect to main page
        return redirect(url_for('homepage'))
    
    affiliate = customers[affiliate_email]
    return render_template('affiliate_page.html', 
                         affiliate=affiliate, 
                         affiliate_code=affiliate_code)

@app.route('/capture-lead', methods=['POST'])
def capture_lead():
    try:
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        affiliate_ref = request.form.get('affiliate_ref', '')
        
        leads = load_json(LEADS_FILE)
        
        # Save lead
        leads[email] = {
            'first_name': first_name,
            'email': email,
            'signup_date': datetime.now().isoformat(),
            'affiliate_ref': affiliate_ref,
            'status': 'lead',
            'follow_ups_sent': 0
        }
        
        save_json(LEADS_FILE, leads)
        
        # Redirect to appropriate page based on affiliate or main
        if affiliate_ref:
            return redirect(f'/aff={affiliate_ref}/thank-you')
        else:
            return redirect('/thank-you')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/thank-you')
@app.route('/aff=<affiliate_code>/thank-you')
def thank_you(affiliate_code=None):
    return render_template('thank_you.html', affiliate_code=affiliate_code)

@app.route('/login')
def login_page():
    if 'customer_email' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/')
def home():
    if 'customer_email' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    customers = load_json(CUSTOMERS_FILE)
    
    if email in customers and customers[email]['password'] == password:
        session['customer_email'] = email
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'customer_email' not in session:
        return redirect(url_for('home'))
    
    email = session['customer_email']
    customers = load_json(CUSTOMERS_FILE)
    packages = load_json(PACKAGES_FILE)
    commissions = load_json(COMMISSIONS_FILE)
    
    customer = customers.get(email, {})
    package_level = customer.get('package_level', 0)
    
    # Get commission info
    customer_commissions = commissions.get(email, {'total_earned': 0, 'payments': []})
    
    # Get queue status
    queue_data = load_commission_queue()
    queue_position = None
    for i, person in enumerate(queue_data['queue']):
        if person['email'] == email:
            queue_position = i + 1
            break
    
    return render_template('dashboard.html', 
                         customer=customer,
                         packages=packages,
                         package_level=package_level,
                         commissions=customer_commissions,
                         queue_position=queue_position)

@app.route('/training')
def training():
    if 'customer_email' not in session:
        return redirect(url_for('login_page'))
    
    email = session['customer_email']
    customers = load_json(CUSTOMERS_FILE)
    customer = customers.get(email, {})
    
    return render_template('training.html', customer=customer)

@app.route('/queue-dashboard')
def queue_dashboard():
    if 'customer_email' not in session:
        return redirect(url_for('home'))
    
    queue_data = load_commission_queue()
    
    return render_template('queue_dashboard.html', 
                         queue_data=queue_data)

@app.route('/webhook/direct-purchase', methods=['POST'])
def handle_direct_purchase():
    try:
        data = request.json
        customer_email = data.get('customer_email')
        package_level = int(data.get('package_level', 1))
        purchase_amount = float(data.get('purchase_amount', 0))
        affiliate_ref = data.get('affiliate_ref')
        
        # Add customer to system
        customers = load_json(CUSTOMERS_FILE)
        if customer_email not in customers:
            customers[customer_email] = {
                'email': customer_email,
                'package_level': package_level,
                'signup_date': datetime.now().isoformat(),
                'password': 'temp123',  # They should change this
                'referred_by': affiliate_ref
            }
            save_json(CUSTOMERS_FILE, customers)
        
        # Add to commission queue
        add_to_commission_queue(customer_email, package_level)
        
        # Process Next 5 commissions
        paid_users = process_next_5_commission(purchase_amount, package_level)
        
        return jsonify({
            'status': 'success',
            'message': f'Customer {customer_email} added and commissions processed',
            'paid_users': len(paid_users)
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/webhook/trial-converted', methods=['POST'])
def handle_trial_converted():
    try:
        data = request.json
        customer_email = data.get('customer_email')
        package_level = int(data.get('package_level', 1))
        purchase_amount = float(data.get('purchase_amount', 0))
        
        # Move from trial to full customer
        trial_customers = load_json(TRIAL_CUSTOMERS_FILE)
        customers = load_json(CUSTOMERS_FILE)
        
        if customer_email in trial_customers:
            # Move to full customers
            trial_data = trial_customers[customer_email]
            customers[customer_email] = {
                'email': customer_email,
                'package_level': package_level,
                'signup_date': datetime.now().isoformat(),
                'password': trial_data.get('password', 'temp123'),
                'referred_by': trial_data.get('referred_by'),
                'converted_from_trial': True
            }
            
            # Remove from trials
            del trial_customers[customer_email]
            
            save_json(CUSTOMERS_FILE, customers)
            save_json(TRIAL_CUSTOMERS_FILE, trial_customers)
        
        # Add to commission queue and process payments
        add_to_commission_queue(customer_email, package_level)
        paid_users = process_next_5_commission(purchase_amount, package_level)
        
        return jsonify({
            'status': 'success',
            'message': f'Trial customer {customer_email} converted and commissions processed',
            'paid_users': len(paid_users)
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/webhook/domain-purchase', methods=['POST'])
def webhook_domain_purchase():
    """Webhook to handle domain purchases from sales.rizzosai.com"""
    try:
        data = request.get_json()
        customer_email = data.get('email')
        domain_name = data.get('domain')
        purchase_amount = data.get('amount', 0)
        
        if not customer_email or not domain_name:
            return jsonify({'status': 'error', 'message': 'Missing email or domain'}), 400
        
        customers = load_json(CUSTOMERS_FILE)
        
        # Create customer if doesn't exist
        if customer_email not in customers:
            customers[customer_email] = {
                'email': customer_email,
                'signup_date': datetime.now().isoformat(),
                'package_level': 1,  # Default to Basic Starter
                'purchased_domains': []
            }
        
        # Add domain to customer's purchased domains
        if 'purchased_domains' not in customers[customer_email]:
            customers[customer_email]['purchased_domains'] = []
        
        domain_info = {
            'domain': domain_name,
            'purchased_date': datetime.now().isoformat(),
            'amount_paid': purchase_amount,
            'status': 'active'
        }
        
        customers[customer_email]['purchased_domains'].append(domain_info)
        save_json(CUSTOMERS_FILE, customers)
        
        # Add to commission queue
        package_level = customers[customer_email].get('package_level', 1)
        add_to_commission_queue(customer_email, package_level)
        
        # Process commissions
        process_next_5_commission(purchase_amount, package_level)
        
        return jsonify({
            'status': 'success',
            'message': f'Domain {domain_name} registered for {customer_email}',
            'redirect_url': f'/domain-purchase-redirect?email={customer_email}&domain={domain_name}'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/logout')
def logout():
    session.pop('customer_email', None)
    return redirect(url_for('home'))

@app.route('/domain-purchase-redirect')
def domain_purchase_redirect():
    """Redirect users to their back office after domain purchase from sales.rizzosai.com"""
    customer_email = request.args.get('email')
    domain_name = request.args.get('domain')
    
    if not customer_email:
        return redirect(url_for('home'))
    
    # Set session and redirect to dashboard
    session['customer_email'] = customer_email
    
    # Log the domain purchase
    customers = load_json(CUSTOMERS_FILE)
    if customer_email in customers:
        if 'purchased_domains' not in customers[customer_email]:
            customers[customer_email]['purchased_domains'] = []
        
        if domain_name and domain_name not in customers[customer_email]['purchased_domains']:
            customers[customer_email]['purchased_domains'].append({
                'domain': domain_name,
                'purchased_date': datetime.now().isoformat(),
                'status': 'active'
            })
            save_json(CUSTOMERS_FILE, customers)
    
    return redirect(url_for('dashboard'))

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


# --- SALES PAGE INTEGRATION ---
from flask import flash

@app.route('/sales', methods=['GET'])
def sales_page():
    return render_template('sales/index.html', affiliate_code=None, affiliate_email=None)

@app.route('/sales/domain-purchase', methods=['POST'])
def sales_domain_purchase():
    name = request.form.get('name')
    email = request.form.get('email')
    domain = request.form.get('domain')
    affiliate_code = request.form.get('affiliate_code')
    if not name or not email or not domain:
        flash('All fields are required.')
        return redirect(url_for('sales_page'))

    # Forward to internal webhook logic (simulate as internal call)
    customers = load_json(CUSTOMERS_FILE)
    if email not in customers:
        customers[email] = {
            'email': email,
            'signup_date': datetime.now().isoformat(),
            'package_level': 1,
            'purchased_domains': [],
            'referred_by': affiliate_code if affiliate_code else None
        }
    if 'purchased_domains' not in customers[email]:
        customers[email]['purchased_domains'] = []
    domain_info = {
        'domain': domain,
        'purchased_date': datetime.now().isoformat(),
        'amount_paid': 0,
        'status': 'pending',
        'affiliate_code': affiliate_code if affiliate_code else None
    }
    customers[email]['purchased_domains'].append(domain_info)
    save_json(CUSTOMERS_FILE, customers)
    package_level = customers[email].get('package_level', 1)
    add_to_commission_queue(email, package_level)
    process_next_5_commission(0, package_level)
    return redirect(url_for('sales_success'))

@app.route('/sales/success', methods=['GET'])
def sales_success():
    return render_template('sales/success.html')