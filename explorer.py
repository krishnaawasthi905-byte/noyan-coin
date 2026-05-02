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
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

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
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")
NYN_SECRET = os.environ.get("NYN_SECRET", "fallback")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")

NYN_GENESIS_DATE = "2026-04-30"
NYN_ALGORITHM = "Proof of Stake (PoS)"
NYN_MAX_SUPPLY = 24000000
NYN_CIRCULATING = 0

class BlockModel(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    timestamp = Column(Float)
    transactions = Column(Text)
    previous_hash = Column(String(64))
    hash = Column(String(64))
    validator = Column(String(100), default="Genesis")
    tx_count = Column(Integer, default=0)

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
    staked_amount = Column(Float, default=0.0)
    referral_code = Column(String(10), unique=True)
    referral_count = Column(Integer, default=0)
    referred_by = Column(String(10), nullable=True)
    otp = Column(String(6), nullable=True)
    otp_expiry = Column(Float, nullable=True)
    total_sent = Column(Float, default=0.0)
    total_received = Column(Float, default=0.0)

class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    sender = Column(String(100))
    receiver = Column(String(100))
    amount = Column(Float)
    timestamp = Column(Float)
    tx_hash = Column(String(64))
    status = Column(String(20), default="confirmed")
    block_index = Column(Integer, default=0)
    fee = Column(Float, default=0.0)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def calculate_hash(index, timestamp, transactions, previous_hash, validator=""):
    block_string = json.dumps({
        "index": index,
        "timestamp": timestamp,
        "transactions": transactions,
        "previous_hash": previous_hash,
        "validator": validator
    }, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

def verify_transaction(sender_address, receiver_address, amount, sender_balance):
    errors = []
    if not receiver_address.startswith("NYN"):
        errors.append("Invalid NYN address format")
    if amount <= 0:
        errors.append("Amount must be greater than 0")
    if sender_balance < amount:
        errors.append(f"Insufficient balance. You have {sender_balance} NYN")
    if sender_address == receiver_address:
        errors.append("Cannot send to yourself")
    if amount > 10000:
        errors.append("Single transaction limit is 10,000 NYN")
    return errors

def select_validator(session_db):
    validators = session_db.query(UserModel).filter(
        UserModel.staked_amount > 0,
        UserModel.is_verified == True
    ).order_by(UserModel.staked_amount.desc()).first()
    if validators:
        return validators.wallet_address
    return "NYN-PoS-System"

def get_chain():
    s = Session()
    blocks = s.query(BlockModel).order_by(BlockModel.index).all()
    s.close()
    return blocks

def add_block(transactions, validator="System"):
    s = Session()
    chain = s.query(BlockModel).order_by(BlockModel.index).all()
    previous_hash = "0" if len(chain) == 0 else chain[-1].hash
    index = len(chain)
    timestamp = time.time()
    h = calculate_hash(index, timestamp, json.dumps(transactions), previous_hash, validator)
    tx_count = 1 if isinstance(transactions, dict) else 0
    block = BlockModel(
        index=index,
        timestamp=timestamp,
        transactions=json.dumps(transactions),
        previous_hash=previous_hash,
        hash=h,
        validator=validator,
        tx_count=tx_count
    )
    s.add(block)
    s.commit()
    s.close()
    return h

def generate_wallet():
    private_key = os.urandom(32)
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    public_key = signing_key.get_verifying_key()
    pub_hash = hashlib.sha256(public_key.to_string()).hexdigest()
    address = "NYN" + pub_hash[:32].upper()
    return address, public_key.to_string().hex()

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def send_otp_email(email, otp, username="User"):
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, HtmlContent
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        html_content = f"""
        <div style="background:#0d1117;padding:40px;font-family:monospace;max-width:500px;margin:0 auto;border-radius:12px;border:1px solid #30363d;">
            <h1 style="color:#00ff88;text-align:center;">⚡ NYN NoyanCoin</h1>
            <p style="color:#8b949e;text-align:center;">Email Verification</p>
            <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;text-align:center;margin:24px 0;">
                <p style="color:#8b949e;margin-bottom:8px;">Your verification code:</p>
                <h2 style="color:#00ff88;font-size:2.5em;letter-spacing:12px;">{otp}</h2>
                <p style="color:#8b949e;font-size:0.85em;">Expires in 10 minutes</p>
            </div>
            <p style="color:#8b949e;text-align:center;font-size:0.85em;">Republic of Nowhere — Currency of Everywhere</p>
        </div>
        """
        message = Mail(
            from_email=EMAIL_USER,
            to_emails=email,
            subject='⚡ NYN Wallet - Verification Code',
            html_content=html_content
        )
        sg.send(message)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def verify_recaptcha(token):
    if not RECAPTCHA_SECRET_KEY:
        return True
    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': token
        })
        return response.json().get('success', False)
    except:
        return True

def get_circulating_supply():
    s = Session()
    total = s.query(UserModel).count() * 50
    s.close()
    return min(total, NYN_MAX_SUPPLY)

s = Session()
if s.query(BlockModel).count() == 0:
    add_block("NYN Genesis Block - Republic of Nowhere", "Founder")
    add_block({"from": "Founder", "to": "Republic of Nowhere", "amount": 24000000}, "Founder")
s.close()

