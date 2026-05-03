STYLES = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--border:#30363d;--text:#e6edf3;--text2:#8b949e;--green:#00ff88;--green2:#00cc6a;--orange:#f0883e;--red:#f85149;--blue:#58a6ff;--yellow:#e3b341;--purple:#a371f7;}
.light{--bg:#ffffff;--bg2:#f6f8fa;--bg3:#eaeef2;--border:#d0d7de;--text:#1f2328;--text2:#636c76;--green:#1a7f37;--green2:#2da44e;--orange:#bc4c00;--red:#cf222e;--blue:#0969da;--yellow:#9a6700;--purple:#8250df;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;transition:background 0.3s,color 0.3s;}
a{color:var(--green);text-decoration:none;}
a:hover{text-decoration:underline;}
.navbar{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:64px;position:sticky;top:0;z-index:100;}
.navbar-brand{display:flex;align-items:center;gap:10px;font-size:1.2em;font-weight:700;color:var(--green);text-decoration:none;}
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
.market-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:16px 0;}
.market-card{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:16px;}
.market-card .m-label{font-size:0.78em;color:var(--text2);margin-bottom:4px;}
.market-card .m-value{font-size:1em;font-weight:600;color:var(--text);}
.market-card .m-value.green{color:var(--green);}
.market-card .m-value.orange{color:var(--orange);}
.market-card .m-value.purple{color:var(--purple);}
.blocks-visual{display:flex;gap:8px;overflow-x:auto;padding:16px 0;scrollbar-width:thin;scrollbar-color:var(--border) transparent;}
.block-vis{min-width:88px;height:88px;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:transform 0.2s,box-shadow 0.2s;text-align:center;padding:8px;}
.block-vis:hover{transform:translateY(-6px);box-shadow:0 8px 24px rgba(0,0,0,0.3);}
.block-vis .bv-num{font-size:0.85em;font-weight:700;}
.block-vis .bv-icon{font-size:1.4em;margin-bottom:2px;}
.block-vis .bv-tx{font-size:0.65em;margin-top:2px;opacity:0.7;}
.section-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px;}
.section-title{font-size:1em;font-weight:600;color:var(--text);margin-bottom:16px;display:flex;align-items:center;gap:8px;}
.block-row{display:grid;grid-template-columns:80px 1fr 1fr 100px;gap:16px;padding:14px 0;border-bottom:1px solid var(--border);align-items:center;font-size:0.875em;}
.block-row:last-child{border-bottom:none;}
.block-num-badge{background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:4px 10px;font-weight:700;color:var(--green);text-align:center;font-family:monospace;font-size:0.9em;}
.hash-text{font-family:monospace;color:var(--orange);font-size:0.8em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.search-bar{display:flex;gap:8px;margin-bottom:24px;}
.search-bar input{flex:1;padding:12px 16px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;transition:border-color 0.2s;}
.search-bar input:focus{border-color:var(--green);}
.search-bar button{padding:12px 24px;background:var(--green);color:#000;border:none;border-radius:8px;font-weight:600;cursor:pointer;}
.form-page{min-height:calc(100vh - 64px);display:flex;align-items:center;justify-content:center;padding:24px;}
.form-card{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:36px;width:100%;max-width:440px;}
.form-card h2{font-size:1.4em;font-weight:700;margin-bottom:4px;}
.form-card .sub{color:var(--text2);font-size:0.9em;margin-bottom:24px;}
.fg{margin-bottom:14px;}
.fg label{display:block;font-size:0.875em;font-weight:500;color:var(--text2);margin-bottom:6px;}
.fg input,.fg select{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;transition:border-color 0.2s;}
.fg input:focus,.fg select:focus{border-color:var(--green);}
.input-wrap{position:relative;}
.input-wrap input{padding-right:44px;}
.eye-btn{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--text2);cursor:pointer;font-size:1em;padding:0;}
.btn-full{width:100%;padding:12px;background:var(--green);color:#000;border:none;border-radius:8px;font-size:1em;font-weight:600;cursor:pointer;margin-top:8px;transition:background 0.2s;}
.btn-full:hover{background:var(--green2);}
.btn-outline{width:100%;padding:12px;background:transparent;color:var(--text);border:1px solid var(--border);border-radius:8px;font-size:1em;font-weight:500;cursor:pointer;margin-top:8px;transition:all 0.2s;}
.btn-outline:hover{background:var(--bg3);}
.btn-danger{width:100%;padding:12px;background:transparent;color:var(--red);border:1px solid var(--red);border-radius:8px;font-size:1em;font-weight:500;cursor:pointer;margin-top:8px;transition:all 0.2s;}
.btn-danger:hover{background:var(--red);color:#fff;}
.form-footer{text-align:center;margin-top:20px;font-size:0.875em;color:var(--text2);}
.alert{padding:12px 16px;border-radius:8px;margin-bottom:16px;font-size:0.875em;}
.alert.error{background:rgba(248,81,73,0.1);border:1px solid var(--red);color:var(--red);}
.alert.success{background:rgba(0,255,136,0.1);border:1px solid var(--green);color:var(--green);}
.alert.info{background:rgba(88,166,255,0.1);border:1px solid var(--blue);color:var(--blue);}
.alert.warning{background:rgba(227,179,65,0.1);border:1px solid var(--yellow);color:var(--yellow);}
.bonus-badge{background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.25);border-radius:8px;padding:10px 14px;margin-bottom:20px;font-size:0.875em;color:var(--green);text-align:center;}
.recaptcha-wrap{display:flex;justify-content:center;margin:16px 0;transform:scale(0.9);transform-origin:center;}
.page-wrap{max-width:900px;margin:0 auto;padding:24px;}
.wallet-header{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:28px;margin-bottom:16px;}
.user-row{display:flex;align-items:center;gap:16px;margin-bottom:20px;}
.avatar{width:52px;height:52px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.4em;font-weight:700;color:#000;flex-shrink:0;}
.uname{font-size:1.3em;font-weight:700;}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.75em;font-weight:600;margin-left:6px;}
.badge.v{background:rgba(0,255,136,0.15);color:var(--green);border:1px solid var(--green);}
.badge.u{background:rgba(248,81,73,0.15);color:var(--red);border:1px solid var(--red);}
.badge.pos{background:rgba(163,113,247,0.15);color:var(--purple);border:1px solid var(--purple);}
.balance-box{text-align:center;padding:24px;background:var(--bg);border-radius:12px;margin-bottom:16px;border:1px solid var(--border);}
.bal-label{font-size:0.85em;color:var(--text2);margin-bottom:8px;}
.bal-amount{font-size:2.8em;font-weight:700;color:var(--green);font-family:monospace;}
.bal-dots{font-size:2.5em;letter-spacing:6px;color:var(--text2);}
.show-btn{background:none;border:1px solid var(--border);color:var(--text2);cursor:pointer;font-size:0.82em;padding:6px 14px;border-radius:6px;margin-top:8px;transition:all 0.2s;}
.show-btn:hover{border-color:var(--green);color:var(--green);}
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
.tx-preview-box{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px;display:none;}
.tx-preview-box.show{display:block;}
.tx-row{font-size:0.85em;display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);}
.tx-row:last-child{border-bottom:none;}
.tx-item{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border);}
.tx-item:last-child{border-bottom:none;}
.tx-icon{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1em;flex-shrink:0;}
.tx-icon.in{background:rgba(0,255,136,0.15);color:var(--green);}
.tx-icon.out{background:rgba(248,81,73,0.15);color:var(--red);}
.tx-info{flex:1;min-width:0;}
.tx-label{font-size:0.85em;font-weight:500;}
.tx-addr{font-size:0.78em;color:var(--text2);font-family:monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tx-time{font-size:0.75em;color:var(--text2);}
.tx-status-badge{font-size:0.7em;padding:2px 8px;border-radius:10px;background:rgba(0,255,136,0.1);color:var(--green);border:1px solid rgba(0,255,136,0.3);}
.tx-amount{font-weight:700;font-size:0.95em;white-space:nowrap;}
.tx-amount.in{color:var(--green);}
.tx-amount.out{color:var(--red);}
.ref-code{font-size:1.5em;font-weight:700;color:var(--green);font-family:monospace;letter-spacing:3px;}
.progress-bar{background:var(--bg);border-radius:4px;height:8px;margin-top:8px;overflow:hidden;}
.progress-fill{background:var(--green);height:100%;border-radius:4px;transition:width 0.5s;}
.stake-box{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:12px;}
.stake-stat{display:flex;justify-content:space-between;font-size:0.875em;padding:6px 0;border-bottom:1px solid var(--border);}
.stake-stat:last-child{border-bottom:none;}
.profile-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;}
.profile-item{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:14px;}
.pi-label{font-size:0.75em;color:var(--text2);margin-bottom:4px;}
.pi-value{font-size:0.9em;font-weight:600;}
.settings-section{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px;}
.settings-section h3{font-size:1em;font-weight:600;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--border);}
.setting-row{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--border);}
.setting-row:last-child{border-bottom:none;}
.setting-label{font-size:0.9em;font-weight:500;}
.setting-desc{font-size:0.78em;color:var(--text2);margin-top:2px;}
.toggle{position:relative;display:inline-block;width:44px;height:24px;}
.toggle input{opacity:0;width:0;height:0;}
.toggle-slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:var(--bg3);border-radius:24px;transition:0.3s;border:1px solid var(--border);}
.toggle-slider:before{position:absolute;content:"";height:18px;width:18px;left:2px;bottom:2px;background:var(--text2);border-radius:50%;transition:0.3s;}
.toggle input:checked + .toggle-slider{background:var(--green);border-color:var(--green);}
.toggle input:checked + .toggle-slider:before{transform:translateX(20px);background:#000;}
.select-styled{padding:8px 12px;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:0.875em;outline:none;cursor:pointer;}
.select-styled:focus{border-color:var(--green);}
.otp-input{font-size:2em;text-align:center;letter-spacing:12px;font-family:monospace;font-weight:700;}
.footer{background:var(--bg2);border-top:1px solid var(--border);padding:32px 24px;text-align:center;color:var(--text2);font-size:0.85em;margin-top:40px;}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;max-width:800px;margin:0 auto 24px;}
.footer-col h4{color:var(--text);margin-bottom:10px;font-size:0.9em;}
.footer-col a{display:block;color:var(--text2);font-size:0.85em;margin-bottom:6px;}
.footer-col a:hover{color:var(--green);text-decoration:none;}
.network-status{display:inline-flex;align-items:center;gap:6px;background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.3);border-radius:20px;padding:4px 12px;font-size:0.8em;color:var(--green);}
.pulse{width:8px;height:8px;background:var(--green);border-radius:50%;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
@media(max-width:600px){.hero h1{font-size:1.8em;}.stats-grid{grid-template-columns:repeat(2,1fr);}.profile-grid{grid-template-columns:1fr;}.block-row{grid-template-columns:60px 1fr;}.block-row .hash-text:last-child,.block-row div:last-child{display:none;}}
</style>
<script>
function toggleTheme(){document.body.classList.toggle('light');localStorage.setItem('nyn_theme',document.body.classList.contains('light')?'light':'dark');}
function togglePwd(id){var i=document.getElementById(id);i.type=i.type==='password'?'text':'password';}
function applyTheme(t){if(t==='light')document.body.classList.add('light');else document.body.classList.remove('light');}
window.onload=function(){var t=localStorage.getItem('nyn_theme')||'dark';applyTheme(t);}
</script>
"""

NAV_IN = """
<nav class="navbar">
  <a href="/" class="navbar-brand">⚡ NYN <span>NoyanCoin</span></a>
  <div class="navbar-links">
    <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    <a href="/" class="nav-btn">Explorer</a>
    <a href="/wallet" class="nav-btn">Wallet</a>
    <a href="/profile" class="nav-btn">Profile</a>
    <a href="/settings" class="nav-btn">Settings</a>
    <a href="/logout" class="nav-btn danger">Logout</a>
  </div>
</nav>
"""

NAV_OUT = """
<nav class="navbar">
  <a href="/" class="navbar-brand">⚡ NYN <span>NoyanCoin Explorer</span></a>
  <div class="navbar-links">
    <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    <a href="/login" class="nav-btn">Login</a>
    <a href="/register" class="nav-btn primary">Get Wallet</a>
  </div>
</nav>
"""

FOOTER = """
<div class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col"><h4>NYN NoyanCoin</h4><a href="/">Explorer</a><a href="/register">Create Wallet</a><a href="/login">Login</a></div>
      <div class="footer-col"><h4>Network</h4><a href="#">Whitepaper</a><a href="#">GitHub</a><a href="#">@OfficiaNowhere</a></div>
      <div class="footer-col"><h4>Info</h4><a href="#">About NYN</a><a href="#">Privacy</a><a href="#">Security</a></div>
    </div>
    <div style="margin-bottom:12px;"><span class="network-status"><span class="pulse"></span> Network Active</span></div>
    <p>⚡ NYN NoyanCoin — Republic of Nowhere — Currency of Everywhere</p>
    <p style="margin-top:6px;">Balance privacy enabled • Human verified • Proof of Stake consensus</p>
  </div>
</div>
"""

MAIN_HTML = """<!DOCTYPE html><html><head><title>NYN Explorer - NoyanCoin Blockchain</title>""" + STYLES + """</head><body>
""" + NAV_OUT + """
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
    <div class="stat-card"><div class="val">24M</div><div class="lbl">Max Supply</div></div>
    <div class="stat-card"><div class="val">{{ circulating }}</div><div class="lbl">Circulating Supply</div></div>
    <div class="stat-card"><div class="val">{{ users }}</div><div class="lbl">Total Wallets</div></div>
    <div class="stat-card"><div class="val">{{ txns }}</div><div class="lbl">Transactions</div></div>
    <div class="stat-card"><div class="val">{{ total_staked }} NYN</div><div class="lbl">Total Staked</div></div>
    <div class="stat-card"><div class="val">~2s</div><div class="lbl">Block Time</div></div>
    <div class="stat-card"><div class="val">PoS</div><div class="lbl">Consensus</div></div>
  </div>

  <div class="section-card">
    <div class="section-title">📊 Market Info</div>
    <div class="market-grid">
      <div class="market-card"><div class="m-label">Algorithm</div><div class="m-value purple">Proof of Stake</div></div>
      <div class="market-card"><div class="m-label">Max Supply</div><div class="m-value">24,000,000 NYN</div></div>
      <div class="market-card"><div class="m-label">Genesis Block</div><div class="m-value">{{ genesis_date }}</div></div>
      <div class="market-card"><div class="m-label">Consensus</div><div class="m-value green">PoS Active ✓</div></div>
      <div class="market-card"><div class="m-label">Privacy</div><div class="m-value green">Balance Hidden ✓</div></div>
      <div class="market-card"><div class="m-label">Human Verified</div><div class="m-value green">Required ✓</div></div>
      <div class="market-card"><div class="m-label">Min Stake</div><div class="m-value">10 NYN</div></div>
      <div class="market-card"><div class="m-label">Network</div><div class="m-value orange">Testnet</div></div>
    </div>
  </div>

  <div class="section-card">
    <div class="section-title">🔲 Block Visualization</div>
    <div class="blocks-visual">
      {% set colors = ['#a371f7','#58a6ff','#00ff88','#f0883e','#e3b341','#f85149','#3fb950','#79c0ff'] %}
      {% for block in chain %}
      {% set color = colors[block.index % 8] %}
      <div class="block-vis" style="background:{{ color }}18;border:2px solid {{ color }}40;" onclick="document.getElementById('block-{{ block.index }}').scrollIntoView({behavior:'smooth'})">
        <span class="bv-icon" style="color:{{ color }};">⬡</span>
        <span class="bv-num" style="color:{{ color }};">#{{ block.index }}</span>
        <span class="bv-tx" style="color:{{ color }};">{{ block.tx_count }} tx</span>
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
    {% set colors = ['#a371f7','#58a6ff','#00ff88','#f0883e','#e3b341','#f85149','#3fb950','#79c0ff'] %}
    {% set color = colors[block.index % 8] %}
    <div class="block-row" id="block-{{ block.index }}">
      <div><span class="block-num-badge" style="color:{{ color }};border-color:{{ color }}40;">#{{ block.index }}</span></div>
      <div>
        <div class="hash-text">🔗 {{ block.hash }}</div>
        <div style="font-size:0.72em;color:var(--text2);margin-top:3px;font-family:monospace;">◀ {{ block.previous_hash[:40] }}...</div>
      </div>
      <div class="hash-text" style="color:var(--text2);font-size:0.78em;">{{ block.transactions[:55] }}...</div>
      <div style="font-size:0.8em;color:var(--text2);">
        <div>🔏 {{ block.validator[:14] if block.validator else 'System' }}</div>
        <div style="margin-top:3px;color:var(--purple);">{{ block.tx_count }} tx</div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
""" + FOOTER + """
</body></html>
"""

REGISTER_HTML = """<!DOCTYPE html><html><head><title>Create Wallet - NYN</title>""" + STYLES + """
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head><body>""" + NAV_OUT + """
<div class="form-page">
<div class="form-card">
  <h2>Create Your Wallet</h2>
  <p class="sub">Join the Republic of Nowhere</p>
  <div class="bonus-badge">🎁 50 NYN free on signup • Earn 20 NYN per referral (max 3)</div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Username</label><input type="text" name="username" placeholder="Choose a username" required maxlength="30" autocomplete="off"></div>
    <div class="fg"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div class="fg"><label>Password</label>
      <div class="input-wrap"><input type="password" name="password" id="p1" placeholder="Min 8 characters" required minlength="8"><button type="button" class="eye-btn" onclick="togglePwd('p1')">👁</button></div>
    </div>
    <div class="fg"><label>Confirm Password</label>
      <div class="input-wrap"><input type="password" name="confirm" id="p2" placeholder="Repeat password" required><button type="button" class="eye-btn" onclick="togglePwd('p2')">👁</button></div>
    </div>
    <div class="fg"><label>Referral Code (optional)</label><input type="text" name="referral" placeholder="Enter code for +20 NYN bonus"></div>
    <div class="recaptcha-wrap"><div class="g-recaptcha" data-sitekey="{{ site_key }}"></div></div>
    <button type="submit" class="btn-full">Create Wallet & Get 50 NYN ⚡</button>
  </form>
  <div class="form-footer">Already have a wallet? <a href="/login">Login here</a></div>
</div>
</div>""" + FOOTER + """</body></html>"""

LOGIN_HTML = """<!DOCTYPE html><html><head><title>Login - NYN</title>""" + STYLES + """</head><body>""" + NAV_OUT + """
<div class="form-page">
<div class="form-card">
  <h2>Welcome Back</h2>
  <p class="sub">Login to your NYN wallet</p>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Username</label><input type="text" name="username" placeholder="Your username" required autocomplete="username"></div>
    <div class="fg"><label>Password</label>
      <div class="input-wrap"><input type="password" name="password" id="lp" placeholder="Your password" required autocomplete="current-password"><button type="button" class="eye-btn" onclick="togglePwd('lp')">👁</button></div>
    </div>
    <button type="submit" class="btn-full">Login ⚡</button>
  </form>
  <div class="form-footer">No wallet yet? <a href="/register">Create one free</a></div>
</div>
</div>""" + FOOTER + """</body></html>"""

VERIFY_HTML = """<!DOCTYPE html><html><head><title>Verify Email - NYN</title>""" + STYLES + """</head><body>
<nav class="navbar"><a href="/" class="navbar-brand">⚡ NYN <span>NoyanCoin</span></a><div class="navbar-links"><button class="theme-btn" onclick="toggleTheme()">🌙</button></div></nav>
<div class="form-page">
<div class="form-card">
  <h2>Verify Your Email</h2>
  <p class="sub">Enter the 6-digit code sent to your inbox</p>
  <div class="alert info">📧 Check your inbox AND spam/junk folder</div>
  <div class="alert warning">⚠️ If in spam, mark as "Not Spam" to receive future emails</div>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Verification Code</label><input type="text" name="otp" class="otp-input" placeholder="000000" maxlength="6" required autocomplete="off" autofocus></div>
    <button type="submit" class="btn-full">Verify & Activate Wallet ⚡</button>
  </form>
  <div class="form-footer"><a href="/resend-otp">Resend verification code</a></div>
</div>
</div></body></html>"""

WALLET_HTML = """<!DOCTYPE html><html><head><title>My Wallet - NYN</title>""" + STYLES + """
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head><body>""" + NAV_IN + """
<div class="page-wrap">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}

  <div class="wallet-header">
    <div class="user-row">
      <div class="avatar">{{ user.username[0].upper() }}</div>
      <div>
        <div class="uname">{{ user.username }}
          <span class="badge {{ 'v' if user.is_verified else 'u' }}">{{ '✓ Verified' if user.is_verified else '✗ Unverified' }}</span>
          {% if user.staked_amount >= 10 %}<span class="badge pos">⛏ Validator</span>{% endif %}
        </div>
        <div style="font-size:0.85em;color:var(--text2);">Member since {{ created_at }}</div>
      </div>
    </div>

    <div class="balance-box">
      <div class="bal-label">Your Balance (Private)</div>
      <div id="bal" class="bal-dots">••••••</div>
      <button class="show-btn" onclick="toggleBal()">👁 Show / Hide Balance</button>
      <div class="privacy-note">🔒 Your balance is private by default. Only you can reveal it.</div>
    </div>

    <div style="margin-top:16px;">
      <div style="font-size:0.85em;color:var(--text2);margin-bottom:6px;">NYN Wallet Address</div>
      <div class="addr-box">{{ user.wallet_address }}</div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ user.wallet_address }}');this.textContent='✓ Copied!'">📋 Copy Address</button>
    </div>
    <div class="qr-wrap"><div id="qrcode"></div></div>
  </div>

  {% if not user.is_verified %}
  <div class="wsection" style="border-color:var(--red);">
    <h3 style="color:var(--red);">⚠️ Email Not Verified</h3>
    <p style="color:var(--text2);font-size:0.9em;margin-bottom:12px;">Verify your email to unlock all features.</p>
    <a href="/verify" style="display:block;text-align:center;padding:10px;background:var(--red);color:#fff;border-radius:8px;font-weight:600;text-decoration:none;">Verify Email Now</a>
  </div>
  {% endif %}

  <div class="wsection">
    <h3>💸 Send NYN</h3>
    <div class="alert info" style="margin-bottom:12px;">🔐 All transactions are verified by PoS consensus before confirmation. Zero fees.</div>
    <input type="text" class="send-input" id="recv" placeholder="Receiver NYN wallet address (starts with NYN...)" oninput="preview()">
    <input type="number" class="send-input" id="amt" placeholder="Amount in NYN (max 10,000 per transaction)" step="0.01" min="0.01" max="10000" oninput="preview()">
    <div class="tx-preview-box" id="prev-box">
      <div style="font-size:0.875em;font-weight:600;margin-bottom:10px;color:var(--text);">📋 Transaction Preview</div>
      <div class="tx-row"><span style="color:var(--text2);">From</span><span style="font-family:monospace;font-size:0.8em;">{{ user.wallet_address[:24] }}...</span></div>
      <div class="tx-row"><span style="color:var(--text2);">To</span><span id="p-to" style="font-family:monospace;font-size:0.8em;">-</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Amount</span><span id="p-amt" style="color:var(--green);font-weight:700;">-</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Network Fee</span><span style="color:var(--green);">0 NYN (Free)</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Consensus</span><span style="color:var(--purple);">Proof of Stake ✓</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Status</span><span style="color:var(--green);">Ready</span></div>
    </div>
    <form method="POST" action="/send" id="sf">
      <input type="hidden" name="receiver" id="rh">
      <input type="hidden" name="amount" id="ah">
      <button type="button" class="send-btn" onclick="doSend()">Confirm & Send NYN ⚡</button>
    </form>
  </div>

  <div class="wsection">
    <h3>⛏ Staking — Become a Validator</h3>
    <div class="alert info" style="margin-bottom:12px;">Stake NYN to become a validator and earn 0.1 NYN reward per block validated. Minimum 10 NYN to stake.</div>
    {% if stake_info %}
    <div class="stake-box">
      <div class="stake-stat"><span style="color:var(--text2);">Staked Amount</span><span style="color:var(--green);font-weight:700;">{{ stake_info.amount }} NYN</span></div>
      <div class="stake-stat"><span style="color:var(--text2);">Rewards Earned</span><span style="color:var(--yellow);">{{ stake_info.rewards }} NYN</span></div>
      <div class="stake-stat"><span style="color:var(--text2);">Status</span><span style="color:var(--green);">Active Validator ✓</span></div>
      <div class="stake-stat"><span style="color:var(--text2);">Blocks Validated</span><span>{{ user.blocks_validated }}</span></div>
    </div>
    <form method="POST" action="/unstake"><button type="submit" class="btn-danger">Unstake NYN</button></form>
    {% else %}
    <form method="POST" action="/stake">
      <input type="number" name="amount" class="send-input" placeholder="Amount to stake (min 10 NYN)" min="10" step="0.01" required>
      <button type="submit" class="send-btn" style="background:var(--purple);border-color:var(--purple);">Stake NYN & Become Validator ⛏</button>
    </form>
    {% endif %}
  </div>

  <div class="wsection">
    <h3>🎁 Referral Program</h3>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:14px;">Share your code — earn 20 NYN per referral. Max 3 referrals.</p>
    <div class="ref-code">{{ user.referral_code }}</div>
    <button class="copy-btn" style="margin-top:10px;" onclick="navigator.clipboard.writeText('{{ user.referral_code }}');this.textContent='✓ Copied!'">📋 Copy Code</button>
    <div style="margin-top:12px;">
      <div style="font-size:0.85em;color:var(--text2);">Referrals: {{ user.referral_count }}/3</div>
      <div class="progress-bar"><div class="progress-fill" style="width:{{ (user.referral_count/3*100)|int }}%"></div></div>
    </div>
  </div>

  <div class="wsection">
    <h3>📋 Transaction History</h3>
    {% if transactions %}
    {% for tx in transactions %}
    <div class="tx-item">
      <div class="tx-icon {{ tx.type }}">{{ '↓' if tx.type == 'in' else '↑' }}</div>
      <div class="tx-info">
        <div class="tx-label">{{ 'Received from' if tx.type == 'in' else 'Sent to' }}</div>
        <div class="tx-addr">{{ tx.sender[:30] if tx.type == 'in' else tx.receiver[:30] }}...</div>
        <div class="tx-time">{{ tx.time }} • <span class="tx-status-badge">✓ Confirmed</span></div>
      </div>
      <div class="tx-amount {{ tx.type }}">{{ '+' if tx.type == 'in' else '-' }}{{ tx.amount }} NYN</div>
    </div>
    {% endfor %}
    {% else %}
    <p style="color:var(--text2);text-align:center;padding:20px 0;font-size:0.9em;">No transactions yet. Send or receive NYN to see history.</p>
    {% endif %}
  </div>
