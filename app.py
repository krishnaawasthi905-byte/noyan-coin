from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
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
import datetime
import requests
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
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")
NYN_SECRET = os.environ.get("NYN_SECRET", "fallback")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")

NYN_MAX_SUPPLY = 24000000
STAKE_REWARD = 0.1
MIN_STAKE = 10.0

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
    blocks_validated = Column(Integer, default=0)
    theme = Column(String(10), default="dark")
    language = Column(String(10), default="en")
    notif_tx = Column(Boolean, default=True)
    notif_security = Column(Boolean, default=True)
    privacy_hide_balance = Column(Boolean, default=True)
    privacy_hide_txs = Column(Boolean, default=False)

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

class StakeModel(Base):
    __tablename__ = 'stakes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    wallet_address = Column(String(100))
    amount = Column(Float)
    staked_at = Column(Float)
    is_active = Column(Boolean, default=True)
    rewards_earned = Column(Float, default=0.0)

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
        errors.append("Invalid NYN address format - must start with NYN")
    if amount <= 0:
        errors.append("Amount must be greater than 0")
    if sender_balance < amount:
        errors.append(f"Insufficient balance. You have {round(sender_balance, 2)} NYN")
    if sender_address == receiver_address:
        errors.append("Cannot send NYN to yourself")
    if amount > 10000:
        errors.append("Maximum 10,000 NYN per single transaction")
    return errors