STYLES = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--border:#30363d;--text:#e6edf3;--text2:#8b949e;--green:#00ff88;--green2:#00cc6a;--orange:#f0883e;--red:#f85149;--blue:#58a6ff;--yellow:#e3b341;--purple:#a371f7;}
.light{--bg:#ffffff;--bg2:#f6f8fa;--bg3:#eaeef2;--border:#d0d7de;--text:#1f2328;--text2:#636c76;--green:#1a7f37;--green2:#2da44e;--orange:#bc4c00;--red:#cf222e;--blue:#0969da;--yellow:#9a6700;--purple:#8250df;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;}
a{color:var(--green);text-decoration:none;}
a:hover{text-decoration:underline;}
.navbar{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:64px;position:sticky;top:0;z-index:100;}
.navbar-brand{display:flex;align-items:center;gap:10px;font-size:1.2em;font-weight:700;color:var(--green);}
.navbar-brand span{color:var(--text2);font-weight:400;font-size:0.8em;}
.navbar-links{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.nav-btn{padding:7px 16px;border-radius:6px;font-size:0.875em;font-weight:500;border:1px solid var(--border);background:transparent;color:var(--text);cursor:pointer;transition:all 0.2s;text-decoration:none;display:inline-block;}
.nav-btn:hover{background:var(--bg3);text-decoration:none;}
.nav-btn.primary{background:var(--green);color:#000;border-color:var(--green);font-weight:600;}
.nav-btn.primary:hover{background:var(--green2);}
.nav-btn.danger{border-color:var(--red);color:var(--red);}
.nav-btn.danger:hover{background:var(--red);color:#fff;}
.theme-btn{background:none;border:1px solid var(--border);color:var(--text2);padding:7px 12px;border-radius:6px;cursor:pointer;font-size:1em;}
.hero{background:var(--bg2);border-bottom:1px solid var(--border);padding:48px 24px;text-align:center;}
.hero h1{font-size:2.5em;font-weight:700;margin-bottom:8px;}
.hero h1 span{color:var(--green);}
.hero p{color:var(--text2);font-size:1.1em;margin-bottom:24px;}
.hero-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
.hero-btn{padding:12px 28px;border-radius:8px;font-size:1em;font-weight:600;cursor:pointer;border:none;transition:all 0.2s;text-decoration:none;display:inline-block;}
.hero-btn.primary{background:var(--green);color:#000;}
.hero-btn.primary:hover{background:var(--green2);text-decoration:none;}
.hero-btn.secondary{background:transparent;color:var(--text);border:1px solid var(--border);}
.hero-btn.secondary:hover{background:var(--bg3);text-decoration:none;}
.container{max-width:1200px;margin:0 auto;padding:0 24px;}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;padding:24px 0;}
.stat-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center;transition:border-color 0.2s;}
.stat-card:hover{border-color:var(--green);}
.stat-card .val{font-size:1.6em;font-weight:700;color:var(--green);}
.stat-card .lbl{font-size:0.8em;color:var(--text2);margin-top:4px;}
.market-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin:16px 0;}
.market-card{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:16px;}
.market-card .m-label{font-size:0.8em;color:var(--text2);margin-bottom:4px;}
.market-card .m-value{font-size:1.1em;font-weight:600;color:var(--text);}
.market-card .m-value.green{color:var(--green);}
.market-card .m-value.orange{color:var(--orange);}
.blocks-visual{display:flex;gap:8px;overflow-x:auto;padding:16px 0;scrollbar-width:thin;}
.block-vis{min-width:80px;height:80px;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:transform 0.2s;font-size:0.75em;font-weight:600;}
.block-vis:hover{transform:translateY(-4px);}
.block-vis .bn{font-size:0.8em;color:rgba(255,255,255,0.7);}
.block-vis .bt{font-size:0.65em;color:rgba(255,255,255,0.5);margin-top:2px;}
.section-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px;}
.section-title{font-size:1em;font-weight:600;color:var(--text);margin-bottom:16px;display:flex;align-items:center;gap:8px;}
.block-row{display:grid;grid-template-columns:80px 1fr 1fr 1fr;gap:16px;padding:12px 0;border-bottom:1px solid var(--border);align-items:center;font-size:0.875em;}
.block-row:last-child{border-bottom:none;}
.block-num-badge{background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:4px 10px;font-weight:600;color:var(--green);text-align:center;font-family:monospace;}
.hash-text{font-family:monospace;color:var(--orange);font-size:0.8em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.search-bar{display:flex;gap:8px;margin-bottom:24px;}
.search-bar input{flex:1;padding:12px 16px;background:var(--bg2);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;transition:border-color 0.2s;}
.search-bar input:focus{border-color:var(--green);}
.search-bar button{padding:12px 24px;background:var(--green);color:#000;border:none;border-radius:8px;font-weight:600;cursor:pointer;}
.form-page{min-height:calc(100vh - 64px);display:flex;align-items:center;justify-content:center;padding:24px;}
.form-card{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:36px;width:100%;max-width:440px;}
.form-card h2{font-size:1.4em;font-weight:700;margin-bottom:4px;}
.form-card .sub{color:var(--text2);font-size:0.9em;margin-bottom:24px;}
.fg{margin-bottom:14px;}
.fg label{display:block;font-size:0.875em;font-weight:500;color:var(--text2);margin-bottom:6px;}
.fg input{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;transition:border-color 0.2s;}
.fg input:focus{border-color:var(--green);}
.input-wrap{position:relative;}
.input-wrap input{padding-right:44px;}
.eye-btn{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--text2);cursor:pointer;font-size:1em;padding:0;}
.btn-full{width:100%;padding:12px;background:var(--green);color:#000;border:none;border-radius:8px;font-size:1em;font-weight:600;cursor:pointer;margin-top:8px;transition:background 0.2s;}
.btn-full:hover{background:var(--green2);}
.form-footer{text-align:center;margin-top:20px;font-size:0.875em;color:var(--text2);}
.alert{padding:12px 16px;border-radius:8px;margin-bottom:16px;font-size:0.875em;}
.alert.error{background:rgba(248,81,73,0.1);border:1px solid var(--red);color:var(--red);}
.alert.success{background:rgba(0,255,136,0.1);border:1px solid var(--green);color:var(--green);}
.alert.info{background:rgba(88,166,255,0.1);border:1px solid var(--blue);color:var(--blue);}
.alert.warning{background:rgba(227,179,65,0.1);border:1px solid var(--yellow);color:var(--yellow);}
.bonus-badge{background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.25);border-radius:8px;padding:10px 14px;margin-bottom:20px;font-size:0.875em;color:var(--green);text-align:center;}
.recaptcha-wrap{display:flex;justify-content:center;margin:16px 0;transform:scale(0.9);transform-origin:center;}
.wallet-page{max-width:900px;margin:0 auto;padding:24px;}
.wallet-header{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:28px;margin-bottom:16px;}
.wallet-user{display:flex;align-items:center;gap:16px;margin-bottom:20px;}
.avatar{width:52px;height:52px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.4em;font-weight:700;color:#000;}
.wname{font-size:1.3em;font-weight:700;}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.75em;font-weight:600;margin-left:8px;}
.badge.v{background:rgba(0,255,136,0.15);color:var(--green);border:1px solid var(--green);}
.badge.u{background:rgba(248,81,73,0.15);color:var(--red);border:1px solid var(--red);}
.balance-box{text-align:center;padding:24px;background:var(--bg);border-radius:12px;margin-bottom:16px;border:1px solid var(--border);}
.bal-label{font-size:0.85em;color:var(--text2);margin-bottom:8px;}
.bal-amount{font-size:2.8em;font-weight:700;color:var(--green);font-family:monospace;}
.bal-dots{font-size:2em;letter-spacing:8px;color:var(--green);}
.bal-sub{font-size:0.85em;color:var(--text2);margin-top:8px;}
.show-btn{background:none;border:none;color:var(--text2);cursor:pointer;font-size:0.85em;padding:6px 12px;border-radius:6px;transition:color 0.2s;}
.show-btn:hover{color:var(--text);}
.privacy-note{background:rgba(88,166,255,0.08);border:1px solid rgba(88,166,255,0.25);border-radius:8px;padding:10px 14px;font-size:0.8em;color:var(--blue);margin-top:8px;}
.addr-box{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:12px 16px;font-family:monospace;font-size:0.85em;color:var(--orange);word-break:break-all;margin-bottom:8px;}
.copy-btn{background:var(--bg3);border:1px solid var(--border);color:var(--text2);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8em;transition:all 0.2s;}
.copy-btn:hover{border-color:var(--green);color:var(--green);}
.qr-wrap{display:flex;justify-content:center;margin:16px auto;padding:16px;background:white;border-radius:10px;width:fit-content;}
.wsection{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:24px;margin-bottom:16px;}
.wsection h3{font-size:1em;font-weight:600;margin-bottom:16px;display:flex;align-items:center;gap:8px;}
.send-input{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;margin-bottom:10px;transition:border-color 0.2s;}
.send-input:focus{border-color:var(--green);}
.send-btn{width:100%;padding:12px;background:var(--green);color:#000;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.95em;transition:background 0.2s;}
.send-btn:hover{background:var(--green2);}
.tx-verify{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px;display:none;}
.tx-verify.show{display:block;}
.tx-row{font-size:0.85em;display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border);}
.tx-row:last-child{border-bottom:none;}
.tx-item{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border);}
.tx-item:last-child{border-bottom:none;}
.tx-icon{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1em;flex-shrink:0;}
.tx-icon.in{background:rgba(0,255,136,0.15);color:var(--green);}
.tx-icon.out{background:rgba(248,81,73,0.15);color:var(--red);}
.tx-info{flex:1;}
.tx-addr{font-size:0.8em;color:var(--text2);font-family:monospace;}
.tx-time{font-size:0.75em;color:var(--text2);}
.tx-hash-small{font-size:0.7em;color:var(--text2);font-family:monospace;}
.tx-amount{font-weight:700;font-size:0.95em;}
.tx-amount.in{color:var(--green);}
.tx-amount.out{color:var(--red);}
.tx-status{font-size:0.7em;padding:2px 8px;border-radius:10px;background:rgba(0,255,136,0.15);color:var(--green);border:1px solid var(--green);}
.ref-code{font-size:1.5em;font-weight:700;color:var(--green);font-family:monospace;letter-spacing:3px;}
.stake-bar{background:var(--bg);border-radius:4px;height:8px;margin-top:8px;overflow:hidden;}
.stake-fill{background:var(--green);height:100%;border-radius:4px;transition:width 0.5s;}
.profile-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.profile-item{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:12px;}
.profile-item .pi-label{font-size:0.75em;color:var(--text2);margin-bottom:4px;}
.profile-item .pi-value{font-size:0.9em;font-weight:600;color:var(--text);}
.otp-input{font-size:2em;text-align:center;letter-spacing:12px;font-family:monospace;font-weight:700;}
.footer{background:var(--bg2);border-top:1px solid var(--border);padding:32px 24px;text-align:center;color:var(--text2);font-size:0.85em;margin-top:40px;}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;max-width:800px;margin:0 auto 24px;}
.footer-col h4{color:var(--text);margin-bottom:10px;font-size:0.9em;}
.footer-col a{display:block;color:var(--text2);font-size:0.85em;margin-bottom:6px;}
.footer-col a:hover{color:var(--green);}
.pos-badge{background:rgba(163,113,247,0.15);border:1px solid var(--purple);color:var(--purple);padding:3px 10px;border-radius:20px;font-size:0.75em;font-weight:600;}
@media(max-width:600px){.hero h1{font-size:1.8em;}.stats-grid{grid-template-columns:repeat(2,1fr);}.profile-grid{grid-template-columns:1fr;}.block-row{grid-template-columns:60px 1fr;}.block-row .hash-text,.block-row .validator{display:none;}}
</style>
<script>
function toggleTheme(){document.body.classList.toggle('light');localStorage.setItem('nyn_theme',document.body.classList.contains('light')?'light':'dark');}
function togglePwd(id){var i=document.getElementById(id);i.type=i.type==='password'?'text':'password';}
window.onload=function(){if(localStorage.getItem('nyn_theme')==='light')document.body.classList.add('light');}
</script>
"""

NAVBAR_LOGGED_IN = """
<nav class="navbar">
  <a href="/" class="navbar-brand" style="text-decoration:none;">⚡ NYN <span>NoyanCoin</span></a>
  <div class="navbar-links">
    <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    <a href="/" class="nav-btn">Explorer</a>
    <a href="/wallet" class="nav-btn">My Wallet</a>
    <a href="/profile" class="nav-btn">Profile</a>
    <a href="/logout" class="nav-btn danger">Logout</a>
  </div>