</div>
""" + FOOTER + """
<script>
var bv=false,rb="{{ user.balance }} NYN";
function toggleBal(){bv=!bv;var e=document.getElementById('bal');e.className=bv?'bal-amount':'bal-dots';e.textContent=bv?rb:'••••••';}
function preview(){var r=document.getElementById('recv').value,a=document.getElementById('amt').value,b=document.getElementById('prev-box');if(r.length>5&&a>0){document.getElementById('p-to').textContent=r.substring(0,24)+'...';document.getElementById('p-amt').textContent=a+' NYN';b.classList.add('show');}else{b.classList.remove('show');}}
function doSend(){var r=document.getElementById('recv').value,a=document.getElementById('amt').value;if(!r||!a){alert('Fill in receiver and amount');return;}if(!r.startsWith('NYN')){alert('Invalid NYN address - must start with NYN');return;}if(parseFloat(a)>10000){alert('Max 10,000 NYN per transaction');return;}if(confirm('Send '+a+' NYN to '+r.substring(0,20)+'...?')){document.getElementById('rh').value=r;document.getElementById('ah').value=a;document.getElementById('sf').submit();}}
new QRCode(document.getElementById("qrcode"),{text:"{{ user.wallet_address }}",width:128,height:128,colorDark:"#000000",colorLight:"#ffffff"});
</script>
</body></html>"""

PROFILE_HTML = """<!DOCTYPE html><html><head><title>Profile - NYN</title>""" + STYLES + """</head><body>""" + NAV_IN + """
<div class="page-wrap">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}
  <div class="wsection">
    <h3>👤 Your Profile</h3>
    <div class="user-row" style="margin-bottom:20px;">
      <div class="avatar" style="width:64px;height:64px;font-size:1.8em;">{{ user.username[0].upper() }}</div>
      <div>
        <div class="uname">{{ user.username }}
          <span class="badge {{ 'v' if user.is_verified else 'u' }}">{{ '✓ Verified' if user.is_verified else '✗ Unverified' }}</span>
        </div>
        <div style="color:var(--text2);font-size:0.85em;">{{ user.email }}</div>
        <div style="color:var(--text2);font-size:0.85em;">Member since {{ created_at }}</div>
      </div>
    </div>
    <div class="profile-grid">
      <div class="profile-item"><div class="pi-label">Total Sent</div><div class="pi-value" style="color:var(--red);">{{ user.total_sent|round(2) }} NYN</div></div>
      <div class="profile-item"><div class="pi-label">Total Received</div><div class="pi-value" style="color:var(--green);">{{ user.total_received|round(2) }} NYN</div></div>
      <div class="profile-item"><div class="pi-label">Blocks Validated</div><div class="pi-value" style="color:var(--purple);">{{ user.blocks_validated }}</div></div>
      <div class="profile-item"><div class="pi-label">Referrals Made</div><div class="pi-value">{{ user.referral_count }}/3</div></div>
      <div class="profile-item"><div class="pi-label">Staked Amount</div><div class="pi-value" style="color:var(--yellow);">{{ user.staked_amount }} NYN</div></div>
      <div class="profile-item"><div class="pi-label">Network</div><div class="pi-value">NYN Testnet</div></div>
    </div>
  </div>
  <div class="wsection" style="border-color:var(--red);">
    <h3 style="color:var(--red);">⚠️ Danger Zone</h3>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:12px;">Account deletion is permanent and irreversible.</p>
    <button onclick="alert('Account deletion coming soon. Contact support on @OfficiaNowhere')" class="btn-danger">Delete Account</button>
  </div>