def select_validator(session_db):
    validators = session_db.query(UserModel).filter(
        UserModel.staked_amount >= MIN_STAKE,
        UserModel.is_verified == True
    ).order_by(UserModel.staked_amount.desc()).all()
    if validators:
        weights = [v.staked_amount for v in validators]
        total = sum(weights)
        probs = [w/total for w in weights]
        chosen = random.choices(validators, weights=probs, k=1)[0]
        chosen.balance += STAKE_REWARD
        chosen.blocks_validated += 1
        session_db.commit()
        return chosen.wallet_address[:20] + "..."
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
    block = BlockModel(
        index=index,
        timestamp=timestamp,
        transactions=json.dumps(transactions),
        previous_hash=previous_hash,
        hash=h,
        validator=validator,
        tx_count=1 if isinstance(transactions, dict) else 0
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
        from sendgrid.helpers.mail import Mail
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        html = f"""
        <div style="background:#0d1117;padding:40px;font-family:monospace;max-width:500px;margin:0 auto;border-radius:12px;border:1px solid #30363d;">
            <h1 style="color:#00ff88;text-align:center;margin-bottom:4px;">⚡ NYN NoyanCoin</h1>
            <p style="color:#8b949e;text-align:center;margin-bottom:24px;">Republic of Nowhere</p>
            <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;text-align:center;margin:16px 0;">
                <p style="color:#8b949e;margin-bottom:12px;">Hi {username}, your verification code is:</p>
                <h2 style="color:#00ff88;font-size:2.5em;letter-spacing:12px;margin:0;">{otp}</h2>
                <p style="color:#8b949e;font-size:0.85em;margin-top:12px;">Expires in 10 minutes</p>
            </div>
            <p style="color:#8b949e;text-align:center;font-size:0.8em;">If you did not request this, ignore this email.</p>
            <p style="color:#8b949e;text-align:center;font-size:0.8em;margin-top:8px;">Republic of Nowhere — Currency of Everywhere</p>
        </div>
        """
        message = Mail(from_email=EMAIL_USER, to_emails=email, subject='⚡ NYN Wallet — Verification Code', html_content=html)
        sg.send(message)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def verify_recaptcha(token):
    if not RECAPTCHA_SECRET_KEY:
        return True
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': RECAPTCHA_SECRET_KEY, 'response': token})
        return r.json().get('success', False)
    except:
        return True

def get_circulating_supply():
    s = Session()
    total = s.query(UserModel).count() * 50
    s.close()
    return min(total, NYN_MAX_SUPPLY)

def get_total_staked():
    s = Session()
    users = s.query(UserModel).all()
    total = sum(u.staked_amount for u in users)
    s.close()
    return round(total, 2)

s = Session()
if s.query(BlockModel).count() == 0:
    add_block("NYN Genesis Block - Republic of Nowhere", "Founder")
    add_block({"from": "Founder", "to": "Republic of Nowhere", "amount": 24000000}, "Founder")
s.close()

from templates import *

@app.route('/')
def explorer():
    s = Session()
    chain = get_chain()
    users = s.query(UserModel).count()
    txns = s.query(TransactionModel).count()
    s.close()
    circulating = get_circulating_supply()
    total_staked = get_total_staked()
    logged_in = 'user_id' in session
    genesis_date = datetime.datetime.fromtimestamp(chain[0].timestamp).strftime('%Y-%m-%d') if chain else "2026-04-30"
    return render_template_string(MAIN_HTML, chain=chain, blocks=len(chain), users=users, txns=txns, logged_in=logged_in, circulating=circulating, total_staked=total_staked, genesis_date=genesis_date)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        if not verify_recaptcha(request.form.get('g-recaptcha-response', '')):
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
        return render_template_string(VERIFY_HTML, msg="Invalid or expired code")
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
    stake = s.query(StakeModel).filter_by(user_id=user.id, is_active=True).first()
    s.close()
    tx_list = [{"sender": t.sender, "receiver": t.receiver, "amount": t.amount, "time": datetime.datetime.fromtimestamp(t.timestamp).strftime('%b %d, %H:%M'), "type": "in" if t.receiver == user.wallet_address else "out"} for t in txns]
    created = datetime.datetime.fromtimestamp(user.created_at).strftime('%b %d, %Y')
    msg = request.args.get('msg', None)
    msg_type = request.args.get('msg_type', 'success')
    stake_info = {"amount": stake.amount, "rewards": round(stake.rewards_earned, 4)} if stake else None
    return render_template_string(WALLET_HTML, user=user, transactions=tx_list, created_at=created, msg=msg, msg_type=msg_type, stake_info=stake_info, min_stake=MIN_STAKE)

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
    errors = verify_transaction(sender.wallet_address, receiver_addr, amount, sender.balance)
    if errors:
        s.close()
        return redirect(url_for('wallet') + '?msg=' + requests.utils.quote(errors[0]) + '&msg_type=error')
    receiver = s.query(UserModel).filter_by(wallet_address=receiver_addr).first()
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
    s.commit()
    add_block({"tx": tx_hash[:20]+"...", "amount": amount, "from": sender.wallet_address[:16]+"...", "to": receiver_addr[:16]+"..."}, validator)
    s.close()
    return redirect(url_for('wallet') + f'?msg=Successfully+sent+{amount}+NYN&msg_type=success')

@app.route('/stake', methods=['POST'])
@limiter.limit("5 per minute")
def stake_nyn():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        amount = float(request.form.get('amount', 0))
    except:
        return redirect(url_for('wallet') + '?msg=Invalid+stake+amount&msg_type=error')
    if amount < MIN_STAKE:
        return redirect(url_for('wallet') + f'?msg=Minimum+stake+is+{MIN_STAKE}+NYN&msg_type=error')
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    if user.balance < amount:
        s.close()
        return redirect(url_for('wallet') + '?msg=Insufficient+balance+to+stake&msg_type=error')
    existing_stake = s.query(StakeModel).filter_by(user_id=user.id, is_active=True).first()
    if existing_stake:
        s.close()
        return redirect(url_for('wallet') + '?msg=You+already+have+an+active+stake&msg_type=error')
    user.balance -= amount
    user.staked_amount += amount
    stake = StakeModel(user_id=user.id, wallet_address=user.wallet_address, amount=amount, staked_at=time.time())
    s.add(stake)
    s.commit()
    add_block({"event": "stake", "validator": user.wallet_address[:20]+"...", "amount": amount}, "PoS-System")
    s.close()
    return redirect(url_for('wallet') + f'?msg=Successfully+staked+{amount}+NYN&msg_type=success')

@app.route('/unstake', methods=['POST'])
def unstake_nyn():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    stake = s.query(StakeModel).filter_by(user_id=user.id, is_active=True).first()
    if not stake:
        s.close()
        return redirect(url_for('wallet') + '?msg=No+active+stake+found&msg_type=error')
    user.balance += stake.amount
    user.staked_amount -= stake.amount
    stake.is_active = False
    s.commit()
    s.close()
    return redirect(url_for('wallet') + '?msg=Successfully+unstaked+NYN&msg_type=success')

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
    return render_template_string(PROFILE_HTML, user=user, created_at=created, msg=msg, msg_type=msg_type)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'theme':
            user.theme = request.form.get('theme', 'dark')
        elif action == 'language':
            user.language = request.form.get('language', 'en')
        elif action == 'notifications':
            user.notif_tx = 'notif_tx' in request.form
            user.notif_security = 'notif_security' in request.form
        elif action == 'privacy':
            user.privacy_hide_balance = 'privacy_hide_balance' in request.form
            user.privacy_hide_txs = 'privacy_hide_txs' in request.form
        s.commit()
        s.close()
        return redirect(url_for('settings') + '?msg=Settings+saved&msg_type=success')
    s.close()
    msg = request.args.get('msg', None)
    msg_type = request.args.get('msg_type', 'success')
    return render_template_string(SETTINGS_HTML, user=user, msg=msg, msg_type=msg_type)

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
        return redirect(url_for('settings') + '?msg=Current+password+incorrect&msg_type=error')
    if new_pwd != confirm:
        s.close()
        return redirect(url_for('settings') + '?msg=Passwords+do+not+match&msg_type=error')
    if len(new_pwd) < 8:
        s.close()
        return redirect(url_for('settings') + '?msg=Password+must+be+8+characters&msg_type=error')
    user.password = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
    s.commit()
    s.close()
    return redirect(url_for('settings') + '?msg=Password+updated&msg_type=success')

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
        return jsonify({"found": "wallet", "address": user.wallet_address, "balance": "🔒 Private", "verified": user.is_verified})
    return jsonify({"found": "nothing"})

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