</nav>
"""

NAVBAR_GUEST = """
<nav class="navbar">
  <a href="/" class="navbar-brand" style="text-decoration:none;">⚡ NYN <span>NoyanCoin Explorer</span></a>
  <div class="navbar-links">
    <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    <a href="/login" class="nav-btn">Login</a>
    <a href="/register" class="nav-btn primary">Get Wallet</a>
  </div>
</nav>
"""

MAIN_HTML = """<!DOCTYPE html><html><head><title>NYN Explorer - NoyanCoin Blockchain</title>""" + STYLES + """</head><body>
{{ navbar | safe }}
<div class="hero">
  <div class="container">
    <h1>⚡ <span>NYN</span> Blockchain Explorer</h1>
    <p>Republic of Nowhere — Private. Human. Borderless. Powered by Proof of Stake.</p>
    {% if not logged_in %}
    <div class="hero-btns">
      <a href="/register" class="hero-btn primary">Create Free Wallet — Get 50 NYN</a>
      <a href="#blocks" class="hero-btn secondary">Explore Blockchain</a>
    </div>
    {% endif %}
  </div>
</div>
<div class="container">
  <div class="stats-grid">
    <div class="stat-card"><div class="val">{{ blocks }}</div><div class="lbl">Total Blocks</div></div>
    <div class="stat-card"><div class="val">24M</div><div class="lbl">Max Supply (NYN)</div></div>
    <div class="stat-card"><div class="val">{{ circulating }}</div><div class="lbl">Circulating Supply</div></div>
    <div class="stat-card"><div class="val">{{ users }}</div><div class="lbl">Total Wallets</div></div>
    <div class="stat-card"><div class="val">{{ txns }}</div><div class="lbl">Transactions</div></div>
    <div class="stat-card"><div class="val">~2s</div><div class="lbl">Block Time</div></div>
  </div>

  <div class="section-card">
    <div class="section-title">📊 Market Info</div>
    <div class="market-grid">
      <div class="market-card"><div class="m-label">Algorithm</div><div class="m-value">Proof of Stake</div></div>
      <div class="market-card"><div class="m-label">Max Supply</div><div class="m-value">24,000,000 NYN</div></div>
      <div class="market-card"><div class="m-label">Genesis Block</div><div class="m-value">{{ genesis_date }}</div></div>
      <div class="market-card"><div class="m-label">Consensus</div><div class="m-value green">PoS Active</div></div>
      <div class="market-card"><div class="m-label">Privacy</div><div class="m-value green">Balance Hidden</div></div>
      <div class="market-card"><div class="m-label">Human Verified</div><div class="m-value green">Required</div></div>
      <div class="market-card"><div class="m-label">Network</div><div class="m-value orange">Testnet</div></div>
      <div class="market-card"><div class="m-label">Ticker</div><div class="m-value">NYN</div></div>
    </div>
  </div>

  <div class="section-card">
    <div class="section-title">🔲 Block Visualization</div>
    <div class="blocks-visual">
      {% for block in chain %}
      {% set colors = ['#a371f7','#58a6ff','#00ff88','#f0883e','#e3b341','#f85149'] %}
      {% set color = colors[block.index % 6] %}
      <div class="block-vis" style="background:{{ color }}22;border:1px solid {{ color }};" onclick="window.location.href='#block-{{ block.index }}'">
        <span style="color:{{ color }};font-size:1em;">⬡</span>
        <span class="bn" style="color:{{ color }};">#{{ block.index }}</span>
        <span class="bt">{{ block.tx_count }} tx</span>
      </div>
      {% endfor %}
    </div>
  </div>

  <div class="section-card" id="blocks">
    <div class="section-title">📦 Latest Blocks</div>
    <div class="search-bar">
      <input type="text" id="si" placeholder="Search by block hash or wallet address...">
      <button onclick="window.location.href='/search?q='+document.getElementById('si').value">Search</button>
    </div>
    {% for block in chain|reverse %}
    <div class="block-row" id="block-{{ block.index }}">
      <div><span class="block-num-badge">#{{ block.index }}</span></div>
      <div>
        <div class="hash-text">🔗 {{ block.hash }}</div>
        <div style="font-size:0.75em;color:var(--text2);margin-top:2px;">◀ {{ block.previous_hash[:32] }}...</div>
      </div>
      <div class="hash-text" style="color:var(--text2);">{{ block.transactions[:60] }}...</div>
      <div style="font-size:0.8em;color:var(--text2);">
        <div>🔏 {{ block.validator[:16] if block.validator else 'System' }}</div>
        <div style="margin-top:2px;">{{ block.tx_count }} tx</div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