</div>""" + FOOTER + """</body></html>"""

SETTINGS_HTML = """<!DOCTYPE html><html><head><title>Settings - NYN</title>""" + STYLES + """</head><body>""" + NAV_IN + """
<div class="page-wrap">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}

  <div class="settings-section">
    <h3>🎨 Appearance</h3>
    <form method="POST">
      <input type="hidden" name="action" value="theme">
      <div class="setting-row">
        <div><div class="setting-label">Theme</div><div class="setting-desc">Choose your preferred color scheme</div></div>
        <select name="theme" class="select-styled" onchange="this.form.submit();applyTheme(this.value);localStorage.setItem('nyn_theme',this.value)">
          <option value="dark" {{ 'selected' if user.theme == 'dark' else '' }}>🌙 Dark</option>
          <option value="light" {{ 'selected' if user.theme == 'light' else '' }}>☀️ Light</option>
        </select>
      </div>
    </form>
    <form method="POST">
      <input type="hidden" name="action" value="language">
      <div class="setting-row">
        <div><div class="setting-label">Language</div><div class="setting-desc">Select your preferred language</div></div>
        <select name="language" class="select-styled" onchange="this.form.submit()">
          <option value="en" {{ 'selected' if user.language == 'en' else '' }}>🇬🇧 English</option>
          <option value="hi" {{ 'selected' if user.language == 'hi' else '' }}>🇮🇳 Hindi</option>
        </select>
      </div>
    </form>
  </div>

  <div class="settings-section">
    <h3>🔔 Notifications</h3>
    <form method="POST">
      <input type="hidden" name="action" value="notifications">
      <div class="setting-row">
        <div><div class="setting-label">Transaction Alerts</div><div class="setting-desc">Get notified when you send or receive NYN</div></div>
        <label class="toggle"><input type="checkbox" name="notif_tx" {{ 'checked' if user.notif_tx else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Security Alerts</div><div class="setting-desc">Get notified about login attempts and security events</div></div>
        <label class="toggle"><input type="checkbox" name="notif_security" {{ 'checked' if user.notif_security else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
    </form>
  </div>

  <div class="settings-section">
    <h3>🔒 Privacy</h3>
    <form method="POST">
      <input type="hidden" name="action" value="privacy">
      <div class="setting-row">
        <div><div class="setting-label">Hide Balance by Default</div><div class="setting-desc">Your balance will be hidden when you open wallet</div></div>
        <label class="toggle"><input type="checkbox" name="privacy_hide_balance" {{ 'checked' if user.privacy_hide_balance else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Hide Transaction History</div><div class="setting-desc">Your transactions will be hidden by default</div></div>
        <label class="toggle"><input type="checkbox" name="privacy_hide_txs" {{ 'checked' if user.privacy_hide_txs else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
    </form>
  </div>

  <div class="settings-section">
    <h3>🛡️ Security — Change Password</h3>
    <form method="POST" action="/change-password">
      <div class="fg"><label>Current Password</label>
        <div class="input-wrap"><input type="password" name="current_password" id="cp1" placeholder="Current password" required><button type="button" class="eye-btn" onclick="togglePwd('cp1')">👁</button></div>
      </div>
      <div class="fg"><label>New Password</label>
        <div class="input-wrap"><input type="password" name="new_password" id="cp2" placeholder="New password (min 8 chars)" required minlength="8"><button type="button" class="eye-btn" onclick="togglePwd('cp2')">👁</button></div>
      </div>
      <div class="fg"><label>Confirm New Password</label>
        <div class="input-wrap"><input type="password" name="confirm_password" id="cp3" placeholder="Confirm new password" required><button type="button" class="eye-btn" onclick="togglePwd('cp3')">👁</button></div>
      </div>
      <button type="submit" class="btn-full">Update Password</button>
    </form>
  </div>

  <div class="settings-section">
    <h3>💳 Wallet Info</h3>
    <div class="setting-row">
      <div><div class="setting-label">Wallet Address</div><div class="setting-desc" style="font-family:monospace;color:var(--orange);">{{ user.wallet_address[:24] }}...</div></div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ user.wallet_address }}');this.textContent='✓ Copied!'">📋 Copy</button>
    </div>
    <div class="setting-row">
      <div><div class="setting-label">Referral Code</div><div class="setting-desc" style="font-family:monospace;color:var(--green);font-size:1em;">{{ user.referral_code }}</div></div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ user.referral_code }}');this.textContent='✓ Copied!'">📋 Copy</button>
    </div>
    <div class="setting-row">
      <div><div class="setting-label">Network</div></div>
      <span style="color:var(--orange);font-size:0.875em;">NYN Testnet</span>
    </div>
  </div>
</div>
""" + FOOTER + """</body></html>"""