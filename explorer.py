from flask import Flask, jsonify, render_template_string, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
import json
import time
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per day", "10 per minute"])

# Database setup
engine = create_engine('sqlite:///nyn_blockchain.db')
Base = declarative_base()

class BlockModel(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    timestamp = Column(Float)
    transactions = Column(Text)
    previous_hash = Column(String(64))
    hash = Column(String(64))

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
    session = Session()
    blocks = session.query(BlockModel).order_by(BlockModel.index).all()
    session.close()
    return blocks

def add_block(transactions):
    session = Session()
    chain = session.query(BlockModel).order_by(BlockModel.index).all()
    if len(chain) == 0:
        previous_hash = "0"
        index = 0
    else:
        previous_hash = chain[-1].hash
        index = len(chain)
    timestamp = time.time()
    hash = calculate_hash(index, timestamp, json.dumps(transactions), previous_hash)
    block = BlockModel(
        index=index,
        timestamp=timestamp,
        transactions=json.dumps(transactions),
        previous_hash=previous_hash,
        hash=hash
    )
    session.add(block)
    session.commit()
    session.close()

# Create genesis block if empty
session = Session()
if session.query(BlockModel).count() == 0:
    add_block("NYN Genesis Block - Republic of Nowhere")
    add_block({"from": "Founder", "to": "Republic of Nowhere", "amount": 24000000})
session.close()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NYN Explorer - NoyanCoin</title>
    <style>
        body { background: #0a0a0a; color: #00ff88; font-family: monospace; padding: 20px; }
        h1 { color: #00ff88; text-align: center; font-size: 2em; }
        h3 { color: #888; text-align: center; }
        .block { background: #111; border: 1px solid #00ff88; margin: 10px 0; padding: 15px; border-radius: 8px; }
        .block h2 { color: #00ff88; margin: 0 0 10px 0; }
        .hash { color: #ff8800; word-break: break-all; }
        .data { color: #ffffff; }
        .stats { display: flex; justify-content: center; gap: 40px; margin: 20px 0; }
        .stat { text-align: center; background: #111; padding: 15px 25px; border-radius: 8px; border: 1px solid #333; }
        .stat h2 { color: #00ff88; margin: 0; }
        .stat p { color: #888; margin: 5px 0 0 0; }
    </style>
</head>
<body>
    <h1>⚡ NYN Explorer</h1>
    <h3>Republic of Nowhere — NoyanCoin Blockchain</h3>
    <div class="stats">
        <div class="stat"><h2>{{ blocks }}</h2><p>Blocks</p></div>
        <div class="stat"><h2>24,000,000</h2><p>Total Supply</p></div>
        <div class="stat"><h2>NYN</h2><p>Ticker</p></div>
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

@app.route('/')
def explorer():
    chain = get_chain()
    return render_template_string(HTML, chain=chain, blocks=len(chain))

NYN_SECRET = os.environ.get("NYN_SECRET", "fallback")

@limiter.limit("5 per minute")
@app.route('/add/<secret>/<data>')
def add(secret, data):
    if secret != NYN_SECRET:
        return jsonify({"error": "Unauthorized! You are not the Founder."}), 403
    add_block({"data": data, "timestamp": time.time()})
    return jsonify({"message": "Block added!", "blocks": len(get_chain())})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)