<div class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col"><h4>NYN NoyanCoin</h4><a href="/">Explorer</a><a href="/register">Create Wallet</a><a href="/login">Login</a></div>
      <div class="footer-col"><h4>Network</h4><a href="#">Whitepaper</a><a href="#">GitHub</a><a href="#">@OfficiaNowhere</a></div>
      <div class="footer-col"><h4>Info</h4><a href="#">About NYN</a><a href="#">Privacy Policy</a><a href="#">Security</a></div>
    </div>
    <p>⚡ NYN NoyanCoin — Republic of Nowhere — Currency of Everywhere</p>
    <p style="margin-top:6px;">Balance privacy enabled • Human verified network • Proof of Stake consensus</p>
  </div>
</div>
</body></html>
"""

REGISTER_HTML = """<!DOCTYPE html><html><head><title>Create Wallet - NYN</title>""" + STYLES + """
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head><body>
""" + NAVBAR_GUEST + """
<div class="form-page">
<div class="form-card">
  <h2>Create Your Wallet</h2>
  <p class="sub">Join the Republic of Nowhere</p>
  <div class="bonus-badge">🎁 Get 50 NYN free • Earn 20 NYN per referral (max 3)</div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Username</label><input type="text" name="username" placeholder="Choose a username" required maxlength="30" autocomplete="off"></div>
    <div class="fg"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div class="fg"><label>Password</label>
      <div class="input-wrap">
        <input type="password" name="password" id="pwd1" placeholder="Min 8 characters" required minlength="8">
        <button type="button" class="eye-btn" onclick="togglePwd('pwd1')">👁</button>
      </div>
    </div>
    <div class="fg"><label>Confirm Password</label>
      <div class="input-wrap">
        <input type="password" name="confirm" id="pwd2" placeholder="Repeat password" required>
        <button type="button" class="eye-btn" onclick="togglePwd('pwd2')">👁</button>
      </div>
    </div>
    <div class="fg"><label>Referral Code (optional)</label><input type="text" name="referral" placeholder="Enter referral code for bonus NYN"></div>
    <div class="recaptcha-wrap"><div class="g-recaptcha" data-sitekey="{{ site_key }}"></div></div>
    <button type="submit" class="btn-full">Create Wallet & Get 50 NYN ⚡</button>
  </form>
  <div class="form-footer">Already have a wallet? <a href="/login">Login here</a></div>
