from flask import Flask, jsonify, render_template_string, request, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
import hashlib
import json
import time
import os
import ecdsa
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "nyn-secret-2026")
bcrypt = Bcrypt(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "20 per minute"])

database_url = os.environ.get("DATABASE_URL", "sqlite:///nyn.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(database_url)
Base = declarative_base()

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
    password = Column(String(200), nullable=False)
    wallet_address = Column(String(100), unique=True)
    public_key = Column(Text)
    created_at = Column(Float)
    is_verified = Column(Boolean, default=False)

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

s = Session()
if s.query(BlockModel).count() == 0:
    add_block("NYN Genesis Block - Republic of Nowhere")
    add_block({"from": "Founder", "to": "Republic of Nowhere", "amount": 24000000})
s.close()

NYN_SECRET = os.environ.get("NYN_SECRET", "fallback")

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
.nav { display: flex; justify-content: center; gap: 15px; margin-bottom: 25px; }
.nav a { color: #00ff88; text-decoration: none; border: 1px solid #00ff88; padding: 8px 20px; border-radius: 5px; }
.nav a:hover { background: #00ff88; color: #000; }
.stats { display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
.stat { text-align: center; background: #111; padding: 15px 25px; border-radius: 8px; border: 1px solid #333; }
.stat h2 { color: #00ff88; margin: 0; }
.stat p { color: #888; margin: 5px 0 0 0; }
.block { background: #111; border: 1px solid #00ff88; margin: 10px 0; padding: 15px; border-radius: 8px; }
.block h2 { color: #00ff88; margin: 0 0 10px 0; }
.hash { color: #ff8800; word-break: break-all; }
.data { color: #fff; }
.form-box { max-width: 400px; margin: 30px auto; background: #111; padding: 30px; border-radius: 10px; border: 1px solid #00ff88; }
.form-box h2 { color: #00ff88; margin-bottom: 20px; text-align: center; }
.form-box input { width: 100%; padding: 12px; margin: 8px 0; background: #000; border: 1px solid #333; color: #00ff88; border-radius: 5px; font-family: monospace; }
.form-box button { width: 100%; padding: 12px; margin-top: 15px; background: #00ff88; color: #000; border: none; border-radius: 5px; font-family: monospace; font-size: 1em; cursor: pointer; font-weight: bold; }
.form-box button:hover { background: #00cc66; }
.wallet-box { max-width: 600px; margin: 30px auto; background: #111; padding: 30px; border-radius: 10px; border: 1px solid #00ff88; }
.wallet-box h2 { color: #00ff88; margin-bottom: 20px; }
.address { background: #000; padding: 15px; border-radius: 5px; word-break: break-all; color: #ff8800; margin: 10px 0; }
.msg { text-align: center; padding: 10px; margin: 10px 0; border-radius: 5px; }
.msg.error { background: #ff000022; border: 1px solid #ff0000; color: #ff4444; }
.msg.success { background: #00ff8822; border: 1px solid #00ff88; color: #00ff88; }
.logout { color: #ff4444; text-decoration: none; border: 1px solid #ff4444; padding: 8px 20px; border-radius: 5px; }
.logout:hover { background: #ff4444; color: #fff; }
</style>
</head>
<body>
<h1>⚡ NYN Explorer</h1>
<h3>Republic of Nowhere — NoyanCoin Blockchain</h3>
<div class="nav">
  <a href="/">Explorer</a>
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
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}.form-box{max-width:400px;margin:50px auto;background:#111;padding:30px;border-radius:10px;border:1px solid #00ff88;}.form-box h2{color:#00ff88;margin-bottom:20px;text-align:center;}.form-box input{width:100%;padding:12px;margin:8px 0;background:#000;border:1px solid #333;color:#00ff88;border-radius:5px;font-family:monospace;}.form-box button{width:100%;padding:12px;margin-top:15px;background:#00ff88;color:#000;border:none;border-radius:5px;font-family:monospace;font-size:1em;cursor:pointer;font-weight:bold;}.msg{text-align:center;padding:10px;margin:10px 0;border-radius:5px;}.msg.error{background:#ff000022;border:1px solid #ff0000;color:#ff4444;}.msg.success{background:#00ff8822;border:1px solid #00ff88;color:#00ff88;}a{color:#00ff88;}</style></head>
<body><div class="form-box">
<h2>⚡ Create NYN Wallet</h2>
{% if msg %}<div class="msg {{ msg_type }}">{{ msg }}</div>{% endif %}
<form method="POST">
<input type="text" name="username" placeholder="Username" required maxlength="30">
<input type="password" name="password" placeholder="Password (min 8 chars)" required minlength="8">
<input type="password" name="confirm" placeholder="Confirm Password" required>
<button type="submit">Create Wallet</button>
</form>
<p style="text-align:center;margin-top:15px;">Already have a wallet? <a href="/login">Login</a></p>
</div></body></html>
"""

LOGIN_HTML = """
<!DOCTYPE html><html><head><title>Login - NYN</title>
<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}.form-box{max-width:400px;margin:50px auto;background:#111;padding:30px;border-radius:10px;border:1px solid #00ff88;}.form-box h2{color:#00ff88;margin-bottom:20px;text-align:center;}.form-box input{width:100%;padding:12px;margin:8px 0;background:#000;border:1px solid #333;color:#00ff88;border-radius:5px;font-family:monospace;}.form-box button{width:100%;padding:12px;margin-top:15px;background:#00ff88;color:#000;border:none;border-radius:5px;font-family:monospace;font-size:1em;cursor:pointer;font-weight:bold;}.msg{text-align:center;padding:10px;margin:10px 0;border-radius:5px;}.msg.error{background:#ff000022;border:1px solid #ff0000;color:#ff4444;}a{color:#00ff88;}</style></head>
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
<style>* {box-sizing:border-box;margin:0;padding:0;}body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}.wallet-box{max-width:600px;margin:30px auto;background:#111;padding:30px;border-radius:10px;border:1px solid #00ff88;}.wallet-box h2{color:#00ff88;margin-bottom:20px;}.address{background:#000;padding:15px;border-radius:5px;word-break:break-all;color:#ff8800;margin:10px 0;}.nav{display:flex;justify-content:center;gap:15px;margin-bottom:25px;}.nav a{color:#00ff88;text-decoration:none;border:1px solid #00ff88;padding:8px 20px;border-radius:5px;}.logout{color:#ff4444!important;border-color:#ff4444!important;}h1{text-align:center;font-size:2em;margin-bottom:5px;}h3{color:#888;text-align:center;margin-bottom:20px;}.badge{display:inline-block;padding:5px 15px;border-radius:20px;font-size:0.8em;margin-left:10px;}.verified{background:#00ff8822;border:1px solid #00ff88;color:#00ff88;}.unverified{background:#ff000022;border:1px solid #ff4444;color:#ff4444;}</style></head>
<body>
<h1>⚡ NYN Explorer</h1>
<h3>Republic of Nowhere — NoyanCoin Blockchain</h3>
<div class="nav">
<a href="/">Explorer</a>
<a href="/wallet">My Wallet</a>
<a href="/logout" class="logout">Logout</a>
</div>
<div class="wallet-box">
<h2>👤 {{ username }} <span class="badge unverified">Unverified</span></h2>
<p style="color:#888;margin-bottom:15px;">Your NYN Wallet Address:</p>
<div class="address">{{ wallet_address }}</div>
<p style="color:#888;margin-top:20px;font-size:0.85em;">⚠️ Save this address. It is your unique NYN identity.</p>
<p style="color:#888;margin-top:10px;font-size:0.85em;">Balance: Coming soon</p>
<p style="color:#888;margin-top:5px;font-size:0.85em;">Human Verification: Coming soon</p>
</div>
</body></html>
"""

@app.route('/')
def explorer():
    s = Session()
    chain = get_chain()
    users = s.query(UserModel).count()
    s.close()
    logged_in = 'user_id' in session
    return render_template_string(HTML, chain=chain, blocks=len(chain), users=users, logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        if len(username) < 3:
            return render_template_string(REGISTER_HTML, msg="Username must be at least 3 characters", msg_type="error")
        if password != confirm:
            return render_template_string(REGISTER_HTML, msg="Passwords don't match", msg_type="error")
        if len(password) < 8:
            return render_template_string(REGISTER_HTML, msg="Password must be at least 8 characters", msg_type="error")
        s = Session()
        existing = s.query(UserModel).filter_by(username=username).first()
        if existing:
            s.close()
            return render_template_string(REGISTER_HTML, msg="Username already taken", msg_type="error")
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        wallet_address, public_key = generate_wallet()
        user = UserModel(username=username, password=hashed, wallet_address=wallet_address, public_key=public_key, created_at=time.time())
        s.add(user)
        s.commit()
        add_block({"event": "new_wallet", "address": wallet_address, "timestamp": time.time()})
        s.close()
        return render_template_string(REGISTER_HTML, msg="Wallet created! Please login.", msg_type="success")
    return render_template_string(REGISTER_HTML, msg=None, msg_type=None)

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
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('wallet'))
        return render_template_string(LOGIN_HTML, msg="Invalid username or password")
    return render_template_string(LOGIN_HTML, msg=None)

@app.route('/wallet')
def wallet():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    s = Session()
    user = s.query(UserModel).filter_by(id=session['user_id']).first()
    s.close()
    return render_template_string(WALLET_HTML, username=user.username, wallet_address=user.wallet_address)

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