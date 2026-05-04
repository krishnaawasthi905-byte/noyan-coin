from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import os

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
    validator = Column(String(100), default="Genesis")
    tx_count = Column(Integer, default=0)
    size = Column(Integer, default=0)

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
    total_sent_today = Column(Float, default=0.0)
    last_tx_date = Column(String(10), nullable=True)
    blocks_validated = Column(Integer, default=0)
    theme = Column(String(10), default="dark")
    language = Column(String(10), default="en")
    notif_tx = Column(Boolean, default=True)
    notif_security = Column(Boolean, default=True)
    privacy_hide_balance = Column(Boolean, default=True)
    privacy_hide_txs = Column(Boolean, default=False)
    two_fa_secret = Column(String(32), nullable=True)
    two_fa_enabled = Column(Boolean, default=False)
    two_fa_backup_codes = Column(Text, nullable=True)
    login_count = Column(Integer, default=0)
    last_login = Column(Float, nullable=True)
    last_login_ip = Column(String(50), nullable=True)
    tx_pin = Column(String(200), nullable=True)
    tx_pin_enabled = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    bio = Column(String(200), nullable=True)

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
    note = Column(String(100), nullable=True)

class StakeModel(Base):
    __tablename__ = 'stakes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    wallet_address = Column(String(100))
    amount = Column(Float)
    staked_at = Column(Float)
    unstake_at = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    rewards_earned = Column(Float, default=0.0)

class LoginHistoryModel(Base):
    __tablename__ = 'login_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ip_address = Column(String(50))
    user_agent = Column(String(200))
    timestamp = Column(Float)
    success = Column(Boolean, default=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)