</div>
</div>
</body></html>
"""

LOGIN_HTML = """<!DOCTYPE html><html><head><title>Login - NYN</title>""" + STYLES + """</head><body>
""" + NAVBAR_GUEST + """
<div class="form-page">
<div class="form-card">
  <h2>Welcome Back</h2>
  <p class="sub">Login to your NYN wallet</p>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Username</label><input type="text" name="username" placeholder="Your username" required autocomplete="username"></div>
    <div class="fg"><label>Password</label>
      <div class="input-wrap">
        <input type="password" name="password" id="lpwd" placeholder="Your password" required autocomplete="current-password">
        <button type="button" class="eye-btn" onclick="togglePwd('lpwd')">👁</button>
      </div>
    </div>
    <button type="submit" class="btn-full">Login ⚡</button>
  </form>
  <div class="form-footer">No wallet yet? <a href="/register">Create one free</a></div>
</div>
</div>
</body></html>
"""

VERIFY_HTML = """<!DOCTYPE html><html><head><title>Verify Email - NYN</title>""" + STYLES + """</head><body>
<nav class="navbar">
  <a href="/" class="navbar-brand" style="text-decoration:none;">⚡ NYN <span>NoyanCoin</span></a>
  <div class="navbar-links"><button class="theme-btn" onclick="toggleTheme()">🌙</button></div>
