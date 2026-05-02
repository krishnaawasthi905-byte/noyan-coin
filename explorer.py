from flask import Flask, jsonify, render_template_string, request, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
import hashlib
import json
import time
import os
import ecdsa
import random
import string
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "nyn-secret-2026")
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
bcrypt = Bcrypt(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "20 per minute"])

database_url = os.environ.get("DATABASE_URL", "sqlite:///nyn.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(database_url)
Base = declarative_base()

EMAIL_USER = os.environ.get("EMAIL_USER", "")
EMAIL_PASS = os.environ.get("EMAIL_PASS", "")
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")
NYN_SECRET = os.environ.get("NYN_SECRET", "fallback")

class BlockModel(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    timestamp = Column(Float)
    transactions = Column(Text)
    previous_hash = Column(String(64))
    hash = Column(String(64))

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(200), nullable=False)
    wallet_address = Column(String(100), unique=True)
    public_key = Column(Text)
    created_at = Column(Float)
    is_verified = Column(Boolean, default=False)
    balance = Column(Float, default=50.0)
    referral_code = Column(String(10), unique=True)
    referral_count = Column(Integer, default=0)
    referred_by = Column(String(10), nullable=True)
    otp = Column(String(6), nullable=True)
    otp_expiry = Column(Float, nullable=True)

class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    sender = Column(String(100))
    receiver = Column(String(100))
    amount = Column(Float)
    timestamp = Column(Float)
    tx_hash = Column(String(64))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def calculate_hash(index, timestamp, transactions, previous_hash):
    block_string = json.dumps({
        "index": index,
        "timestamp": timestamp,
        "transactions": transactions,
        "previous_hash": previous_hash
    }, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

def get_chain():
    s = Session()
    blocks = s.query(BlockModel).order_by(BlockModel.index).all()
    s.close()
    return blocks

def add_block(transactions):
    s = Session()
    chain = s.query(BlockModel).order_by(BlockModel.index).all()
    previous_hash = "0" if len(chain) == 0 else chain[-1].hash
    index = len(chain)
    timestamp = time.time()
    h = calculate_hash(index, timestamp, json.dumps(transactions), previous_hash)
    block = BlockModel(index=index, timestamp=timestamp, transactions=json.dumps(transactions), previous_hash=previous_hash, hash=h)
    s.add(block)
    s.commit()
    s.close()

def generate_wallet():
    private_key = os.urandom(32)
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    public_key = signing_key.get_verifying_key()
    pub_hash = hashlib.sha256(public_key.to_string()).hexdigest()
    address = "NYN" + pub_hash[:32].upper()
    return address, public_key.to_string().hex()

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def send_otp_email(email, otp):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = "NYN Wallet - Your Verification Code"
        body = f"""
⚡ NYN NoyanCoin Verification

Your OTP code is: {otp}

This code expires in 10 minutes.

Republic of Nowhere - Currency of Everywhere
        """
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        return True
    except:
        return False

def verify_recaptcha(token):
    if not RECAPTCHA_SECRET_KEY:
        return True
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    })
    return response.json().get('success', False)

s = Session()
if s.query(BlockModel).count() == 0:
    add_block("NYN Genesis Block - Republic of Nowhere")
    add_block({"from": "Founder", "to": "Republic of Nowhere", "amount": 24000000})
