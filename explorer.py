from flask import Flask, jsonify, render_template_string
import hashlib
import json
import time

app = Flask(__name__)

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "NYN Genesis Block - Republic of Nowhere", "0")

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, previous_block.hash)
        self.chain.append(new_block)
        return new_block

nyn = Blockchain()
nyn.add_block({"from": "Aryan", "to": "World", "amount": 24000000})

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
    return render_template_string(HTML, chain=nyn.chain, blocks=len(nyn.chain))

if __name__ == '__main__':
    app.run(debug=True, port=5000)