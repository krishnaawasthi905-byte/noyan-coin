import hashlib
import hmac
import base64
import os
import time
import struct
import re
import pyotp
from flask import request, session
from sqlalchemy.orm import sessionmaker

FAILED_ATTEMPTS = {}
BLOCKED_IPS = {}
TX_COOLDOWNS = {}
MAX_ATTEMPTS = 5
BLOCK_TIME = 1800
TX_COOLDOWN = 30
DAILY_TX_LIMIT = 50000.0

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def is_ip_blocked(ip):
    if ip in BLOCKED_IPS:
        if time.time() - BLOCKED_IPS[ip] < BLOCK_TIME:
            return True
        else:
            del BLOCKED_IPS[ip]
            if ip in FAILED_ATTEMPTS:
                del FAILED_ATTEMPTS[ip]
    return False

def record_failed_attempt(ip):
    if ip not in FAILED_ATTEMPTS:
        FAILED_ATTEMPTS[ip] = []
    FAILED_ATTEMPTS[ip].append(time.time())
    recent = [t for t in FAILED_ATTEMPTS[ip] if time.time() - t < 600]
    FAILED_ATTEMPTS[ip] = recent
    if len(recent) >= MAX_ATTEMPTS:
        BLOCKED_IPS[ip] = time.time()
        return True
    return False

def clear_attempts(ip):
    if ip in FAILED_ATTEMPTS:
        del FAILED_ATTEMPTS[ip]

def get_attempts_remaining(ip):
    if ip not in FAILED_ATTEMPTS:
        return MAX_ATTEMPTS
    recent = [t for t in FAILED_ATTEMPTS[ip] if time.time() - t < 600]
    return max(0, MAX_ATTEMPTS - len(recent))

def get_block_time_remaining(ip):
    if ip in BLOCKED_IPS:
        remaining = BLOCK_TIME - (time.time() - BLOCKED_IPS[ip])
        return max(0, int(remaining / 60))
    return 0

def check_tx_cooldown(user_id):
    if user_id in TX_COOLDOWNS:
        elapsed = time.time() - TX_COOLDOWNS[user_id]
        if elapsed < TX_COOLDOWN:
            return False, int(TX_COOLDOWN - elapsed)
    return True, 0

def set_tx_cooldown(user_id):
    TX_COOLDOWNS[user_id] = time.time()

def generate_totp_secret():
    return pyotp.random_base32()

def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)

def get_totp_uri(secret, username):
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="NYN NoyanCoin"
    )

def generate_backup_codes():
    codes = []
    for _ in range(8):
        code = base64.b32encode(os.urandom(5)).decode('utf-8').lower()
        codes.append(code)
    return codes

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('utf-8')
    return session['csrf_token']

def verify_csrf_token(token):
    return token and token == session.get('csrf_token')

def check_password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    if len(password) >= 12:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add numbers")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$...)")
    if score <= 2:
        strength = "weak"
    elif score <= 4:
        strength = "medium"
    else:
        strength = "strong"
    return score, strength, feedback

def sanitize_input(text, max_length=100):
    if not text:
        return ""
    text = str(text)[:max_length]
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()

def get_security_headers():
    return {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self' https://www.google.com https://www.gstatic.com https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' https://www.google.com https://www.gstatic.com https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline';",
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }

def validate_nyn_address(address):
    if not address:
        return False
    if not address.startswith('NYN'):
        return False
    if len(address) != 35:
        return False
    if not re.match(r'^NYN[A-F0-9]{32}$', address):
        return False
    return True

def check_daily_limit(user, amount):
    return user.total_sent_today + amount <= DAILY_TX_LIMIT

def format_login_alert(username, ip, user_agent):
    return f"""
    <div style="background:#0d1117;padding:40px;font-family:monospace;max-width:500px;margin:0 auto;border-radius:12px;border:1px solid #30363d;">
        <h1 style="color:#f85149;text-align:center;">⚠️ Security Alert</h1>
        <p style="color:#8b949e;text-align:center;margin-bottom:20px;">New login detected on your NYN account</p>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px;margin:16px 0;">
            <p style="color:#e6edf3;margin-bottom:8px;"><strong>Account:</strong> {username}</p>
            <p style="color:#e6edf3;margin-bottom:8px;"><strong>IP Address:</strong> {ip}</p>
            <p style="color:#e6edf3;margin-bottom:8px;"><strong>Time:</strong> {time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p style="color:#e6edf3;"><strong>Device:</strong> {user_agent[:50]}...</p>
        </div>
        <p style="color:#f85149;text-align:center;font-size:0.85em;">If this wasn't you, change your password immediately.</p>
        <p style="color:#8b949e;text-align:center;font-size:0.8em;margin-top:16px;">Republic of Nowhere — NYN NoyanCoin</p>
    </div>
    """