</nav>
<div class="form-page">
<div class="form-card">
  <h2>Verify Your Email</h2>
  <p class="sub">Enter the 6-digit code sent to your email</p>
  <div class="alert info">📧 Check your inbox — code expires in 10 minutes</div>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg">
      <label>Verification Code</label>
      <input type="text" name="otp" class="otp-input" placeholder="000000" maxlength="6" required autocomplete="off" autofocus>
    </div>
    <button type="submit" class="btn-full">Verify & Activate Wallet ⚡</button>
  </form>
  <div class="form-footer"><a href="/resend-otp">Resend verification code</a></div>
</div>
</div>
</body></html>
"""

WALLET_HTML = """<!DOCTYPE html><html><head><title>My Wallet - NYN</title>""" + STYLES + """
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head><body>
""" + NAVBAR_LOGGED_IN + """
<div class="wallet-page">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}

  <div class="wallet-header">
    <div class="wallet-user">
      <div class="avatar">{{ username[0].upper() }}</div>
      <div>
        <div class="wname">{{ username }} <span class="badge {{ 'v' if is_verified else 'u' }}">{{ '✓ Verified' if is_verified else '✗ Unverified' }}</span> <span class="pos-badge">PoS Node</span></div>
        <div style="font-size:0.85em;color:var(--text2);">Member since {{ created_at }}</div>
      </div>
    </div>

    <div class="balance-box">
      <div class="bal-label">Your Balance (Private)</div>
      <div id="bal-display" class="bal-dots">••••••</div>
      <div><button class="show-btn" onclick="toggleBal()">👁 Show / Hide Balance</button></div>
      <div class="privacy-note">🔒 Your balance is private. Only you can see it. This is NYN's core privacy feature.</div>
    </div>

    <div style="margin-top:16px;">
      <div style="font-size:0.85em;color:var(--text2);margin-bottom:6px;">Your NYN Wallet Address</div>
      <div class="addr-box" id="waddr">{{ wallet_address }}</div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ wallet_address }}');this.textContent='✓ Copied!'">📋 Copy Address</button>
    </div>
    <div class="qr-wrap"><div id="qrcode"></div></div>
  </div>

  {% if not is_verified %}
  <div class="wsection" style="border-color:var(--red);">
    <h3>⚠️ Email Not Verified</h3>
    <p style="color:var(--text2);font-size:0.9em;margin-bottom:12px;">Verify your email to unlock sending NYN and all features.</p>
    <a href="/verify" style="display:block;text-align:center;padding:10px;background:var(--red);color:#fff;border-radius:8px;font-weight:600;text-decoration:none;">Verify Email Now</a>
  </div>
  {% endif %}

  <div class="wsection">
    <h3>💸 Send NYN</h3>
    <div class="alert info" style="margin-bottom:12px;">🔐 Every transaction is verified by PoS consensus before confirmation</div>
    <input type="text" class="send-input" id="recv-addr" placeholder="Receiver NYN wallet address (NYN...)" oninput="previewTx()">
    <input type="number" class="send-input" id="send-amt" placeholder="Amount in NYN (max 10,000 per tx)" step="0.01" min="0.01" max="10000" oninput="previewTx()">

    <div class="tx-verify" id="tx-preview">
      <div style="font-size:0.85em;font-weight:600;color:var(--text);margin-bottom:8px;">📋 Transaction Preview</div>
      <div class="tx-row"><span style="color:var(--text2);">From</span><span style="font-family:monospace;font-size:0.8em;">{{ wallet_address[:24] }}...</span></div>
      <div class="tx-row"><span style="color:var(--text2);">To</span><span id="prev-to" style="font-family:monospace;font-size:0.8em;">-</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Amount</span><span id="prev-amt" style="color:var(--green);font-weight:600;">-</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Network Fee</span><span style="color:var(--text2);">0 NYN (Free)</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Consensus</span><span class="pos-badge">Proof of Stake</span></div>
      <div class="tx-row" style="border:none;"><span style="color:var(--text2);">Status</span><span style="color:var(--green);">Ready to confirm</span></div>
    </div>

    <form method="POST" action="/send" id="send-form">
      <input type="hidden" name="receiver" id="recv-hidden">
      <input type="hidden" name="amount" id="amt-hidden">
      <button type="button" class="send-btn" onclick="confirmSend()">Preview & Send NYN ⚡</button>
    </form>
  </div>

  <div class="wsection">
    <h3>🎁 Referral Program</h3>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:12px;">Share your code and earn 20 NYN per referral (max 3 referrals)</p>
    <div class="ref-code">{{ referral_code }}</div>
    <button class="copy-btn" style="margin-top:10px;" onclick="navigator.clipboard.writeText('{{ referral_code }}');this.textContent='✓ Copied!'">📋 Copy Code</button>
    <div style="margin-top:12px;">
      <div style="font-size:0.85em;color:var(--text2);">Referrals: {{ referral_count }}/3</div>
      <div class="stake-bar"><div class="stake-fill" style="width:{{ (referral_count/3*100)|int }}%"></div></div>
    </div>
  </div>

  <div class="wsection">
    <h3>📋 Transaction History</h3>
    {% if transactions %}
    {% for tx in transactions %}
    <div class="tx-item">
      <div class="tx-icon {{ 'in' if tx.receiver == wallet_address else 'out' }}">{{ '↓' if tx.receiver == wallet_address else '↑' }}</div>
      <div class="tx-info">
        <div style="font-size:0.85em;font-weight:500;">{{ 'Received from' if tx.receiver == wallet_address else 'Sent to' }}</div>
        <div class="tx-addr">{{ tx.sender[:28] if tx.receiver == wallet_address else tx.receiver[:28] }}...</div>
        <div class="tx-time">{{ tx.time }} • <span class="tx-status">✓ Confirmed</span></div>
      </div>
      <div>
        <div class="tx-amount {{ 'in' if tx.receiver == wallet_address else 'out' }}">{{ '+' if tx.receiver == wallet_address else '-' }}{{ tx.amount }} NYN</div>
      </div>
    </div>
    {% endfor %}
    {% else %}
    <p style="color:var(--text2);font-size:0.9em;text-align:center;padding:20px 0;">No transactions yet. Send or receive NYN to see history here.</p>
    {% endif %}
  </div>