s.close()

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>NYN Explorer - NoyanCoin</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0a0a; color: #00ff88; font-family: monospace; padding: 20px; }
h1 { text-align: center; font-size: 2em; margin-bottom: 5px; }
h3 { color: #888; text-align: center; margin-bottom: 20px; }
.nav { display: flex; justify-content: center; gap: 15px; margin-bottom: 25px; flex-wrap: wrap; }
.nav a { color: #00ff88; text-decoration: none; border: 1px solid #00ff88; padding: 8px 20px; border-radius: 5px; }
.nav a:hover { background: #00ff88; color: #000; }
.logout { color: #ff4444 !important; border-color: #ff4444 !important; }
.logout:hover { background: #ff4444 !important; color: #fff !important; }
.stats { display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
.stat { text-align: center; background: #111; padding: 15px 25px; border-radius: 8px; border: 1px solid #333; }
.stat h2 { color: #00ff88; margin: 0; }
.stat p { color: #888; margin: 5px 0 0 0; }
.block { background: #111; border: 1px solid #00ff88; margin: 10px 0; padding: 15px; border-radius: 8px; }
.block h2 { color: #00ff88; margin: 0 0 10px 0; }
.hash { color: #ff8800; word-break: break-all; }
.data { color: #fff; }
.search-box { max-width: 600px; margin: 20px auto; display: flex; gap: 10px; }
.search-box input { flex: 1; padding: 10px; background: #000; border: 1px solid #333; color: #00ff88; border-radius: 5px; font-family: monospace; }
.search-box button { padding: 10px 20px; background: #00ff88; color: #000; border: none; border-radius: 5px; cursor: pointer; font-family: monospace; font-weight: bold; }
.leaderboard { max-width: 700px; margin: 20px auto; }
.leaderboard h2 { color: #00ff88; margin-bottom: 15px; text-align: center; }
.lb-row { display: flex; justify-content: space-between; background: #111; border: 1px solid #333; margin: 5px 0; padding: 12px 15px; border-radius: 5px; }
.lb-rank { color: #ff8800; font-weight: bold; }
.lb-addr { color: #888; font-size: 0.85em; }
.lb-bal { color: #00ff88; font-weight: bold; }
</style>
</head>
<body>
<h1>⚡ NYN Explorer</h1>
<h3>Republic of Nowhere — NoyanCoin Blockchain</h3>
<div class="nav">
  <a href="/">Explorer</a>
  <a href="/leaderboard">Leaderboard</a>
  {% if logged_in %}
  <a href="/wallet">My Wallet</a>
  <a href="/logout" class="logout">Logout</a>
  {% else %}
  <a href="/login">Login</a>
  <a href="/register">Register</a>
  {% endif %}
</div>
<div class="stats">
  <div class="stat"><h2>{{ blocks }}</h2><p>Blocks</p></div>
  <div class="stat"><h2>24,000,000</h2><p>Total Supply</p></div>
  <div class="stat"><h2>NYN</h2><p>Ticker</p></div>
  <div class="stat"><h2>{{ users }}</h2><p>Wallets</p></div>
  <div class="stat"><h2>{{ txns }}</h2><p>Transactions</p></div>
</div>
<div class="search-box">
  <input type="text" id="searchInput" placeholder="Search by block hash or wallet address...">
  <button onclick="window.location.href='/search?q='+document.getElementById('searchInput').value">Search</button>
</div>
{% for block in chain %}
<div class="block">
  <h2>Block #{{ block.index }}</h2>
  <p class="hash">Hash: {{ block.hash }}</p>
  <p class="hash">Prev: {{ block.previous_hash }}</p>
  <p class="data">Data: {{ block.transactions }}</p>
</div>
{% endfor %}
</body>
</html>
"""

REGISTER_HTML = """
<!DOCTYPE html><html><head><title>Register - NYN</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}.form-box{max-width:420px;margin:30px auto;background:#111;padding:30px;border-radius:10px;border:1px solid #00ff88;}.form-box h2{color:#00ff88;margin-bottom:20px;text-align:center;}.form-box input{width:100%;padding:12px;margin:8px 0;background:#000;border:1px solid #333;color:#00ff88;border-radius:5px;font-family:monospace;font-size:14px;}.form-box button{width:100%;padding:12px;margin-top:15px;background:#00ff88;color:#000;border:none;border-radius:5px;font-family:monospace;font-size:1em;cursor:pointer;font-weight:bold;}.msg{text-align:center;padding:10px;margin:10px 0;border-radius:5px;}.msg.error{background:#ff000022;border:1px solid #ff0000;color:#ff4444;}.msg.success{background:#00ff8822;border:1px solid #00ff88;color:#00ff88;}a{color:#00ff88;}.recaptcha-box{margin:15px 0;display:flex;justify-content:center;}.bonus{background:#00ff8811;border:1px solid #00ff8844;padding:10px;border-radius:5px;margin:10px 0;text-align:center;font-size:0.85em;color:#00ff88;}</style></head>
<body><div class="form-box">
<h2>⚡ Create NYN Wallet</h2>
<div class="bonus">🎁 Get 50 NYN free on registration!</div>
{% if msg %}<div class="msg {{ msg_type }}">{{ msg }}</div>{% endif %}
<form method="POST">
<input type="text" name="username" placeholder="Username (min 3 chars)" required maxlength="30">
<input type="email" name="email" placeholder="Email address" required>
<input type="password" name="password" placeholder="Password (min 8 chars)" required minlength="8">
<input type="password" name="confirm" placeholder="Confirm Password" required>
<input type="text" name="referral" placeholder="Referral code (optional)">
<div class="recaptcha-box">
<div class="g-recaptcha" data-sitekey="{{ site_key }}"></div>
</div>
<button type="submit">Create Wallet & Get 50 NYN</button>
</form>
<p style="text-align:center;margin-top:15px;">Already have a wallet? <a href="/login">Login</a></p>
</div></body></html>
"""

VERIFY_HTML = """
<!DOCTYPE html><html><head><title>Verify Email - NYN</title>
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}.form-box{max-width:400px;margin:50px auto;background:#111;padding:30px;border-radius:10px;border:1px solid #00ff88;}.form-box h2{color:#00ff88;margin-bottom:20px;text-align:center;}.form-box input{width:100%;padding:12px;margin:8px 0;background:#000;border:1px solid #333;color:#00ff88;border-radius:5px;font-family:monospace;font-size:20px;text-align:center;letter-spacing:10px;}.form-box button{width:100%;padding:12px;margin-top:15px;background:#00ff88;color:#000;border:none;border-radius:5px;font-family:monospace;font-size:1em;cursor:pointer;font-weight:bold;}.msg{text-align:center;padding:10px;margin:10px 0;border-radius:5px;}.msg.error{background:#ff000022;border:1px solid #ff0000;color:#ff4444;}a{color:#00ff88;}</style></head>
<body><div class="form-box">
<h2>⚡ Verify Your Email</h2>
<p style="color:#888;text-align:center;margin-bottom:20px;">Enter the 6-digit code sent to your email</p>
{% if msg %}<div class="msg error">{{ msg }}</div>{% endif %}
<form method="POST">
<input type="text" name="otp" placeholder="000000" maxlength="6" required>
<button type="submit">Verify & Activate Wallet</button>
</form>
<p style="text-align:center;margin-top:15px;"><a href="/resend-otp">Resend code</a></p>
</div></body></html>
"""

LOGIN_HTML = """
<!DOCTYPE html><html><head><title>Login - NYN</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}.form-box{max-width:400px;margin:50px auto;background:#111;padding:30px;border-radius:10px;border:1px solid #00ff88;}.form-box h2{color:#00ff88;margin-bottom:20px;text-align:center;}.form-box input{width:100%;padding:12px;margin:8px 0;background:#000;border:1px solid #333;color:#00ff88;border-radius:5px;font-family:monospace;font-size:14px;}.form-box button{width:100%;padding:12px;margin-top:15px;background:#00ff88;color:#000;border:none;border-radius:5px;font-family:monospace;font-size:1em;cursor:pointer;font-weight:bold;}.msg{text-align:center;padding:10px;margin:10px 0;border-radius:5px;}.msg.error{background:#ff000022;border:1px solid #ff0000;color:#ff4444;}a{color:#00ff88;}</style></head>
<body><div class="form-box">
<h2>⚡ Login to NYN</h2>
{% if msg %}<div class="msg error">{{ msg }}</div>{% endif %}
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<p style="text-align:center;margin-top:15px;">No wallet yet? <a href="/register">Register</a></p>
</div></body></html>
"""

WALLET_HTML = """
<!DOCTYPE html><html><head><title>My Wallet - NYN</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}h1{text-align:center;font-size:2em;margin-bottom:5px;}h3{color:#888;text-align:center;margin-bottom:20px;}.nav{display:flex;justify-content:center;gap:15px;margin-bottom:25px;flex-wrap:wrap;}.nav a{color:#00ff88;text-decoration:none;border:1px solid #00ff88;padding:8px 20px;border-radius:5px;}.logout{color:#ff4444!important;border-color:#ff4444!important;}.wallet-box{max-width:600px;margin:20px auto;background:#111;padding:25px;border-radius:10px;border:1px solid #00ff88;margin-bottom:15px;}.wallet-box h2{color:#00ff88;margin-bottom:15px;}.address{background:#000;padding:15px;border-radius:5px;word-break:break-all;color:#ff8800;margin:10px 0;font-size:0.85em;}.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:0.75em;margin-left:8px;}.verified{background:#00ff8822;border:1px solid #00ff88;color:#00ff88;}.unverified{background:#ff000022;border:1px solid #ff4444;color:#ff4444;}.balance{font-size:2em;color:#00ff88;text-align:center;padding:20px;}.balance span{font-size:0.5em;color:#888;}.send-form input{width:100%;padding:10px;margin:5px 0;background:#000;border:1px solid #333;color:#00ff88;border-radius:5px;font-family:monospace;}.send-form button{width:100%;padding:12px;margin-top:10px;background:#00ff88;color:#000;border:none;border-radius:5px;cursor:pointer;font-family:monospace;font-weight:bold;}.tx-row{display:flex;justify-content:space-between;padding:10px;border-bottom:1px solid #222;font-size:0.85em;}.tx-in{color:#00ff88;}.tx-out{color:#ff4444;}.referral-box{background:#00ff8811;border:1px solid #00ff8844;padding:15px;border-radius:5px;margin:10px 0;}.copy-btn{background:none;border:1px solid #00ff88;color:#00ff88;padding:5px 10px;border-radius:3px;cursor:pointer;font-family:monospace;font-size:0.8em;margin-left:10px;}.msg{padding:10px;border-radius:5px;margin:10px 0;text-align:center;}.msg.error{background:#ff000022;border:1px solid #ff0000;color:#ff4444;}.msg.success{background:#00ff8822;border:1px solid #00ff88;color:#00ff88;}#qrcode{display:flex;justify-content:center;margin:15px 0;padding:10px;background:white;border-radius:5px;width:fit-content;margin:15px auto;}</style></head>
<body>
<h1>⚡ NYN Explorer</h1>
<h3>Republic of Nowhere — NoyanCoin Blockchain</h3>
<div class="nav">
<a href="/">Explorer</a>
<a href="/leaderboard">Leaderboard</a>
<a href="/wallet">My Wallet</a>
<a href="/logout" class="logout">Logout</a>
</div>
{% if msg %}<div class="msg {{ msg_type }}" style="max-width:600px;margin:10px auto;">{{ msg }}</div>{% endif %}
<div class="wallet-box">
<h2>👤 {{ username }} <span class="badge {{ 'verified' if is_verified else 'unverified' }}">{{ 'Verified ✓' if is_verified else 'Unverified' }}</span></h2>
<div class="balance">{{ balance }} <span>NYN</span></div>
<p style="color:#888;margin-bottom:8px;">Wallet Address:</p>
<div class="address" id="walletAddr">{{ wallet_address }}</div>
<button class="copy-btn" onclick="navigator.clipboard.writeText('{{ wallet_address }}');alert('Copied!')">Copy Address</button>
<div id="qrcode"></div>
<p style="color:#888;font-size:0.8em;margin-top:10px;">Member since: {{ created_at }}</p>
</div>
{% if not is_verified %}
<div class="wallet-box" style="border-color:#ff4444;">
<h2 style="color:#ff4444;">⚠️ Verify Your Email</h2>
<p style="color:#888;margin-bottom:10px;">Verify your email to unlock all NYN features.</p>
<a href="/verify" style="color:#00ff88;">Click here to verify →</a>
</div>
{% endif %}
<div class="wallet-box">
<h2>Send NYN</h2>
<div class="send-form">
<form method="POST" action="/send">
<input type="text" name="receiver" placeholder="Receiver wallet address (NYN...)">
<input type="number" name="amount" placeholder="Amount (NYN)" step="0.01" min="0.01">
<button type="submit">Send NYN ⚡</button>
</form>
</div>
</div>
<div class="wallet-box">
<h2>Referral Program 🎁</h2>
<div class="referral-box">
<p style="color:#888;font-size:0.85em;">Your referral code:</p>
<p style="font-size:1.2em;color:#00ff88;">{{ referral_code }} <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ referral_code }}');alert('Copied!')">Copy</button></p>
<p style="color:#888;font-size:0.8em;margin-top:8px;">Referrals used: {{ referral_count }}/3 • Earn 20 NYN per referral</p>
</div>
</div>
<div class="wallet-box">
<h2>Transaction History</h2>
{% if transactions %}
{% for tx in transactions %}
<div class="tx-row">
<span class="{{ 'tx-in' if tx.receiver == wallet_address else 'tx-out' }}">{{ '+' if tx.receiver == wallet_address else '-' }}{{ tx.amount }} NYN</span>
<span style="color:#888;font-size:0.8em;">{{ tx.sender[:20] }}...</span>
<span style="color:#555;font-size:0.75em;">{{ tx.time }}</span>
</div>
{% endfor %}
{% else %}
<p style="color:#555;">No transactions yet.</p>
{% endif %}
</div>
<script>
new QRCode(document.getElementById("qrcode"), {
  text: "{{ wallet_address }}",
  width: 128,
  height: 128
});
</script>
</body></html>
"""

LEADERBOARD_HTML = """
<!DOCTYPE html><html><head><title>Leaderboard - NYN</title>
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}h1{text-align:center;font-size:2em;margin-bottom:5px;}h3{color:#888;text-align:center;margin-bottom:20px;}.nav{display:flex;justify-content:center;gap:15px;margin-bottom:25px;flex-wrap:wrap;}.nav a{color:#00ff88;text-decoration:none;border:1px solid #00ff88;padding:8px 20px;border-radius:5px;}.logout{color:#ff4444!important;border-color:#ff4444!important;}.lb-table{max-width:700px;margin:0 auto;}.lb-header{display:flex;justify-content:space-between;padding:10px 15px;color:#888;font-size:0.85em;border-bottom:1px solid #333;}.lb-row{display:flex;justify-content:space-between;align-items:center;background:#111;border:1px solid #222;margin:5px 0;padding:12px 15px;border-radius:5px;}.lb-rank{color:#ff8800;font-weight:bold;width:40px;}.lb-user{color:#00ff88;flex:1;}.lb-addr{color:#555;font-size:0.75em;flex:2;}.lb-bal{color:#00ff88;font-weight:bold;text-align:right;}.gold{border-color:#ffd700!important;}.silver{border-color:#c0c0c0!important;}.bronze{border-color:#cd7f32!important;}</style></head>
<body>
<h1>⚡ NYN Explorer</h1>
<h3>Republic of Nowhere — NoyanCoin Blockchain</h3>
<div class="nav">
<a href="/">Explorer</a>
<a href="/leaderboard">Leaderboard</a>
{% if logged_in %}<a href="/wallet">My Wallet</a><a href="/logout" class="logout">Logout</a>
{% else %}<a href="/login">Login</a><a href="/register">Register</a>{% endif %}
</div>
<div class="lb-table">
<h2 style="text-align:center;margin-bottom:20px;">🏆 Top NYN Wallets</h2>
<div class="lb-header"><span>Rank</span><span>Username</span><span>Address</span><span>Balance</span></div>
{% for user in users %}
<div class="lb-row {{ 'gold' if loop.index == 1 else 'silver' if loop.index == 2 else 'bronze' if loop.index == 3 else '' }}">
<span class="lb-rank">#{{ loop.index }}</span>
<span class="lb-user">{{ user.username }}</span>
<span class="lb-addr">{{ user.wallet_address[:20] }}...</span>
<span class="lb-bal">{{ user.balance }} NYN</span>
</div>
{% endfor %}
</div>
</body></html>
"""

@app.route('/')
def explorer():
    s = Session()
    chain = get_chain()
    users = s.query(UserModel).count()
    txns = s.query(TransactionModel).count()
    s.close()
    logged_in = 'user_id' in session
    return render_template_string(HTML, chain=chain, blocks=len(chain), users=users, txns=txns, logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        captcha_token = request.form.get('g-recaptcha-response', '')
        if not verify_recaptcha(captcha_token):
            return render_template_string(REGISTER_HTML, msg="Please complete the captcha", msg_type="error", site_key=RECAPTCHA_SITE_KEY)
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        referral_input = request.form.get('referral', '').strip().upper()
        if len(username) < 3:
            return render_template_string(REGISTER_HTML, msg="Username must be at least 3 characters", msg_type="error", site_key=RECAPTCHA_SITE_KEY)
        if password != confirm:
            return render_template_string(REGISTER_HTML, msg="Passwords don't match", msg_type="error", site_key=RECAPTCHA_SITE_KEY)
        s = Session()
        if s.query(UserModel).filter_by(username=username).first():
            s.close()
            return render_template_string(REGISTER_HTML, msg="Username already taken", msg_type="error", site_key=RECAPTCHA_SITE_KEY)
        if s.query(UserModel).filter_by(email=email).first():
            s.close()
            return render_template_string(REGISTER_HTML, msg="Email already registered", msg_type="error", site_key=RECAPTCHA_SITE_KEY)
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        wallet_address, public_key = generate_wallet()
        referral_code = generate_referral_code()
        otp = ''.join(random.choices(string.digits, k=6))
        otp_expiry = time.time() + 600
        bonus = 50.0
        referred_by = None
        if referral_input:
            referrer = s.query(UserModel).filter_by(referral_code=referral_input).first()
            if referrer and referrer.referral_count < 3:
                referrer.balance += 20.0
                referrer.referral_count += 1
                bonus += 20.0
                referred_by = referral_input
                add_block({"event": "referral_bonus", "referrer": referrer.username, "amount": 20, "timestamp": time.time()})
                s.commit()
        user = UserModel(username=username, email=email, password=hashed, wallet_address=wallet_address, public_key=public_key, created_at=time.time(), balance=bonus, referral_code=referral_code, referral_count=0, referred_by=referred_by, otp=otp, otp_expiry=otp_expiry)
        s.add(user)
        s.commit()
        add_block({"event": "new_wallet", "address": wallet_address, "timestamp": time.time()})
        send_otp_email(email, otp)
        session['pending_user_id'] = user.id
        s.close()
        return redirect(url_for('verify_email'))
    return render_template_string(REGISTER_HTML, msg=None, msg_type=None, site_key=RECAPTCHA_SITE_KEY)

@app.route('/verify', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        otp_input = request.form.get('otp', '').strip()
        user_id = session.get('pending_user_id') or session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        s = Session()
        user = s.query(UserModel).filter_by(id=user_id).first()
        if not user:
            s.close()
            return redirect(url_for('login'))
        if user.otp == otp_input and time.time() < user.otp_expiry:
            user.is_verified = True
            user.otp = None
            s.commit()
            session.pop('pending_user_id', None)
            session['user_id'] = user.id
            session['username'] = user.username
            s.close()
            return redirect(url_for('wallet'))
        s.close()
        return render_template_string(VERIFY_HTML, msg="Invalid or expired OTP")
    return render_template_string(VERIFY_HTML, msg=None)

@app.route('/resend-otp')
def resend_otp():
    user_id = session.get('pending_user_id') or session.get('user_id')
    if user_id:
        s = Session()
        user = s.query(UserModel).filter_by(id=user_id).first()
        if user:
            otp = ''.join(random.choices(string.digits, k=6))
            user.otp = otp
            user.otp_expiry = time.time() + 600
            s.commit()
            send_otp_email(user.email, otp)
        s.close()
    return redirect(url_for('verify_email'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        s = Session()
        user = s.query(UserModel).filter_by(username=username).first()
        s.close()
        if user and bcrypt.check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            if not user.is_verified:
                session['pending_user_id'] = user.id
                return redirect(url_for('verify_email'))
            return redirect(url_for('wallet'))
        return render_template_string(LOGIN_HTML, msg="Invalid username or password")
    return render_template_string(LOGIN_HTML, msg=None)

@app.route('/wallet', methods=['GET'])
def wallet():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    txns = s.query(TransactionModel).filter(
        (TransactionModel.sender == user.wallet_address) |
        (TransactionModel.receiver == user.wallet_address)
    ).order_by(TransactionModel.timestamp.desc()).limit(10).all()
    s.close()
    tx_list = [{"sender": t.sender, "receiver": t.receiver, "amount": t.amount, "time": time.strftime('%Y-%m-%d %H:%M', time.localtime(t.timestamp))} for t in txns]
    import datetime
    created = datetime.datetime.fromtimestamp(user.created_at).strftime('%Y-%m-%d')
    msg = request.args.get('msg', None)
    msg_type = request.args.get('msg_type', None)
    return render_template_string(WALLET_HTML, username=user.username, wallet_address=user.wallet_address, balance=round(user.balance, 2), is_verified=user.is_verified, referral_code=user.referral_code, referral_count=user.referral_count, transactions=tx_list, created_at=created, msg=msg, msg_type=msg_type)

@app.route('/send', methods=['POST'])
@limiter.limit("10 per minute")
def send_nyn():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    receiver_addr = request.form.get('receiver', '').strip()
    try:
        amount = float(request.form.get('amount', 0))
    except:
        return redirect(url_for('wallet') + '?msg=Invalid amount&msg_type=error')
    s = Session()
    sender = s.query(UserModel).filter_by(id=session['user_id']).first()
    receiver = s.query(UserModel).filter_by(wallet_address=receiver_addr).first()
    if not receiver:
        s.close()
        return redirect(url_for('wallet') + '?msg=Wallet address not found&msg_type=error')
    if sender.wallet_address == receiver_addr:
        s.close()
        return redirect(url_for('wallet') + '?msg=Cannot send to yourself&msg_type=error')
    if amount <= 0 or sender.balance < amount:
        s.close()
        return redirect(url_for('wallet') + '?msg=Insufficient balance&msg_type=error')
    sender.balance -= amount
    receiver.balance += amount
    tx_hash = hashlib.sha256(f"{sender.wallet_address}{receiver_addr}{amount}{time.time()}".encode()).hexdigest()
    tx = TransactionModel(sender=sender.wallet_address, receiver=receiver_addr, amount=amount, timestamp=time.time(), tx_hash=tx_hash)
    s.add(tx)
    add_block({"from": sender.wallet_address, "to": receiver_addr, "amount": amount, "tx_hash": tx_hash})
    s.commit()
    s.close()
    return redirect(url_for('wallet') + f'?msg=Sent {amount} NYN successfully!&msg_type=success')

@app.route('/leaderboard')
def leaderboard():
    s = Session()
    users = s.query(UserModel).order_by(UserModel.balance.desc()).limit(20).all()
    s.close()
    logged_in = 'user_id' in session
    return render_template_string(LEADERBOARD_HTML, users=users, logged_in=logged_in)

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    s = Session()
    block = s.query(BlockModel).filter_by(hash=q).first()
    user = s.query(UserModel).filter_by(wallet_address=q).first()
    s.close()
    if block:
        return jsonify({"found": "block", "index": block.index, "hash": block.hash, "data": block.transactions})
    if user:
        return jsonify({"found": "wallet", "address": user.wallet_address, "balance_hidden": "NYN privacy enabled"})
    return jsonify({"found": "nothing", "query": q})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('explorer'))

@app.route('/add/<secret>/<data>')
@limiter.limit("5 per minute")
def add(secret, data):
    if secret != NYN_SECRET:
        return jsonify({"error": "Unauthorized"}), 403
    add_block({"data": data, "timestamp": time.time()})
    return jsonify({"message": "Block added!", "blocks": len(get_chain())})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)