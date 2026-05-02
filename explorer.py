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
        import sendgrid
        from sendgrid.helpers.mail import Mail
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        message = Mail(
            from_email=EMAIL_USER,
            to_emails=email,
            subject='NYN Wallet - Your Verification Code',
            plain_text_content=f"""
⚡ NYN NoyanCoin Verification

Your OTP code is: {otp}

This code expires in 10 minutes.

Republic of Nowhere - Currency of Everywhere
            """
        )
        sg.send(message)
        return True
    except Exception as e:
        print(f"Email error: {e}")
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

BASE_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {
  --bg: #0d1117;
  --bg2: #161b22;
  --bg3: #21262d;
  --border: #30363d;
  --text: #e6edf3;
  --text2: #8b949e;
  --green: #00ff88;
  --green2: #00cc6a;
  --orange: #f0883e;
  --red: #f85149;
  --blue: #58a6ff;
  --yellow: #e3b341;
}
.light {
  --bg: #ffffff;
  --bg2: #f6f8fa;
  --bg3: #eaeef2;
  --border: #d0d7de;
  --text: #1f2328;
  --text2: #636c76;
  --green: #1a7f37;
  --green2: #2da44e;
  --orange: #bc4c00;
  --red: #cf222e;
  --blue: #0969da;
  --yellow: #9a6700;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; min-height: 100vh; }
a { color: var(--green); text-decoration: none; }
a:hover { text-decoration: underline; }

/* NAVBAR */
.navbar { background: var(--bg2); border-bottom: 1px solid var(--border); padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 64px; position: sticky; top: 0; z-index: 100; }
.navbar-brand { display: flex; align-items: center; gap: 10px; font-size: 1.3em; font-weight: 700; color: var(--green); }
.navbar-brand span { color: var(--text); font-weight: 400; font-size: 0.75em; }
.navbar-links { display: flex; align-items: center; gap: 8px; }
.nav-btn { padding: 7px 16px; border-radius: 6px; font-size: 0.875em; font-weight: 500; border: 1px solid var(--border); background: transparent; color: var(--text); cursor: pointer; transition: all 0.2s; text-decoration: none; display: inline-block; }
.nav-btn:hover { background: var(--bg3); text-decoration: none; }
.nav-btn.primary { background: var(--green); color: #000; border-color: var(--green); font-weight: 600; }
.nav-btn.primary:hover { background: var(--green2); }
.nav-btn.danger { border-color: var(--red); color: var(--red); }
.nav-btn.danger:hover { background: var(--red); color: #fff; }
.theme-toggle { background: none; border: 1px solid var(--border); color: var(--text2); padding: 7px 12px; border-radius: 6px; cursor: pointer; font-size: 1em; }

/* HERO */
.hero { background: linear-gradient(135deg, var(--bg2) 0%, var(--bg) 100%); border-bottom: 1px solid var(--border); padding: 48px 24px; text-align: center; }
.hero h1 { font-size: 2.5em; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.hero h1 span { color: var(--green); }
.hero p { color: var(--text2); font-size: 1.1em; margin-bottom: 24px; }
.hero-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.hero-btn { padding: 12px 28px; border-radius: 8px; font-size: 1em; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s; text-decoration: none; }
.hero-btn.primary { background: var(--green); color: #000; }
.hero-btn.primary:hover { background: var(--green2); text-decoration: none; }
.hero-btn.secondary { background: transparent; color: var(--text); border: 1px solid var(--border); }
.hero-btn.secondary:hover { background: var(--bg3); text-decoration: none; }

/* STATS */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; padding: 24px; max-width: 1100px; margin: 0 auto; }
.stat-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px; padding: 20px; text-align: center; transition: border-color 0.2s; }
.stat-card:hover { border-color: var(--green); }
.stat-card .value { font-size: 1.8em; font-weight: 700; color: var(--green); }
.stat-card .label { font-size: 0.85em; color: var(--text2); margin-top: 4px; }

/* SEARCH */
.search-section { max-width: 700px; margin: 0 auto; padding: 0 24px 24px; }
.search-bar { display: flex; gap: 8px; }
.search-bar input { flex: 1; padding: 12px 16px; background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: 0.95em; outline: none; transition: border-color 0.2s; }
.search-bar input:focus { border-color: var(--green); }
.search-bar button { padding: 12px 24px; background: var(--green); color: #000; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }

/* BLOCKS */
.blocks-section { max-width: 1100px; margin: 0 auto; padding: 0 24px 40px; }
.section-title { font-size: 1.1em; font-weight: 600; color: var(--text2); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.block-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; transition: border-color 0.2s; }
.block-card:hover { border-color: var(--green); }
.block-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.block-num { font-size: 1em; font-weight: 700; color: var(--green); }
.block-time { font-size: 0.8em; color: var(--text2); }
.block-hash { font-size: 0.8em; color: var(--orange); word-break: break-all; margin-bottom: 4px; font-family: monospace; }
.block-data { font-size: 0.85em; color: var(--text2); font-family: monospace; }

/* FORMS */
.form-page { min-height: calc(100vh - 64px); display: flex; align-items: center; justify-content: center; padding: 24px; }
.form-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 36px; width: 100%; max-width: 420px; }
.form-card h2 { font-size: 1.4em; font-weight: 700; margin-bottom: 6px; color: var(--text); }
.form-card .subtitle { color: var(--text2); font-size: 0.9em; margin-bottom: 24px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 0.875em; font-weight: 500; color: var(--text2); margin-bottom: 6px; }
.form-group input { width: 100%; padding: 10px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: 0.95em; outline: none; transition: border-color 0.2s; }
.form-group input:focus { border-color: var(--green); }
.btn-full { width: 100%; padding: 12px; background: var(--green); color: #000; border: none; border-radius: 8px; font-size: 1em; font-weight: 600; cursor: pointer; margin-top: 8px; transition: background 0.2s; }
.btn-full:hover { background: var(--green2); }
.form-footer { text-align: center; margin-top: 20px; font-size: 0.875em; color: var(--text2); }
.alert { padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 0.875em; }
.alert.error { background: rgba(248,81,73,0.1); border: 1px solid var(--red); color: var(--red); }
.alert.success { background: rgba(0,255,136,0.1); border: 1px solid var(--green); color: var(--green); }
.alert.info { background: rgba(88,166,255,0.1); border: 1px solid var(--blue); color: var(--blue); }
.bonus-badge { background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.3); border-radius: 8px; padding: 10px 14px; margin-bottom: 20px; font-size: 0.875em; color: var(--green); text-align: center; }
.recaptcha-wrap { display: flex; justify-content: center; margin: 16px 0; transform: scale(0.9); }

/* WALLET PAGE */
.wallet-page { max-width: 800px; margin: 0 auto; padding: 24px; }
.wallet-header { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 28px; margin-bottom: 20px; }
.wallet-user { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.wallet-avatar { width: 52px; height: 52px; background: var(--green); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4em; font-weight: 700; color: #000; }
.wallet-name { font-size: 1.3em; font-weight: 700; }
.verified-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75em; font-weight: 600; margin-left: 8px; }
.verified-badge.yes { background: rgba(0,255,136,0.15); color: var(--green); border: 1px solid var(--green); }
.verified-badge.no { background: rgba(248,81,73,0.15); color: var(--red); border: 1px solid var(--red); }
.balance-section { text-align: center; padding: 20px; background: var(--bg); border-radius: 12px; margin-bottom: 16px; }
.balance-label { font-size: 0.85em; color: var(--text2); margin-bottom: 6px; }
.balance-amount { font-size: 2.5em; font-weight: 700; color: var(--green); }
.balance-sub { font-size: 0.9em; color: var(--text2); margin-top: 4px; }
.balance-hidden { font-size: 1.1em; color: var(--text2); letter-spacing: 6px; }
.addr-box { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; font-family: monospace; font-size: 0.85em; color: var(--orange); word-break: break-all; margin-bottom: 8px; }
.copy-btn { background: var(--bg3); border: 1px solid var(--border); color: var(--text2); padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.8em; transition: all 0.2s; }
.copy-btn:hover { border-color: var(--green); color: var(--green); }
.qr-wrap { display: flex; justify-content: center; margin: 16px 0; padding: 16px; background: white; border-radius: 10px; width: fit-content; margin: 16px auto; }
.wallet-section { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 16px; }
.wallet-section h3 { font-size: 1em; font-weight: 600; color: var(--text); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.send-input { width: 100%; padding: 10px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: 0.95em; outline: none; margin-bottom: 10px; transition: border-color 0.2s; }
.send-input:focus { border-color: var(--green); }
.send-btn { width: 100%; padding: 12px; background: var(--green); color: #000; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.95em; }
.referral-code { font-size: 1.5em; font-weight: 700; color: var(--green); font-family: monospace; letter-spacing: 3px; }
.tx-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border); }
.tx-item:last-child { border-bottom: none; }
.tx-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1em; margin-right: 12px; flex-shrink: 0; }
.tx-icon.in { background: rgba(0,255,136,0.15); color: var(--green); }
.tx-icon.out { background: rgba(248,81,73,0.15); color: var(--red); }
.tx-info { flex: 1; }
.tx-addr { font-size: 0.8em; color: var(--text2); font-family: monospace; }
.tx-time { font-size: 0.75em; color: var(--text2); }
.tx-amount { font-weight: 700; }
.tx-amount.in { color: var(--green); }
.tx-amount.out { color: var(--red); }
.privacy-notice { background: rgba(88,166,255,0.08); border: 1px solid rgba(88,166,255,0.3); border-radius: 8px; padding: 10px 14px; font-size: 0.8em; color: var(--blue); margin-top: 8px; }

/* VERIFY */
.otp-input { font-size: 2em; text-align: center; letter-spacing: 12px; font-family: monospace; font-weight: 700; }

/* FOOTER */
.footer { background: var(--bg2); border-top: 1px solid var(--border); padding: 24px; text-align: center; color: var(--text2); font-size: 0.85em; margin-top: 40px; }

/* RESPONSIVE */
@media (max-width: 600px) {
  .hero h1 { font-size: 1.8em; }
  .navbar-links .nav-btn span { display: none; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
<script>
function toggleTheme() {
  document.body.classList.toggle('light');
  localStorage.setItem('theme', document.body.classList.contains('light') ? 'light' : 'dark');
}
window.onload = function() {
  if(localStorage.getItem('theme') === 'light') document.body.classList.add('light');
}
</script>
"""

MAIN_HTML = """
<!DOCTYPE html><html><head><title>NYN Explorer - NoyanCoin</title>""" + BASE_STYLE + """</head>
<body>
<nav class="navbar">
  <div class="navbar-brand">⚡ NYN <span>NoyanCoin Explorer</span></div>
  <div class="navbar-links">
    <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
    {% if logged_in %}
    <a href="/wallet" class="nav-btn">My Wallet</a>
    <a href="/logout" class="nav-btn danger">Logout</a>
    {% else %}
    <a href="/login" class="nav-btn">Login</a>
    <a href="/register" class="nav-btn primary">Get Wallet</a>
    {% endif %}
  </div>
</nav>

<div class="hero">
  <h1>⚡ <span>NYN</span> Blockchain Explorer</h1>
  <p>Republic of Nowhere — Private. Human. Borderless.</p>
  {% if not logged_in %}
  <div class="hero-btns">
    <a href="/register" class="hero-btn primary">Create Free Wallet</a>
    <a href="#blocks" class="hero-btn secondary">Explore Blocks</a>
  </div>
  {% endif %}
</div>

<div class="stats-grid">
  <div class="stat-card"><div class="value">{{ blocks }}</div><div class="label">Total Blocks</div></div>
  <div class="stat-card"><div class="value">24M</div><div class="label">Total Supply (NYN)</div></div>
  <div class="stat-card"><div class="value">{{ users }}</div><div class="label">Wallets Created</div></div>
  <div class="stat-card"><div class="value">{{ txns }}</div><div class="label">Transactions</div></div>
  <div class="stat-card"><div class="value">~2s</div><div class="label">Block Time</div></div>
</div>

<div class="search-section">
  <div class="search-bar">
    <input type="text" id="searchInput" placeholder="Search by block hash or wallet address...">
    <button onclick="window.location.href='/search?q='+document.getElementById('searchInput').value">Search</button>
  </div>
</div>

<div class="blocks-section" id="blocks">
  <div class="section-title">📦 Latest Blocks</div>
  {% for block in chain|reverse %}
  <div class="block-card">
    <div class="block-header">
      <span class="block-num">Block #{{ block.index }}</span>
      <span class="block-time">{{ block.index }}</span>
    </div>
    <div class="block-hash">🔗 {{ block.hash }}</div>
    <div class="block-hash" style="color:#8b949e;">◀ {{ block.previous_hash }}</div>
    <div class="block-data">📄 {{ block.transactions }}</div>
  </div>
  {% endfor %}
</div>

<div class="footer">
  <p>⚡ NYN NoyanCoin — Republic of Nowhere — Currency of Everywhere</p>
  <p style="margin-top:8px;">Balance privacy enabled. Human verified network.</p>
</div>
</body></html>
"""

REGISTER_HTML = """
<!DOCTYPE html><html><head><title>Create Wallet - NYN</title>""" + BASE_STYLE + """
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head>
<body>
<nav class="navbar">
  <div class="navbar-brand">⚡ NYN <span>NoyanCoin</span></div>
  <div class="navbar-links">
    <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
    <a href="/" class="nav-btn">Explorer</a>
    <a href="/login" class="nav-btn">Login</a>
  </div>
</nav>
<div class="form-page">
<div class="form-card">
  <h2>Create Your Wallet</h2>
  <p class="subtitle">Join the Republic of Nowhere</p>
  <div class="bonus-badge">🎁 50 NYN free on registration + 20 NYN per referral</div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="form-group"><label>Username</label><input type="text" name="username" placeholder="Choose a username" required maxlength="30"></div>
    <div class="form-group"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div class="form-group"><label>Password</label><input type="password" name="password" placeholder="Min 8 characters" required minlength="8"></div>
    <div class="form-group"><label>Confirm Password</label><input type="password" name="confirm" placeholder="Repeat password" required></div>
    <div class="form-group"><label>Referral Code (optional)</label><input type="text" name="referral" placeholder="Enter referral code for +20 NYN"></div>
    <div class="recaptcha-wrap"><div class="g-recaptcha" data-sitekey="{{ site_key }}"></div></div>
    <button type="submit" class="btn-full">Create Wallet & Get 50 NYN ⚡</button>
  </form>
  <div class="form-footer">Already have a wallet? <a href="/login">Login</a></div>
</div>
</div>
</body></html>
"""

VERIFY_HTML = """
<!DOCTYPE html><html><head><title>Verify Email - NYN</title>""" + BASE_STYLE + """</head>
<body>
<nav class="navbar">
  <div class="navbar-brand">⚡ NYN <span>NoyanCoin</span></div>
  <div class="navbar-links"><button class="theme-toggle" onclick="toggleTheme()">🌙</button></div>
</nav>
<div class="form-page">
<div class="form-card">
  <h2>Verify Your Email</h2>
  <p class="subtitle">Enter the 6-digit code sent to your email</p>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <div class="alert info">📧 Check your inbox for the verification code</div>
  <form method="POST">
    <div class="form-group">
      <label>Verification Code</label>
      <input type="text" name="otp" class="otp-input" placeholder="000000" maxlength="6" required autocomplete="off">
    </div>
    <button type="submit" class="btn-full">Verify & Activate ⚡</button>
  </form>
  <div class="form-footer"><a href="/resend-otp">Resend verification code</a></div>
</div>
</div>
</body></html>
"""

LOGIN_HTML = """
<!DOCTYPE html><html><head><title>Login - NYN</title>""" + BASE_STYLE + """</head>
<body>
<nav class="navbar">
  <div class="navbar-brand">⚡ NYN <span>NoyanCoin</span></div>
  <div class="navbar-links">
    <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
    <a href="/" class="nav-btn">Explorer</a>
    <a href="/register" class="nav-btn primary">Get Wallet</a>
  </div>
</nav>
<div class="form-page">
<div class="form-card">
  <h2>Welcome Back</h2>
  <p class="subtitle">Login to your NYN wallet</p>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="form-group"><label>Username</label><input type="text" name="username" placeholder="Your username" required></div>
    <div class="form-group"><label>Password</label><input type="password" name="password" placeholder="Your password" required></div>
    <button type="submit" class="btn-full">Login ⚡</button>
  </form>
  <div class="form-footer">No wallet yet? <a href="/register">Create one free</a></div>
</div>
</div>
</body></html>
"""

WALLET_HTML = """
<!DOCTYPE html><html><head><title>My Wallet - NYN</title>""" + BASE_STYLE + """
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head>
<body>
<nav class="navbar">
  <div class="navbar-brand">⚡ NYN <span>NoyanCoin</span></div>
  <div class="navbar-links">
    <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
    <a href="/" class="nav-btn">Explorer</a>
    <a href="/logout" class="nav-btn danger">Logout</a>
  </div>
</nav>

<div class="wallet-page">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}

  <div class="wallet-header">
    <div class="wallet-user">
      <div class="wallet-avatar">{{ username[0].upper() }}</div>
      <div>
        <div class="wallet-name">{{ username }} <span class="verified-badge {{ 'yes' if is_verified else 'no' }}">{{ '✓ Verified' if is_verified else '✗ Unverified' }}</span></div>
        <div style="font-size:0.85em;color:var(--text2);">Member since {{ created_at }}</div>
      </div>
    </div>

    <div class="balance-section">
      <div class="balance-label">Your Balance</div>
      <div class="balance-amount" id="balanceDisplay">••••••</div>
      <div class="balance-sub">
        <button onclick="toggleBalance()" style="background:none;border:none;color:var(--text2);cursor:pointer;font-size:0.85em;">👁 Show / Hide Balance</button>
      </div>
      <div class="privacy-notice">🔒 Your balance is private. Only you can see it.</div>
    </div>

    <div style="margin-top:16px;">
      <div style="font-size:0.85em;color:var(--text2);margin-bottom:6px;">Wallet Address</div>
      <div class="addr-box" id="walletAddr">{{ wallet_address }}</div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ wallet_address }}');this.textContent='Copied!'">📋 Copy Address</button>
    </div>
    <div class="qr-wrap"><div id="qrcode"></div></div>
  </div>

  {% if not is_verified %}
  <div class="wallet-section" style="border-color:var(--red);">
    <h3>⚠️ Verify Your Email</h3>
    <p style="color:var(--text2);font-size:0.9em;margin-bottom:12px;">Verify your email to unlock sending NYN and full features.</p>
    <a href="/verify" class="send-btn" style="display:block;text-align:center;padding:10px;border-radius:8px;text-decoration:none;color:#000;">Verify Email Now</a>
  </div>
  {% endif %}

  <div class="wallet-section">
    <h3>💸 Send NYN</h3>
    <form method="POST" action="/send">
      <input type="text" name="receiver" class="send-input" placeholder="Receiver wallet address (NYN...)" required>
      <input type="number" name="amount" class="send-input" placeholder="Amount in NYN" step="0.01" min="0.01" required>
      <button type="submit" class="send-btn">Send NYN ⚡</button>
    </form>
  </div>

  <div class="wallet-section">
    <h3>🎁 Referral Program</h3>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:12px;">Share your code and earn 20 NYN per referral (max 3 referrals)</p>
    <div class="referral-code">{{ referral_code }}</div>
    <button class="copy-btn" style="margin-top:10px;" onclick="navigator.clipboard.writeText('{{ referral_code }}');this.textContent='Copied!'">📋 Copy Code</button>
    <p style="color:var(--text2);font-size:0.8em;margin-top:8px;">Referrals used: {{ referral_count }}/3</p>
  </div>

  <div class="wallet-section">
    <h3>📋 Transaction History</h3>
    {% if transactions %}
    {% for tx in transactions %}
    <div class="tx-item">
      <div class="tx-icon {{ 'in' if tx.receiver == wallet_address else 'out' }}">{{ '↓' if tx.receiver == wallet_address else '↑' }}</div>
      <div class="tx-info">
        <div class="tx-addr">{{ tx.sender[:24] if tx.receiver == wallet_address else tx.receiver[:24] }}...</div>
        <div class="tx-time">{{ tx.time }}</div>
      </div>
      <div class="tx-amount {{ 'in' if tx.receiver == wallet_address else 'out' }}">{{ '+' if tx.receiver == wallet_address else '-' }}{{ tx.amount }} NYN</div>
    </div>
    {% endfor %}
    {% else %}
    <p style="color:var(--text2);font-size:0.9em;">No transactions yet. Send or receive NYN to see history.</p>
    {% endif %}
  </div>
</div>

<div class="footer">
  <p>⚡ NYN NoyanCoin — Republic of Nowhere</p>
</div>

<script>
var balanceVisible = false;
var realBalance = "{{ balance }} NYN";
function toggleBalance() {
  balanceVisible = !balanceVisible;
  document.getElementById('balanceDisplay').textContent = balanceVisible ? realBalance : '••••••';
}
new QRCode(document.getElementById("qrcode"), {
  text: "{{ wallet_address }}",
  width: 128,
  height: 128,
  colorDark: "#000000",
  colorLight: "#ffffff"
});
</script>
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
    return render_template_string(MAIN_HTML, chain=chain, blocks=len(chain), users=users, txns=txns, logged_in=logged_in)

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
                s.commit()
        user = UserModel(username=username, email=email, password=hashed, wallet_address=wallet_address, public_key=public_key, created_at=time.time(), balance=bonus, referral_code=referral_code, referral_count=0, referred_by=referred_by, otp=otp, otp_expiry=otp_expiry)
        s.add(user)
        s.commit()
        add_block({"event": "new_wallet", "address": wallet_address[:20]+"...", "timestamp": time.time()})
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
        return render_template_string(VERIFY_HTML, msg="Invalid or expired code. Please try again.")
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

@app.route('/wallet')
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
    tx_list = [{"sender": t.sender, "receiver": t.receiver, "amount": t.amount, "time": time.strftime('%b %d, %H:%M', time.localtime(t.timestamp))} for t in txns]
    import datetime
    created = datetime.datetime.fromtimestamp(user.created_at).strftime('%b %d, %Y')
    msg = request.args.get('msg', None)
    msg_type = request.args.get('msg_type', 'success')
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
        return redirect(url_for('wallet') + '?msg=Invalid+amount&msg_type=error')
    s = Session()
    sender = s.query(UserModel).filter_by(id=session['user_id']).first()
    receiver = s.query(UserModel).filter_by(wallet_address=receiver_addr).first()
    if not receiver:
        s.close()
        return redirect(url_for('wallet') + '?msg=Wallet+not+found&msg_type=error')
    if sender.wallet_address == receiver_addr:
        s.close()
        return redirect(url_for('wallet') + '?msg=Cannot+send+to+yourself&msg_type=error')
    if amount <= 0 or sender.balance < amount:
        s.close()
        return redirect(url_for('wallet') + '?msg=Insufficient+balance&msg_type=error')
    sender.balance -= amount
    receiver.balance += amount
    tx_hash = hashlib.sha256(f"{sender.wallet_address}{receiver_addr}{amount}{time.time()}".encode()).hexdigest()
    tx = TransactionModel(sender=sender.wallet_address, receiver=receiver_addr, amount=amount, timestamp=time.time(), tx_hash=tx_hash)
    s.add(tx)
    add_block({"tx": tx_hash[:20]+"...", "amount": amount, "timestamp": time.time()})
    s.commit()
    s.close()
    return redirect(url_for('wallet') + f'?msg=Sent+{amount}+NYN+successfully&msg_type=success')

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    s = Session()
    block = s.query(BlockModel).filter_by(hash=q).first()
    user = s.query(UserModel).filter_by(wallet_address=q).first()
    s.close()
    if block:
        return jsonify({"found": "block", "index": block.index, "hash": block.hash})
    if user:
        return jsonify({"found": "wallet", "address": user.wallet_address, "balance": "🔒 Private", "verified": user.is_verified})
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