</div>

<div class="footer">
  <p>⚡ NYN NoyanCoin — Republic of Nowhere</p>
</div>

<script>
var balVis = false;
var realBal = "{{ balance }} NYN";
function toggleBal(){
  balVis = !balVis;
  var el = document.getElementById('bal-display');
  el.className = balVis ? 'bal-amount' : 'bal-dots';
  el.textContent = balVis ? realBal : '••••••';
}
function previewTx(){
  var addr = document.getElementById('recv-addr').value;
  var amt = document.getElementById('send-amt').value;
  var preview = document.getElementById('tx-preview');
  if(addr.length > 5 && amt > 0){
    document.getElementById('prev-to').textContent = addr.substring(0,24)+'...';
    document.getElementById('prev-amt').textContent = amt + ' NYN';
    preview.classList.add('show');
  } else {
    preview.classList.remove('show');
  }
}
function confirmSend(){
  var addr = document.getElementById('recv-addr').value;
  var amt = document.getElementById('send-amt').value;
  if(!addr || !amt){ alert('Please fill in receiver address and amount'); return; }
  if(!addr.startsWith('NYN')){ alert('Invalid NYN address. Must start with NYN'); return; }
  if(parseFloat(amt) > 10000){ alert('Maximum 10,000 NYN per transaction'); return; }
  if(confirm('Confirm sending ' + amt + ' NYN to ' + addr.substring(0,20) + '...?')){
    document.getElementById('recv-hidden').value = addr;
    document.getElementById('amt-hidden').value = amt;
    document.getElementById('send-form').submit();
  }
}
new QRCode(document.getElementById("qrcode"),{text:"{{ wallet_address }}",width:128,height:128,colorDark:"#000000",colorLight:"#ffffff"});
</script>
</body></html>
"""

PROFILE_HTML = """<!DOCTYPE html><html><head><title>Profile - NYN</title>""" + STYLES + """</head><body>
""" + NAVBAR_LOGGED_IN + """
<div class="wallet-page">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}

  <div class="wsection">
    <h3>👤 Profile</h3>
    <div class="wallet-user" style="margin-bottom:20px;">
      <div class="avatar" style="width:64px;height:64px;font-size:1.8em;">{{ username[0].upper() }}</div>
      <div>
        <div class="wname">{{ username }} <span class="badge {{ 'v' if is_verified else 'u' }}">{{ '✓ Verified' if is_verified else '✗ Unverified' }}</span></div>
        <div style="color:var(--text2);font-size:0.85em;">{{ email }}</div>
        <div style="color:var(--text2);font-size:0.85em;">Member since {{ created_at }}</div>
      </div>
    </div>
    <div class="profile-grid">
      <div class="profile-item"><div class="pi-label">Total Sent</div><div class="pi-value" style="color:var(--red);">{{ total_sent }} NYN</div></div>
      <div class="profile-item"><div class="pi-label">Total Received</div><div class="pi-value" style="color:var(--green);">{{ total_received }} NYN</div></div>
      <div class="profile-item"><div class="pi-label">Referrals Made</div><div class="pi-value">{{ referral_count }}/3</div></div>
      <div class="profile-item"><div class="pi-label">Wallet Address</div><div class="pi-value" style="font-family:monospace;font-size:0.75em;color:var(--orange);">{{ wallet_address[:20] }}...</div></div>
      <div class="profile-item"><div class="pi-label">Network</div><div class="pi-value">NYN Testnet</div></div>
      <div class="profile-item"><div class="pi-label">Consensus</div><div class="pi-value" style="color:var(--purple);">Proof of Stake</div></div>
    </div>
  </div>

  <div class="wsection">
    <h3>🔒 Change Password</h3>
    <form method="POST" action="/change-password">
      <div class="fg"><label>Current Password</label>
        <div class="input-wrap">
          <input type="password" name="current_password" id="cp1" placeholder="Current password" required>
          <button type="button" class="eye-btn" onclick="togglePwd('cp1')">👁</button>
        </div>
      </div>
      <div class="fg"><label>New Password</label>
        <div class="input-wrap">
          <input type="password" name="new_password" id="cp2" placeholder="New password (min 8 chars)" required minlength="8">
          <button type="button" class="eye-btn" onclick="togglePwd('cp2')">👁</button>
        </div>
      </div>
      <div class="fg"><label>Confirm New Password</label>
        <div class="input-wrap">
          <input type="password" name="confirm_password" id="cp3" placeholder="Confirm new password" required>
          <button type="button" class="eye-btn" onclick="togglePwd('cp3')">👁</button>
        </div>
      </div>
      <button type="submit" class="btn-full">Update Password</button>
    </form>
  </div>

  <div class="wsection" style="border-color:var(--red);">
    <h3 style="color:var(--red);">⚠️ Danger Zone</h3>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:12px;">These actions are irreversible. Please be careful.</p>
    <button onclick="alert('Account deletion coming soon. Contact support.')" style="background:none;border:1px solid var(--red);color:var(--red);padding:8px 16px;border-radius:6px;cursor:pointer;font-size:0.875em;">Delete Account</button>
  </div>
</div>
<div class="footer"><p>⚡ NYN NoyanCoin — Republic of Nowhere</p></div>
</body></html>
"""

@app.route('/')
def explorer():
    s = Session()
    chain = get_chain()
    users = s.query(UserModel).count()
    txns = s.query(TransactionModel).count()
    circulating = get_circulating_supply()
    s.close()
    logged_in = 'user_id' in session
    navbar = NAVBAR_LOGGED_IN if logged_in else NAVBAR_GUEST
    genesis_date = datetime.datetime.fromtimestamp(get_chain()[0].timestamp).strftime('%Y-%m-%d') if chain else NYN_GENESIS_DATE
    return render_template_string(MAIN_HTML, chain=chain, blocks=len(chain), users=users, txns=txns, logged_in=logged_in, navbar=navbar, circulating=circulating, genesis_date=genesis_date)

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
        if len(password) < 8:
            return render_template_string(REGISTER_HTML, msg="Password must be at least 8 characters", msg_type="error", site_key=RECAPTCHA_SITE_KEY)
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
        add_block({"event": "new_wallet", "address": wallet_address[:20]+"...", "timestamp": time.time()}, "PoS-System")
        send_otp_email(email, otp, username)
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
            send_otp_email(user.email, otp, user.username)
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
    tx_list = [{"sender": t.sender, "receiver": t.receiver, "amount": t.amount, "time": datetime.datetime.fromtimestamp(t.timestamp).strftime('%b %d, %H:%M')} for t in txns]
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
    errors = verify_transaction(sender.wallet_address, receiver_addr, amount, sender.balance)
    if errors:
        s.close()
        return redirect(url_for('wallet') + '?msg=' + '+'.join(errors[0].split()) + '&msg_type=error')
    if not receiver:
        s.close()
        return redirect(url_for('wallet') + '?msg=Wallet+address+not+found&msg_type=error')
    sender.balance -= amount
    receiver.balance += amount
    sender.total_sent += amount
    receiver.total_received += amount
    tx_hash = hashlib.sha256(f"{sender.wallet_address}{receiver_addr}{amount}{time.time()}".encode()).hexdigest()
    validator = select_validator(s)
    tx = TransactionModel(sender=sender.wallet_address, receiver=receiver_addr, amount=amount, timestamp=time.time(), tx_hash=tx_hash, status="confirmed", block_index=len(get_chain()))
    s.add(tx)
    add_block({"tx": tx_hash[:20]+"...", "amount": amount, "from": sender.wallet_address[:16]+"...", "to": receiver_addr[:16]+"..."}, validator)
    s.commit()
    s.close()
    return redirect(url_for('wallet') + f'?msg=Successfully+sent+{amount}+NYN&msg_type=success')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    s.close()
    created = datetime.datetime.fromtimestamp(user.created_at).strftime('%b %d, %Y')
    msg = request.args.get('msg', None)
    msg_type = request.args.get('msg_type', 'success')
    return render_template_string(PROFILE_HTML, username=user.username, email=user.email or "Not set", wallet_address=user.wallet_address, is_verified=user.is_verified, referral_count=user.referral_count, total_sent=round(user.total_sent, 2), total_received=round(user.total_received, 2), created_at=created, msg=msg, msg_type=msg_type)

@app.route('/change-password', methods=['POST'])
@limiter.limit("5 per minute")
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    current = request.form.get('current_password', '')
    new_pwd = request.form.get('new_password', '')
    confirm = request.form.get('confirm_password', '')
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    if not bcrypt.check_password_hash(user.password, current):
        s.close()
        return redirect(url_for('profile') + '?msg=Current+password+is+incorrect&msg_type=error')
    if new_pwd != confirm:
        s.close()
        return redirect(url_for('profile') + '?msg=New+passwords+do+not+match&msg_type=error')
    if len(new_pwd) < 8:
        s.close()
        return redirect(url_for('profile') + '?msg=Password+must+be+at+least+8+characters&msg_type=error')
    user.password = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
    s.commit()
    s.close()
    return redirect(url_for('profile') + '?msg=Password+updated+successfully&msg_type=success')

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    s = Session()
    block = s.query(BlockModel).filter_by(hash=q).first()
    user = s.query(UserModel).filter_by(wallet_address=q).first()
    s.close()
    if block:
        return jsonify({"found": "block", "index": block.index, "hash": block.hash, "validator": block.validator})
    if user:
        return jsonify({"found": "wallet", "address": user.wallet_address, "balance": "🔒 Private - NYN Privacy", "verified": user.is_verified})
    return jsonify({"found": "nothing", "message": "No block or wallet found for this query"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('explorer'))

@app.route('/add/<secret>/<data>')
@limiter.limit("5 per minute")
def add(secret, data):
    if secret != NYN_SECRET:
        return jsonify({"error": "Unauthorized"}), 403
    add_block({"data": data, "timestamp": time.time()}, "Founder")
    return jsonify({"message": "Block added!", "blocks": len(get_chain())})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)