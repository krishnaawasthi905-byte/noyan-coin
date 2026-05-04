STYLES = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--border:#30363d;--text:#e6edf3;--text2:#8b949e;--green:#00ff88;--green2:#00cc6a;--orange:#f0883e;--red:#f85149;--blue:#58a6ff;--yellow:#e3b341;--purple:#a371f7;--sidebar-w:240px;}
.light{--bg:#ffffff;--bg2:#f6f8fa;--bg3:#eaeef2;--border:#d0d7de;--text:#1f2328;--text2:#636c76;--green:#1a7f37;--green2:#2da44e;--orange:#bc4c00;--red:#cf222e;--blue:#0969da;--yellow:#9a6700;--purple:#8250df;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;}
a{color:var(--green);text-decoration:none;}
a:hover{text-decoration:underline;}

/* SIDEBAR */
.sidebar{position:fixed;left:0;top:0;width:var(--sidebar-w);height:100vh;background:var(--bg2);border-right:1px solid var(--border);display:flex;flex-direction:column;z-index:200;overflow-y:auto;}
.sidebar-logo{padding:20px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;}
.sidebar-logo span{font-size:1.3em;font-weight:700;color:var(--green);}
.sidebar-logo small{color:var(--text2);font-size:0.75em;display:block;}
.sidebar-nav{padding:8px 0;flex:1;}
.sidebar-section{padding:12px 16px 4px;font-size:0.7em;font-weight:600;color:var(--text2);text-transform:uppercase;letter-spacing:0.8px;}
.sidebar-item{display:flex;align-items:center;gap:12px;padding:10px 16px;color:var(--text2);font-size:0.9em;transition:all 0.2s;border-radius:0;cursor:pointer;text-decoration:none;}
.sidebar-item:hover{background:var(--bg3);color:var(--text);text-decoration:none;}
.sidebar-item.active{background:rgba(0,255,136,0.1);color:var(--green);border-right:2px solid var(--green);}
.sidebar-item .icon{width:20px;text-align:center;font-size:1em;}
.sidebar-bottom{padding:16px;border-top:1px solid var(--border);}
.sidebar-user{display:flex;align-items:center;gap:10px;padding:8px;border-radius:8px;background:var(--bg3);}
.sidebar-avatar{width:32px;height:32px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;color:#000;font-size:0.85em;flex-shrink:0;}

/* MAIN CONTENT */
.main-content{margin-left:var(--sidebar-w);min-height:100vh;}
.topbar{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;}
.topbar-search{display:flex;align-items:center;gap:8px;flex:1;max-width:500px;}
.topbar-search input{flex:1;padding:8px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.875em;outline:none;transition:border-color 0.2s;}
.topbar-search input:focus{border-color:var(--green);}
.topbar-search button{padding:8px 16px;background:var(--green);color:#000;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.875em;}
.topbar-right{display:flex;align-items:center;gap:12px;}
.theme-btn{background:none;border:1px solid var(--border);color:var(--text2);padding:6px 10px;border-radius:6px;cursor:pointer;font-size:0.9em;}
.mobile-menu-btn{display:none;background:none;border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:6px;cursor:pointer;font-size:1em;}

/* PAGE */
.page{padding:24px;}
.page-header{margin-bottom:24px;}
.page-header h1{font-size:1.5em;font-weight:700;}
.page-header p{color:var(--text2);font-size:0.9em;margin-top:4px;}
.breadcrumb{font-size:0.8em;color:var(--text2);margin-bottom:12px;}
.breadcrumb a{color:var(--text2);}
.breadcrumb span{color:var(--text);}

/* CARDS */
.card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px;}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;}
.card-title{font-size:0.95em;font-weight:600;}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px;}
.stat-card{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:16px;text-align:center;transition:border-color 0.2s;}
.stat-card:hover{border-color:var(--green);}
.stat-card .val{font-size:1.5em;font-weight:700;color:var(--green);}
.stat-card .lbl{font-size:0.78em;color:var(--text2);margin-top:4px;}

/* BLOCKS VISUAL */
.blocks-visual{display:flex;gap:8px;overflow-x:auto;padding:8px 0 16px;scrollbar-width:thin;}
.block-vis{min-width:80px;height:80px;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:transform 0.2s;text-align:center;padding:8px;text-decoration:none;}
.block-vis:hover{transform:translateY(-4px);text-decoration:none;}
.block-vis .bn{font-size:0.8em;font-weight:700;}
.block-vis .bi{font-size:1.2em;margin-bottom:2px;}
.block-vis .bt{font-size:0.6em;opacity:0.7;}

/* TABLE */
.table{width:100%;border-collapse:collapse;}
.table th{font-size:0.78em;font-weight:600;color:var(--text2);padding:8px 12px;border-bottom:1px solid var(--border);text-align:left;text-transform:uppercase;letter-spacing:0.5px;}
.table td{padding:12px;border-bottom:1px solid var(--border);font-size:0.875em;vertical-align:middle;}
.table tr:last-child td{border-bottom:none;}
.table tr:hover td{background:var(--bg3);}
.hash-link{font-family:monospace;color:var(--orange);font-size:0.85em;}
.hash-link:hover{color:var(--green);}
.tx-badge{font-size:0.7em;padding:2px 8px;border-radius:10px;font-weight:600;}
.tx-badge.in{background:rgba(0,255,136,0.1);color:var(--green);border:1px solid rgba(0,255,136,0.3);}
.tx-badge.out{background:rgba(248,81,73,0.1);color:var(--red);border:1px solid rgba(248,81,73,0.3);}
.tx-badge.confirmed{background:rgba(0,255,136,0.1);color:var(--green);border:1px solid rgba(0,255,136,0.3);}

/* DETAIL PAGE */
.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;}
.detail-item{padding:12px 0;border-bottom:1px solid var(--border);display:flex;gap:12px;}
.detail-item:last-child{border-bottom:none;}
.detail-label{font-size:0.8em;color:var(--text2);min-width:160px;flex-shrink:0;}
.detail-value{font-size:0.875em;word-break:break-all;}
.block-nav{display:flex;gap:8px;margin-bottom:16px;}
.block-nav a{padding:8px 16px;background:var(--bg2);border:1px solid var(--border);border-radius:6px;font-size:0.875em;color:var(--text);transition:all 0.2s;}
.block-nav a:hover{border-color:var(--green);color:var(--green);text-decoration:none;}

/* FORMS */
.form-section{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px;}
.form-section h3{font-size:1em;font-weight:600;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--border);}
.fg{margin-bottom:14px;}
.fg label{display:block;font-size:0.875em;font-weight:500;color:var(--text2);margin-bottom:6px;}
.fg input,.fg select,.fg textarea{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;transition:border-color 0.2s;}
.fg input:focus,.fg select:focus,.fg textarea:focus{border-color:var(--green);}
.input-wrap{position:relative;}
.input-wrap input{padding-right:44px;}
.eye-btn{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--text2);cursor:pointer;font-size:1em;}
.pwd-bar{height:4px;border-radius:2px;margin-top:6px;transition:all 0.3s;width:0%;}
.pwd-bar.weak{background:var(--red);width:33%;}
.pwd-bar.medium{background:var(--yellow);width:66%;}
.pwd-bar.strong{background:var(--green);width:100%;}
.pwd-hint{font-size:0.75em;color:var(--text2);margin-top:4px;}
.btn{padding:10px 20px;border-radius:8px;font-size:0.9em;font-weight:600;cursor:pointer;border:none;transition:all 0.2s;display:inline-block;text-align:center;}
.btn-primary{background:var(--green);color:#000;}
.btn-primary:hover{background:var(--green2);}
.btn-secondary{background:transparent;color:var(--text);border:1px solid var(--border);}
.btn-secondary:hover{background:var(--bg3);}
.btn-danger{background:transparent;color:var(--red);border:1px solid var(--red);}
.btn-danger:hover{background:var(--red);color:#fff;}
.btn-blue{background:var(--blue);color:#fff;}
.btn-purple{background:var(--purple);color:#fff;}
.btn-full{width:100%;display:block;}
.btn-sm{padding:6px 14px;font-size:0.8em;}

/* ALERTS */
.alert{padding:12px 16px;border-radius:8px;margin-bottom:16px;font-size:0.875em;}
.alert.error{background:rgba(248,81,73,0.1);border:1px solid var(--red);color:var(--red);}
.alert.success{background:rgba(0,255,136,0.1);border:1px solid var(--green);color:var(--green);}
.alert.info{background:rgba(88,166,255,0.1);border:1px solid var(--blue);color:var(--blue);}
.alert.warning{background:rgba(227,179,65,0.1);border:1px solid var(--yellow);color:var(--yellow);}

/* WALLET */
.balance-box{text-align:center;padding:28px;background:var(--bg);border-radius:12px;border:1px solid var(--border);margin-bottom:16px;}
.bal-label{font-size:0.85em;color:var(--text2);margin-bottom:8px;}
.bal-amount{font-size:2.8em;font-weight:700;color:var(--green);font-family:monospace;}
.bal-hidden{font-size:2.5em;letter-spacing:6px;color:var(--text2);}
.show-btn{background:none;border:1px solid var(--border);color:var(--text2);cursor:pointer;font-size:0.82em;padding:6px 14px;border-radius:6px;margin-top:8px;transition:all 0.2s;}
.show-btn:hover{border-color:var(--green);color:var(--green);}
.addr-box{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:12px 16px;font-family:monospace;font-size:0.82em;color:var(--orange);word-break:break-all;margin-bottom:8px;}
.copy-btn{background:var(--bg3);border:1px solid var(--border);color:var(--text2);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:0.78em;transition:all 0.2s;}
.copy-btn:hover{border-color:var(--green);color:var(--green);}
.qr-wrap{display:flex;justify-content:center;margin:16px auto;padding:16px;background:white;border-radius:10px;width:fit-content;}
.tx-preview{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px;display:none;}
.tx-preview.show{display:block;}
.tx-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);font-size:0.85em;}
.tx-row:last-child{border-bottom:none;}
.tx-item{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border);}
.tx-item:last-child{border-bottom:none;}
.tx-icon{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.tx-icon.in{background:rgba(0,255,136,0.15);color:var(--green);}
.tx-icon.out{background:rgba(248,81,73,0.15);color:var(--red);}
.tx-info{flex:1;min-width:0;}
.tx-amount{font-weight:700;white-space:nowrap;}
.tx-amount.in{color:var(--green);}
.tx-amount.out{color:var(--red);}

/* SETTINGS */
.settings-menu{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:16px;}
.settings-item{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:20px;display:flex;align-items:center;gap:14px;cursor:pointer;transition:all 0.2s;text-decoration:none;color:var(--text);}
.settings-item:hover{border-color:var(--green);transform:translateY(-2px);text-decoration:none;color:var(--text);}
.settings-item .si-icon{width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3em;flex-shrink:0;}
.settings-item .si-title{font-weight:600;font-size:0.9em;}
.settings-item .si-desc{font-size:0.78em;color:var(--text2);margin-top:2px;}
.setting-row{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--border);}
.setting-row:last-child{border-bottom:none;}
.setting-label{font-size:0.9em;font-weight:500;}
.setting-desc{font-size:0.78em;color:var(--text2);margin-top:2px;}
.toggle{position:relative;display:inline-block;width:44px;height:24px;flex-shrink:0;}
.toggle input{opacity:0;width:0;height:0;}
.toggle-slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:var(--bg3);border-radius:24px;transition:0.3s;border:1px solid var(--border);}
.toggle-slider:before{position:absolute;content:"";height:18px;width:18px;left:2px;bottom:2px;background:var(--text2);border-radius:50%;transition:0.3s;}
.toggle input:checked + .toggle-slider{background:var(--green);border-color:var(--green);}
.toggle input:checked + .toggle-slider:before{transform:translateX(20px);background:#000;}
.select-styled{padding:8px 12px;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:0.875em;outline:none;cursor:pointer;}

/* SECURITY SCORE */
.sec-score{display:flex;align-items:center;gap:16px;background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:16px;}
.score-ring{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1em;font-weight:700;flex-shrink:0;}
.score-low{background:rgba(248,81,73,0.15);border:2px solid var(--red);color:var(--red);}
.score-mid{background:rgba(227,179,65,0.15);border:2px solid var(--yellow);color:var(--yellow);}
.score-high{background:rgba(0,255,136,0.15);border:2px solid var(--green);color:var(--green);}

/* BADGES */
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.75em;font-weight:600;margin-left:6px;}
.badge-green{background:rgba(0,255,136,0.15);color:var(--green);border:1px solid var(--green);}
.badge-red{background:rgba(248,81,73,0.15);color:var(--red);border:1px solid var(--red);}
.badge-blue{background:rgba(88,166,255,0.15);color:var(--blue);border:1px solid var(--blue);}
.badge-purple{background:rgba(163,113,247,0.15);color:var(--purple);border:1px solid var(--purple);}
.badge-yellow{background:rgba(227,179,65,0.15);color:var(--yellow);border:1px solid var(--yellow);}

/* AUTH PAGES */
.auth-page{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;background:var(--bg);}
.auth-card{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:36px;width:100%;max-width:420px;}
.auth-card h2{font-size:1.4em;font-weight:700;margin-bottom:4px;}
.auth-card .sub{color:var(--text2);font-size:0.875em;margin-bottom:24px;}
.auth-logo{text-align:center;margin-bottom:24px;}
.auth-logo span{font-size:1.8em;font-weight:700;color:var(--green);}
.bonus-badge{background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.25);border-radius:8px;padding:10px;margin-bottom:20px;font-size:0.875em;color:var(--green);text-align:center;}
.recaptcha-wrap{display:flex;justify-content:center;margin:16px 0;transform:scale(0.9);transform-origin:center;}
.otp-input{font-size:2em;text-align:center;letter-spacing:12px;font-family:monospace;font-weight:700;}

/* PROFILE */
.profile-header{display:flex;align-items:center;gap:20px;margin-bottom:24px;}
.profile-avatar{width:72px;height:72px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2em;font-weight:700;color:#000;flex-shrink:0;}
.profile-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.profile-stat{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:14px;}
.ps-label{font-size:0.75em;color:var(--text2);margin-bottom:4px;}
.ps-value{font-size:0.95em;font-weight:600;}
.login-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);font-size:0.85em;}
.login-row:last-child{border-bottom:none;}

/* SEARCH */
.search-result{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:10px;display:flex;align-items:center;gap:16px;transition:border-color 0.2s;}
.search-result:hover{border-color:var(--green);}
.sr-icon{width:40px;height:40px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.2em;flex-shrink:0;}

/* NETWORK STATUS */
.network-pill{display:inline-flex;align-items:center;gap:6px;background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.3);border-radius:20px;padding:4px 12px;font-size:0.78em;color:var(--green);}
.pulse{width:7px;height:7px;background:var(--green);border-radius:50%;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}

/* BACKUP CODES */
.backup-code{font-family:monospace;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:8px 12px;font-size:0.9em;color:var(--green);display:inline-block;margin:4px;}

/* PROGRESS */
.progress-bar{background:var(--bg);border-radius:4px;height:8px;overflow:hidden;}
.progress-fill{background:var(--green);height:100%;border-radius:4px;transition:width 0.5s;}

/* MOBILE */
@media(max-width:768px){
  .sidebar{transform:translateX(-100%);transition:transform 0.3s;}
  .sidebar.open{transform:translateX(0);}
  .main-content{margin-left:0;}
  .mobile-menu-btn{display:block;}
  .detail-grid{grid-template-columns:1fr;}
  .profile-grid{grid-template-columns:1fr;}
  .stats-grid{grid-template-columns:repeat(2,1fr);}
  .settings-menu{grid-template-columns:1fr;}
  .block-row-grid{grid-template-columns:60px 1fr;}
}
.overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:150;}
.overlay.show{display:block;}
</style>
<script>
function toggleTheme(){document.body.classList.toggle('light');localStorage.setItem('nyn_theme',document.body.classList.contains('light')?'light':'dark');}
function togglePwd(id){var i=document.getElementById(id);i.type=i.type==='password'?'text':'password';}
function checkPwd(val,sid,hid){var s=document.getElementById(sid),h=document.getElementById(hid);if(!s)return;var sc=0;if(val.length>=8)sc++;if(val.length>=12)sc++;if(/[A-Z]/.test(val))sc++;if(/[a-z]/.test(val))sc++;if(/\d/.test(val))sc++;if(/[!@#$%^&*]/.test(val))sc++;if(sc<=2){s.className='pwd-bar weak';if(h)h.textContent='Weak';}else if(sc<=4){s.className='pwd-bar medium';if(h)h.textContent='Medium';}else{s.className='pwd-bar strong';if(h)h.textContent='Strong ✓';}}
function toggleSidebar(){var s=document.getElementById('sidebar'),o=document.getElementById('overlay');s.classList.toggle('open');o.classList.toggle('show');}
window.onload=function(){if(localStorage.getItem('nyn_theme')==='light')document.body.classList.add('light');}
</script>
"""

def sidebar_html(active="explorer", user=None, logged_in=False):
    u = user
    return f"""
<div class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <span>⚡ NYN</span>
    <div><small>NoyanCoin</small><small style="color:var(--green);font-size:0.65em;">● Testnet</small></div>
  </div>
  <nav class="sidebar-nav">
    <div class="sidebar-section">Blockchain</div>
    <a href="/" class="sidebar-item {'active' if active=='explorer' else ''}"><span class="icon">🏠</span> Explorer</a>
    <a href="/#blocks" class="sidebar-item {'active' if active=='blocks' else ''}"><span class="icon">📦</span> Blocks</a>
    <a href="/#transactions" class="sidebar-item {'active' if active=='txns' else ''}"><span class="icon">💸</span> Transactions</a>
    {"" if not logged_in else f'''
    <div class="sidebar-section">My Account</div>
    <a href="/wallet" class="sidebar-item {'active' if active=='wallet' else ''}"><span class="icon">👛</span> Wallet</a>
    <a href="/wallet#send" class="sidebar-item {'active' if active=='send' else ''}"><span class="icon">📤</span> Send NYN</a>
    <a href="/wallet#stake" class="sidebar-item {'active' if active=='stake' else ''}"><span class="icon">⛏</span> Staking</a>
    <a href="/wallet#referral" class="sidebar-item {'active' if active=='referral' else ''}"><span class="icon">🎁</span> Referral</a>
    <div class="sidebar-section">Account</div>
    <a href="/profile" class="sidebar-item {'active' if active=='profile' else ''}"><span class="icon">👤</span> Profile</a>
    <a href="/settings" class="sidebar-item {'active' if active=='settings' else ''}"><span class="icon">⚙️</span> Settings</a>
    '''}
  </nav>
  {"" if not logged_in else f'''
  <div class="sidebar-bottom">
    <div class="sidebar-user">
      <div class="sidebar-avatar">{u.username[0].upper() if u else "?"}</div>
      <div style="flex:1;min-width:0;">
        <div style="font-size:0.85em;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{u.username if u else ""}</div>
        <a href="/logout" style="font-size:0.75em;color:var(--red);">Logout</a>
      </div>
    </div>
  </div>
  '''}
</div>
<div class="overlay" id="overlay" onclick="toggleSidebar()"></div>
"""

def topbar_html(logged_in=False):
    return f"""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:12px;flex:1;">
    <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
    <div class="topbar-search">
      <input type="text" id="search-input" placeholder="Search blocks, transactions, addresses...">
      <button onclick="window.location.href='/search?q='+document.getElementById('search-input').value">Search</button>
    </div>
  </div>
  <div class="topbar-right">
    <span class="network-pill"><span class="pulse"></span> Live</span>
    <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    {"<a href='/wallet' style='padding:6px 14px;background:var(--green);color:#000;border-radius:6px;font-size:0.875em;font-weight:600;text-decoration:none;'>My Wallet</a>" if logged_in else "<a href='/register' style='padding:6px 14px;background:var(--green);color:#000;border-radius:6px;font-size:0.875em;font-weight:600;text-decoration:none;'>Get Wallet</a><a href='/login' style='padding:6px 14px;border:1px solid var(--border);color:var(--text);border-radius:6px;font-size:0.875em;margin-left:6px;'>Login</a>"}
  </div>
</div>
"""

MAIN_HTML = """<!DOCTYPE html><html><head><title>NYN Explorer - NoyanCoin Blockchain</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="page-header">
    <h1>⚡ NYN Blockchain Explorer</h1>
    <p>Republic of Nowhere — Private. Human. Borderless. Powered by Proof of Stake.</p>
  </div>

  <div class="stats-grid">
    <div class="stat-card"><div class="val">{{ blocks }}</div><div class="lbl">Total Blocks</div></div>
    <div class="stat-card"><div class="val">24,000,000</div><div class="lbl">Max Supply (NYN)</div></div>
    <div class="stat-card"><div class="val">{{ circulating }}</div><div class="lbl">Circulating Supply</div></div>
    <div class="stat-card"><div class="val">{{ users }}</div><div class="lbl">Total Wallets</div></div>
    <div class="stat-card"><div class="val">{{ txns }}</div><div class="lbl">Transactions</div></div>
    <div class="stat-card"><div class="val">{{ total_staked }} NYN</div><div class="lbl">Total Staked</div></div>
    <div class="stat-card"><div class="val">~2s</div><div class="lbl">Block Time</div></div>
    <div class="stat-card"><div class="val">PoS</div><div class="lbl">Consensus</div></div>
  </div>

  <div class="card">
    <div class="card-header"><div class="card-title">📊 Network Info</div><span class="network-pill"><span class="pulse"></span> Active</span></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;">
      <div style="padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);"><div style="font-size:0.75em;color:var(--text2);">Algorithm</div><div style="font-weight:600;color:var(--purple);margin-top:4px;">Proof of Stake</div></div>
      <div style="padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);"><div style="font-size:0.75em;color:var(--text2);">Genesis Block</div><div style="font-weight:600;margin-top:4px;">{{ genesis_date }}</div></div>
      <div style="padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);"><div style="font-size:0.75em;color:var(--text2);">Privacy</div><div style="font-weight:600;color:var(--green);margin-top:4px;">Balance Hidden ✓</div></div>
      <div style="padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);"><div style="font-size:0.75em;color:var(--text2);">Human Verified</div><div style="font-weight:600;color:var(--green);margin-top:4px;">Required ✓</div></div>
      <div style="padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);"><div style="font-size:0.75em;color:var(--text2);">Security</div><div style="font-weight:600;color:var(--green);margin-top:4px;">2FA + TX PIN ✓</div></div>
      <div style="padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);"><div style="font-size:0.75em;color:var(--text2);">Network</div><div style="font-weight:600;color:var(--orange);margin-top:4px;">Testnet</div></div>
    </div>
  </div>

  <div class="card" id="blocks">
    <div class="card-header"><div class="card-title">🔲 Latest Blocks</div><a href="/#blocks" style="font-size:0.8em;color:var(--text2);">View all</a></div>
    <div class="blocks-visual">
      {% set colors = ['#a371f7','#58a6ff','#00ff88','#f0883e','#e3b341','#f85149','#3fb950','#79c0ff'] %}
      {% for block in chain[-10:]|reverse %}
      {% set color = colors[block.index % 8] %}
      <a href="/block/{{ block.index }}" class="block-vis" style="background:{{ color }}18;border:2px solid {{ color }}40;">
        <span class="bi" style="color:{{ color }};">⬡</span>
        <span class="bn" style="color:{{ color }};">#{{ block.index }}</span>
        <span class="bt" style="color:{{ color }};">{{ block.tx_count }} tx</span>
      </a>
      {% endfor %}
    </div>
    <table class="table">
      <thead><tr><th>Block</th><th>Hash</th><th>Validator</th><th>Txns</th><th>Size</th></tr></thead>
      <tbody>
        {% for block in chain[-10:]|reverse %}
        <tr>
          <td><a href="/block/{{ block.index }}" class="hash-link">#{{ block.index }}</a></td>
          <td><a href="/block/{{ block.index }}" class="hash-link">{{ block.hash[:16] }}...{{ block.hash[-8:] }}</a></td>
          <td style="font-size:0.8em;color:var(--text2);">{{ block.validator[:20] if block.validator else 'System' }}</td>
          <td><span style="color:var(--purple);">{{ block.tx_count }}</span></td>
          <td style="color:var(--text2);">{{ block.size }} B</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="card" id="transactions">
    <div class="card-header"><div class="card-title">💸 Recent Transactions</div></div>
    {% if recent_txns %}
    <table class="table">
      <thead><tr><th>TX Hash</th><th>From</th><th>To</th><th>Amount</th><th>Time</th></tr></thead>
      <tbody>
        {% for tx in recent_txns %}
        <tr>
          <td><a href="/tx/{{ tx.hash }}" class="hash-link">{{ tx.hash[:16] }}...</a></td>
          <td style="font-family:monospace;font-size:0.78em;color:var(--text2);">{{ tx.sender }}</td>
          <td style="font-family:monospace;font-size:0.78em;color:var(--text2);">{{ tx.receiver }}</td>
          <td style="color:var(--green);font-weight:600;">{{ tx.amount }} NYN</td>
          <td style="color:var(--text2);font-size:0.8em;">{{ tx.time }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <p style="color:var(--text2);text-align:center;padding:24px;">No transactions yet.</p>
    {% endif %}
  </div>
</div>
</div>
</body></html>"""

BLOCK_DETAIL_HTML = """<!DOCTYPE html><html><head><title>Block #{{ block.index }} - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/">Explorer</a> › <a href="/#blocks">Blocks</a> › <span>Block #{{ block.index }}</span></div>
  <div class="page-header">
    <h1>Block #{{ block.index }}</h1>
    <p>{{ block_time }}</p>
  </div>

  <div class="block-nav">
    {% if prev_block %}<a href="/block/{{ prev_block.index }}">← Block #{{ prev_block.index }}</a>{% endif %}
    {% if next_block %}<a href="/block/{{ next_block.index }}">Block #{{ next_block.index }} →</a>{% endif %}
  </div>

  <div class="card">
    <div class="card-header"><div class="card-title">📦 Block Details</div><span class="tx-badge confirmed">✓ Confirmed</span></div>
    <div class="detail-item"><div class="detail-label">Block Height</div><div class="detail-value" style="font-family:monospace;">#{{ block.index }}</div></div>
    <div class="detail-item"><div class="detail-label">Hash</div><div class="detail-value" style="font-family:monospace;color:var(--orange);">{{ block.hash }}</div></div>
    <div class="detail-item"><div class="detail-label">Previous Hash</div><div class="detail-value" style="font-family:monospace;color:var(--text2);">{{ block.previous_hash }}</div></div>
    <div class="detail-item"><div class="detail-label">Timestamp</div><div class="detail-value">{{ block_time }}</div></div>
    <div class="detail-item"><div class="detail-label">Validator</div><div class="detail-value" style="color:var(--purple);">{{ block.validator }}</div></div>
    <div class="detail-item"><div class="detail-label">Transactions</div><div class="detail-value">{{ block.tx_count }}</div></div>
    <div class="detail-item"><div class="detail-label">Size</div><div class="detail-value">{{ block.size }} bytes</div></div>
    <div class="detail-item"><div class="detail-label">Consensus</div><div class="detail-value" style="color:var(--green);">Proof of Stake ✓</div></div>
    <div class="detail-item"><div class="detail-label">Data</div><div class="detail-value" style="font-family:monospace;font-size:0.8em;color:var(--text2);">{{ tx_data }}</div></div>
  </div>

  {% if txns %}
  <div class="card">
    <div class="card-header"><div class="card-title">💸 Transactions in this Block ({{ txns|length }})</div></div>
    <table class="table">
      <thead><tr><th>TX Hash</th><th>From</th><th>To</th><th>Amount</th><th>Status</th></tr></thead>
      <tbody>
        {% for tx in txns %}
        <tr>
          <td><a href="/tx/{{ tx.hash }}" class="hash-link">{{ tx.hash[:20] }}...</a></td>
          <td><a href="/address/{{ tx.sender }}" class="hash-link">{{ tx.sender[:16] }}...</a></td>
          <td><a href="/address/{{ tx.receiver }}" class="hash-link">{{ tx.receiver[:16] }}...</a></td>
          <td style="color:var(--green);font-weight:600;">{{ tx.amount }} NYN</td>
          <td><span class="tx-badge confirmed">✓ {{ tx.status }}</span></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% endif %}
</div>
</div>
</body></html>"""

TX_DETAIL_HTML = """<!DOCTYPE html><html><head><title>Transaction - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/">Explorer</a> › <a href="/#transactions">Transactions</a> › <span>{{ tx.tx_hash[:20] }}...</span></div>
  <div class="page-header">
    <h1>Transaction Details</h1>
    <p>{{ tx_time }}</p>
  </div>

  <div class="card">
    <div class="card-header"><div class="card-title">💸 Transaction Info</div><span class="tx-badge confirmed">✓ Confirmed</span></div>
    <div class="detail-item"><div class="detail-label">Transaction Hash</div><div class="detail-value" style="font-family:monospace;color:var(--orange);">{{ tx.tx_hash }}</div></div>
    <div class="detail-item"><div class="detail-label">Status</div><div class="detail-value" style="color:var(--green);">✓ Confirmed</div></div>
    <div class="detail-item"><div class="detail-label">Block</div><div class="detail-value"><a href="/block/{{ tx.block_index }}" style="color:var(--green);">#{{ tx.block_index }}</a></div></div>
    <div class="detail-item"><div class="detail-label">Timestamp</div><div class="detail-value">{{ tx_time }}</div></div>
    <div class="detail-item"><div class="detail-label">From</div><div class="detail-value"><a href="/address/{{ tx.sender }}" class="hash-link">{{ tx.sender }}</a></div></div>
    <div class="detail-item"><div class="detail-label">To</div><div class="detail-value"><a href="/address/{{ tx.receiver }}" class="hash-link">{{ tx.receiver }}</a></div></div>
    <div class="detail-item"><div class="detail-label">Amount</div><div class="detail-value" style="font-size:1.2em;font-weight:700;color:var(--green);">{{ tx.amount }} NYN</div></div>
    <div class="detail-item"><div class="detail-label">Network Fee</div><div class="detail-value" style="color:var(--green);">0 NYN (Free)</div></div>
    <div class="detail-item"><div class="detail-label">Consensus</div><div class="detail-value" style="color:var(--purple);">Proof of Stake ✓</div></div>
    {% if block %}<div class="detail-item"><div class="detail-label">Validated by</div><div class="detail-value" style="color:var(--purple);">{{ block.validator }}</div></div>{% endif %}
  </div>
</div>
</div>
</body></html>"""

ADDRESS_HTML = """<!DOCTYPE html><html><head><title>Address - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/">Explorer</a> › <span>Address</span></div>
  <div class="page-header">
    <h1>Wallet Address</h1>
    <p style="font-family:monospace;font-size:0.85em;color:var(--orange);">{{ address }}</p>
  </div>
  {% if wallet %}
  <div class="card">
    <div class="card-header"><div class="card-title">👤 Wallet Info</div>
      <span class="tx-badge {{ 'confirmed' if wallet.is_verified else 'out' }}">{{ '✓ Verified' if wallet.is_verified else '✗ Unverified' }}</span>
    </div>
    <div class="detail-item"><div class="detail-label">Address</div><div class="detail-value" style="font-family:monospace;color:var(--orange);">{{ address }}</div></div>
    <div class="detail-item"><div class="detail-label">Balance</div><div class="detail-value" style="color:var(--blue);">🔒 Private (NYN Privacy)</div></div>
    <div class="detail-item"><div class="detail-label">Total Transactions</div><div class="detail-value">{{ txns|length }}</div></div>
    <div class="detail-item"><div class="detail-label">Member Since</div><div class="detail-value">{{ wallet.created_at }}</div></div>
  </div>
  {% else %}
  <div class="alert info">This address has no registered wallet but may have received transactions.</div>
  {% endif %}

  <div class="card">
    <div class="card-header"><div class="card-title">💸 Transactions ({{ txns|length }})</div></div>
    {% if txns %}
    <table class="table">
      <thead><tr><th>Hash</th><th>Type</th><th>Address</th><th>Amount</th><th>Time</th></tr></thead>
      <tbody>
        {% for tx in txns %}
        <tr>
          <td><a href="/tx/{{ tx.hash }}" class="hash-link">{{ tx.hash[:16] }}...</a></td>
          <td><span class="tx-badge {{ tx.type }}">{{ '↓ IN' if tx.type == 'in' else '↑ OUT' }}</span></td>
          <td><a href="/address/{{ tx.sender if tx.type == 'in' else tx.receiver }}" class="hash-link">{{ (tx.sender if tx.type == 'in' else tx.receiver)[:20] }}...</a></td>
          <td class="tx-amount {{ tx.type }}">{{ '+' if tx.type == 'in' else '-' }}{{ tx.amount }} NYN</td>
          <td style="color:var(--text2);font-size:0.8em;">{{ tx.time }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <p style="color:var(--text2);text-align:center;padding:24px;">No transactions found.</p>
    {% endif %}
  </div>
</div>
</div>
</body></html>"""

SEARCH_HTML = """<!DOCTYPE html><html><head><title>Search - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="page-header"><h1>Search Results</h1><p>Results for: "{{ query }}"</p></div>
  {% if results %}
  {% for r in results %}
  <a href="{{ r.url }}" class="search-result" style="text-decoration:none;display:flex;">
    <div class="sr-icon" style="background:{% if r.type == 'block' %}rgba(163,113,247,0.15){% elif r.type == 'transaction' %}rgba(0,255,136,0.15){% else %}rgba(88,166,255,0.15){% endif %};">
      {{ '📦' if r.type == 'block' else '💸' if r.type == 'transaction' else '👛' }}
    </div>
    <div>
      <div style="font-weight:600;text-transform:capitalize;">{{ r.type }}</div>
      <div style="font-family:monospace;font-size:0.8em;color:var(--text2);">
        {% if r.type == 'block' %}#{{ r.data.index }} — {{ r.data.hash[:32] }}...
        {% elif r.type == 'transaction' %}{{ r.data.tx_hash[:32] }}...
        {% else %}{{ r.data.wallet_address[:32] }}...{% endif %}
      </div>
    </div>
  </a>
  {% endfor %}
  {% else %}
  <div class="card" style="text-align:center;padding:40px;">
    <div style="font-size:2em;margin-bottom:12px;">🔍</div>
    <div style="font-weight:600;margin-bottom:8px;">No results found</div>
    <div style="color:var(--text2);font-size:0.9em;">Try searching for a block number, transaction hash, or wallet address</div>
  </div>
  {% endif %}
</div>
</div>
</body></html>"""

WALLET_HTML = """<!DOCTYPE html><html><head><title>My Wallet - NYN</title>""" + STYLES + """
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  {% if msg %}<div class="alert {{ msg_type }}" style="margin-bottom:16px;">{{ msg }}</div>{% endif %}

  <div class="page-header">
    <h1>👛 My Wallet</h1>
    <p>{{ user.username }} — <span class="badge {{ 'badge-green' if user.is_verified else 'badge-red' }}">{{ '✓ Verified' if user.is_verified else '✗ Unverified' }}</span>
    {% if user.staked_amount >= 10 %}<span class="badge badge-purple">⛏ Validator</span>{% endif %}
    {% if user.two_fa_enabled %}<span class="badge badge-blue">🔐 2FA</span>{% endif %}
    </p>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;">
    <div class="balance-box">
      <div class="bal-label">Your Balance (Private)</div>
      <div id="bal" class="bal-hidden">••••••</div>
      <button class="show-btn" onclick="toggleBal()">👁 Show / Hide</button>
      <div style="background:rgba(88,166,255,0.08);border:1px solid rgba(88,166,255,0.25);border-radius:8px;padding:8px;font-size:0.78em;color:var(--blue);margin-top:8px;">🔒 Only you can see your balance</div>
    </div>
    <div class="card" style="margin:0;">
      <div style="font-size:0.8em;color:var(--text2);margin-bottom:6px;">Wallet Address</div>
      <div class="addr-box">{{ user.wallet_address }}</div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ user.wallet_address }}');this.textContent='✓ Copied!'">📋 Copy Address</button>
      <div class="qr-wrap"><div id="qrcode"></div></div>
    </div>
  </div>

  {% if not user.is_verified %}
  <div class="alert error">⚠️ Email not verified. <a href="/verify">Verify now</a> to unlock all features.</div>
  {% endif %}

  <div class="card" id="send">
    <div class="card-header"><div class="card-title">💸 Send NYN</div><span style="font-size:0.78em;color:var(--green);">Zero fees • PoS verified</span></div>
    <div class="alert info" style="margin-bottom:12px;">🔐 All transfers are verified by Proof of Stake consensus. 30s cooldown between transactions.</div>
    <input type="text" class="fg" id="recv" style="width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;margin-bottom:10px;" placeholder="Receiver wallet address (NYN...)" oninput="preview()">
    <input type="number" class="fg" id="amt" style="width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;margin-bottom:10px;" placeholder="Amount in NYN (max 10,000 per tx)" step="0.01" min="0.01" max="10000" oninput="preview()">
    {% if user.tx_pin_enabled %}<input type="password" id="txpin" style="width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;margin-bottom:10px;" placeholder="6-digit Transaction PIN">{% endif %}
    <div class="tx-preview" id="prev">
      <div style="font-weight:600;margin-bottom:10px;font-size:0.875em;">📋 Transaction Preview</div>
      <div class="tx-row"><span style="color:var(--text2);">From</span><span style="font-family:monospace;font-size:0.8em;">{{ user.wallet_address[:24] }}...</span></div>
      <div class="tx-row"><span style="color:var(--text2);">To</span><span id="p-to" style="font-family:monospace;font-size:0.8em;">-</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Amount</span><span id="p-amt" style="color:var(--green);font-weight:700;">-</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Fee</span><span style="color:var(--green);">0 NYN</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Consensus</span><span style="color:var(--purple);">Proof of Stake ✓</span></div>
    </div>
    <form method="POST" action="/send" id="sf">
      <input type="hidden" name="receiver" id="rh">
      <input type="hidden" name="amount" id="ah">
      <input type="hidden" name="tx_pin" id="ph">
      <button type="button" class="btn btn-primary btn-full" onclick="doSend()" style="margin-top:8px;">Confirm & Send NYN ⚡</button>
    </form>
  </div>

  <div class="card" id="stake">
    <div class="card-header"><div class="card-title">⛏ Staking</div><span style="font-size:0.78em;color:var(--purple);">Earn 0.1 NYN/block</span></div>
    <div class="alert info" style="margin-bottom:12px;">Stake NYN to become a validator. Min 10 NYN. 24hr lock period.</div>
    {% if stake_info %}
    <div style="background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:12px;">
      <div class="tx-row"><span style="color:var(--text2);">Staked Since</span><span>{{ stake_info.staked_at }}</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Amount</span><span style="color:var(--green);font-weight:700;">{{ stake_info.amount }} NYN</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Rewards</span><span style="color:var(--yellow);">{{ stake_info.rewards }} NYN</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Blocks Validated</span><span style="color:var(--purple);">{{ user.blocks_validated }}</span></div>
      <div class="tx-row"><span style="color:var(--text2);">Status</span><span style="color:var(--green);">✓ Active Validator</span></div>
    </div>
    <form method="POST" action="/unstake"><button type="submit" class="btn btn-danger btn-full">Unstake NYN</button></form>
    {% else %}
    <form method="POST" action="/stake">
      <input type="number" name="amount" style="width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95em;outline:none;margin-bottom:10px;" placeholder="Amount to stake (min 10 NYN)" min="10" step="0.01" required>
      <button type="submit" class="btn btn-purple btn-full">Stake & Become Validator ⛏</button>
    </form>
    {% endif %}
  </div>

  <div class="card" id="referral">
    <div class="card-header"><div class="card-title">🎁 Referral Program</div></div>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:14px;">Earn 20 NYN per referral. Max 3 referrals.</p>
    <div style="font-size:1.5em;font-weight:700;color:var(--green);font-family:monospace;letter-spacing:3px;margin-bottom:8px;">{{ user.referral_code }}</div>
    <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ user.referral_code }}');this.textContent='✓ Copied!'">📋 Copy Code</button>
    <div style="margin-top:12px;">
      <div style="font-size:0.85em;color:var(--text2);margin-bottom:4px;">Referrals: {{ user.referral_count }}/3</div>
      <div class="progress-bar"><div class="progress-fill" style="width:{{ (user.referral_count/3*100)|int }}%"></div></div>
    </div>
  </div>

  <div class="card">
    <div class="card-header"><div class="card-title">📋 Transaction History</div></div>
    {% if transactions %}
    <table class="table">
      <thead><tr><th>Type</th><th>Address</th><th>Amount</th><th>Time</th><th>Hash</th></tr></thead>
      <tbody>
        {% for tx in transactions %}
        <tr>
          <td><span class="tx-badge {{ tx.type }}">{{ '↓ IN' if tx.type == 'in' else '↑ OUT' }}</span></td>
          <td><a href="/address/{{ tx.sender if tx.type == 'in' else tx.receiver }}" class="hash-link">{{ (tx.sender if tx.type == 'in' else tx.receiver)[:20] }}...</a></td>
          <td class="tx-amount {{ tx.type }}">{{ '+' if tx.type == 'in' else '-' }}{{ tx.amount }} NYN</td>
          <td style="color:var(--text2);font-size:0.8em;">{{ tx.time }}</td>
          <td><a href="/tx/{{ tx.hash }}" class="hash-link">{{ tx.hash[:12] }}...</a></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <p style="color:var(--text2);text-align:center;padding:24px;">No transactions yet.</p>
    {% endif %}
  </div>
</div>
</div>
<script>
var bv=false,rb="{{ user.balance }} NYN";
function toggleBal(){bv=!bv;var e=document.getElementById('bal');e.className=bv?'bal-amount':'bal-hidden';e.textContent=bv?rb:'••••••';}
function preview(){var r=document.getElementById('recv').value,a=document.getElementById('amt').value,b=document.getElementById('prev');if(r.length>5&&a>0){document.getElementById('p-to').textContent=r.substring(0,24)+'...';document.getElementById('p-amt').textContent=a+' NYN';b.classList.add('show');}else b.classList.remove('show');}
function doSend(){var r=document.getElementById('recv').value,a=document.getElementById('amt').value;if(!r||!a){alert('Fill receiver and amount');return;}if(!r.startsWith('NYN')){alert('Invalid NYN address - must start with NYN');return;}if(r.length!==35){alert('Invalid address length');return;}if(parseFloat(a)>10000){alert('Max 10,000 NYN per transaction');return;}{% if user.tx_pin_enabled %}var p=document.getElementById('txpin').value;if(!p||p.length!==6){alert('Enter your 6-digit TX PIN');return;}document.getElementById('ph').value=p;{% endif %}if(confirm('Send '+a+' NYN to '+r.substring(0,20)+'...?\n\nThis cannot be undone.')){document.getElementById('rh').value=r;document.getElementById('ah').value=a;document.getElementById('sf').submit();}}
new QRCode(document.getElementById("qrcode"),{text:"{{ user.wallet_address }}",width:120,height:120,colorDark:"#000",colorLight:"#fff"});
</script>
</body></html>"""

PROFILE_HTML = """<!DOCTYPE html><html><head><title>Profile - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>👤 Profile</h1></div>
  <div class="card">
    <div class="profile-header">
      <div class="profile-avatar">{{ user.username[0].upper() }}</div>
      <div>
        <div style="font-size:1.3em;font-weight:700;">{{ user.username }}
          <span class="badge {{ 'badge-green' if user.is_verified else 'badge-red' }}">{{ '✓ Verified' if user.is_verified else '✗ Unverified' }}</span>
          {% if user.two_fa_enabled %}<span class="badge badge-blue">🔐 2FA</span>{% endif %}
        </div>
        <div style="color:var(--text2);font-size:0.875em;margin-top:4px;">{{ user.email }}</div>
        <div style="color:var(--text2);font-size:0.85em;">Member since {{ created_at }}</div>
        <div style="margin-top:8px;"><a href="/address/{{ user.wallet_address }}" class="hash-link" style="font-size:0.8em;">{{ user.wallet_address[:24] }}...</a></div>
      </div>
    </div>
    <div class="profile-grid">
      <div class="profile-stat"><div class="ps-label">Total Sent</div><div class="ps-value" style="color:var(--red);">{{ user.total_sent|round(2) }} NYN</div></div>
      <div class="profile-stat"><div class="ps-label">Total Received</div><div class="ps-value" style="color:var(--green);">{{ user.total_received|round(2) }} NYN</div></div>
      <div class="profile-stat"><div class="ps-label">Blocks Validated</div><div class="ps-value" style="color:var(--purple);">{{ user.blocks_validated }}</div></div>
      <div class="profile-stat"><div class="ps-label">Referrals Made</div><div class="ps-value">{{ user.referral_count }}/3</div></div>
      <div class="profile-stat"><div class="ps-label">Staked Amount</div><div class="ps-value" style="color:var(--yellow);">{{ user.staked_amount }} NYN</div></div>
      <div class="profile-stat"><div class="ps-label">Login Count</div><div class="ps-value">{{ user.login_count }}</div></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title" style="margin-bottom:16px;">🔐 Recent Login Activity</div>
    {% for l in logins %}
    <div class="login-row">
      <span style="font-family:monospace;font-size:0.85em;">{{ l.ip }}</span>
      <span style="font-size:0.8em;color:var(--text2);">{{ l.agent }}</span>
      <span style="font-size:0.8em;color:var(--text2);">{{ l.time }}</span>
      <span style="color:{{ 'var(--green)' if l.success else 'var(--red)' }};font-size:0.8em;">{{ '✓' if l.success else '✗' }}</span>
    </div>
    {% endfor %}
  </div>
  <div class="card" style="border-color:var(--red);">
    <div class="card-title" style="color:var(--red);margin-bottom:12px;">⚠️ Danger Zone</div>
    <button onclick="alert('Contact @OfficiaNowhere for account deletion')" class="btn btn-danger">Delete Account</button>
  </div>
</div>
</div>
</body></html>"""

SETTINGS_HOME_HTML = """<!DOCTYPE html><html><head><title>Settings - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>⚙️ Settings</h1><p>Manage your account preferences and security</p></div>

  {% set sec_score = (1 if user.is_verified else 0) + (2 if user.two_fa_enabled else 0) + (1 if user.tx_pin_enabled else 0) + (1 if user.notif_security else 0) %}
  <div class="sec-score">
    <div class="score-ring {{ 'score-high' if sec_score >= 4 else 'score-mid' if sec_score >= 2 else 'score-low' }}">{{ sec_score }}/5</div>
    <div>
      <div style="font-weight:600;margin-bottom:4px;">Security Score</div>
      <div style="font-size:0.85em;color:var(--text2);">{{ 'Excellent security!' if sec_score >= 4 else 'Enable 2FA and TX PIN for better security.' if sec_score >= 2 else 'Please enable security features.' }}</div>
    </div>
  </div>

  <div class="settings-menu">
    <a href="/settings/appearance" class="settings-item">
      <div class="si-icon" style="background:rgba(163,113,247,0.15);">🎨</div>
      <div><div class="si-title">Appearance</div><div class="si-desc">Theme, language</div></div>
    </a>
    <a href="/settings/security" class="settings-item">
      <div class="si-icon" style="background:rgba(248,81,73,0.15);">🛡️</div>
      <div><div class="si-title">Security</div><div class="si-desc">Password, 2FA</div></div>
    </a>
    <a href="/settings/tx-pin" class="settings-item">
      <div class="si-icon" style="background:rgba(0,255,136,0.15);">🔑</div>
      <div><div class="si-title">Transaction PIN</div><div class="si-desc">Set, change, reset PIN</div></div>
    </a>
    <a href="/settings/privacy" class="settings-item">
      <div class="si-icon" style="background:rgba(88,166,255,0.15);">🔒</div>
      <div><div class="si-title">Privacy</div><div class="si-desc">Balance, transactions</div></div>
    </a>
    <a href="/settings/notifications" class="settings-item">
      <div class="si-icon" style="background:rgba(227,179,65,0.15);">🔔</div>
      <div><div class="si-title">Notifications</div><div class="si-desc">Email alerts</div></div>
    </a>
    <a href="/profile" class="settings-item">
      <div class="si-icon" style="background:rgba(0,255,136,0.15);">👤</div>
      <div><div class="si-title">Profile</div><div class="si-desc">View profile & activity</div></div>
    </a>
  </div>
</div>
</div>
</body></html>"""

SETTINGS_APPEARANCE_HTML = """<!DOCTYPE html><html><head><title>Appearance - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/settings">Settings</a> › <span>Appearance</span></div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>🎨 Appearance</h1></div>
  <div class="form-section">
    <h3>Theme & Language</h3>
    <form method="POST">
      <div class="setting-row">
        <div><div class="setting-label">Color Theme</div><div class="setting-desc">Choose dark or light mode</div></div>
        <select name="theme" class="select-styled" onchange="localStorage.setItem('nyn_theme',this.value);if(this.value==='light')document.body.classList.add('light');else document.body.classList.remove('light');">
          <option value="dark" {{ 'selected' if user.theme == 'dark' else '' }}>🌙 Dark</option>
          <option value="light" {{ 'selected' if user.theme == 'light' else '' }}>☀️ Light</option>
        </select>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Language</div><div class="setting-desc">Interface language</div></div>
        <select name="language" class="select-styled">
          <option value="en" {{ 'selected' if user.language == 'en' else '' }}>🇬🇧 English</option>
          <option value="hi" {{ 'selected' if user.language == 'hi' else '' }}>🇮🇳 Hindi</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary" style="margin-top:16px;">Save Changes</button>
    </form>
  </div>
</div>
</div>
</body></html>"""

SETTINGS_SECURITY_HTML = """<!DOCTYPE html><html><head><title>Security - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/settings">Settings</a> › <span>Security</span></div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>🛡️ Security</h1></div>

  <div class="form-section">
    <h3>🔐 Two-Factor Authentication (2FA)</h3>
    {% if user.two_fa_enabled %}
    <div class="alert success" style="margin-bottom:16px;">✓ 2FA is active. Your account is protected.</div>
    <form method="POST" action="/disable-2fa">
      <div class="fg"><label>Enter Password to Disable 2FA</label>
        <div class="input-wrap"><input type="password" name="password" id="d2fa" placeholder="Current password" required><button type="button" class="eye-btn" onclick="togglePwd('d2fa')">👁</button></div>
      </div>
      <button type="submit" class="btn btn-danger">Disable 2FA</button>
    </form>
    {% else %}
    <div class="alert warning" style="margin-bottom:16px;">⚠️ 2FA not enabled. Enable it for better security.</div>
    <a href="/setup-2fa" class="btn btn-blue">Enable 2FA with Google Authenticator 🔐</a>
    {% endif %}
  </div>

  <div class="form-section">
    <h3>🔑 Change Password</h3>
    <form method="POST" action="/settings/change-password">
      <div class="fg"><label>Current Password</label>
        <div class="input-wrap"><input type="password" name="current_password" id="cp1" placeholder="Current password" required><button type="button" class="eye-btn" onclick="togglePwd('cp1')">👁</button></div>
      </div>
      <div class="fg"><label>New Password</label>
        <div class="input-wrap"><input type="password" name="new_password" id="cp2" placeholder="New password (min 8 chars)" required minlength="8" oninput="checkPwd(this.value,'pwd-bar','pwd-hint')"><button type="button" class="eye-btn" onclick="togglePwd('cp2')">👁</button></div>
        <div class="pwd-bar" id="pwd-bar"></div>
        <div class="pwd-hint" id="pwd-hint"></div>
      </div>
      <div class="fg"><label>Confirm New Password</label>
        <div class="input-wrap"><input type="password" name="confirm_password" id="cp3" placeholder="Confirm new password" required><button type="button" class="eye-btn" onclick="togglePwd('cp3')">👁</button></div>
      </div>
      <button type="submit" class="btn btn-primary">Update Password</button>
    </form>
  </div>
</div>
</div>
</body></html>"""

SETTINGS_TX_PIN_HTML = """<!DOCTYPE html><html><head><title>Transaction PIN - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/settings">Settings</a> › <span>Transaction PIN</span></div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>🔑 Transaction PIN</h1><p>Secure your transfers with a 6-digit PIN</p></div>

  {% if not user.tx_pin_enabled %}
  <div class="form-section">
    <h3>Set Transaction PIN</h3>
    <div class="alert info" style="margin-bottom:16px;">A 6-digit PIN will be required before every NYN transfer.</div>
    <form method="POST">
      <input type="hidden" name="action" value="set">
      <div class="fg"><label>6-Digit PIN</label><input type="password" name="tx_pin" placeholder="Enter 6-digit PIN" maxlength="6" pattern="[0-9]{6}" required></div>
      <button type="submit" class="btn btn-primary">Set Transaction PIN</button>
    </form>
  </div>
  {% else %}
  <div class="alert success" style="margin-bottom:16px;">✓ Transaction PIN is active.</div>

  <div class="form-section">
    <h3>Change PIN</h3>
    <form method="POST">
      <input type="hidden" name="action" value="change">
      <div class="fg"><label>Current PIN</label><input type="password" name="old_pin" placeholder="Current 6-digit PIN" maxlength="6" required></div>
      <div class="fg"><label>New PIN</label><input type="password" name="new_pin" placeholder="New 6-digit PIN" maxlength="6" required></div>
      <button type="submit" class="btn btn-primary">Change PIN</button>
    </form>
  </div>

  <div class="form-section">
    <h3>Reset PIN</h3>
    <p style="color:var(--text2);font-size:0.875em;margin-bottom:12px;">Forgot your PIN? Reset it using your account password.</p>
    <form method="POST">
      <input type="hidden" name="action" value="reset">
      <div class="fg"><label>Account Password</label>
        <div class="input-wrap"><input type="password" name="password" id="rp" placeholder="Account password" required><button type="button" class="eye-btn" onclick="togglePwd('rp')">👁</button></div>
      </div>
      <button type="submit" class="btn btn-secondary">Reset PIN</button>
    </form>
  </div>

  <div class="form-section" style="border-color:var(--red);">
    <h3 style="color:var(--red);">Disable PIN</h3>
    <form method="POST">
      <input type="hidden" name="action" value="disable">
      <div class="fg"><label>Account Password</label>
        <div class="input-wrap"><input type="password" name="password" id="dp" placeholder="Confirm with password" required><button type="button" class="eye-btn" onclick="togglePwd('dp')">👁</button></div>
      </div>
      <button type="submit" class="btn btn-danger">Disable Transaction PIN</button>
    </form>
  </div>
  {% endif %}
</div>
</div>
</body></html>"""

SETTINGS_PRIVACY_HTML = """<!DOCTYPE html><html><head><title>Privacy - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/settings">Settings</a> › <span>Privacy</span></div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>🔒 Privacy</h1></div>
  <div class="form-section">
    <h3>Privacy Settings</h3>
    <form method="POST">
      <div class="setting-row">
        <div><div class="setting-label">Hide Balance by Default</div><div class="setting-desc">Your balance will be hidden when you open wallet</div></div>
        <label class="toggle"><input type="checkbox" name="privacy_hide_balance" {{ 'checked' if user.privacy_hide_balance else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Hide Transaction History</div><div class="setting-desc">Transactions hidden by default on wallet page</div></div>
        <label class="toggle"><input type="checkbox" name="privacy_hide_txs" {{ 'checked' if user.privacy_hide_txs else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
    </form>
  </div>
</div>
</div>
</body></html>"""

SETTINGS_NOTIFICATIONS_HTML = """<!DOCTYPE html><html><head><title>Notifications - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/settings">Settings</a> › <span>Notifications</span></div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="page-header"><h1>🔔 Notifications</h1></div>
  <div class="form-section">
    <h3>Email Notifications</h3>
    <form method="POST">
      <div class="setting-row">
        <div><div class="setting-label">Transaction Alerts</div><div class="setting-desc">Email when NYN is sent or received</div></div>
        <label class="toggle"><input type="checkbox" name="notif_tx" {{ 'checked' if user.notif_tx else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Security Alerts</div><div class="setting-desc">Email on new logins and security events</div></div>
        <label class="toggle"><input type="checkbox" name="notif_security" {{ 'checked' if user.notif_security else '' }} onchange="this.form.submit()"><span class="toggle-slider"></span></label>
      </div>
    </form>
  </div>
</div>
</div>
</body></html>"""

REGISTER_HTML = """<!DOCTYPE html><html><head><title>Create Wallet - NYN</title>""" + STYLES + """
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head><body>
<div class="auth-page">
<div class="auth-card">
  <div class="auth-logo"><span>⚡ NYN NoyanCoin</span><div style="font-size:0.75em;color:var(--text2);margin-top:4px;">Republic of Nowhere</div></div>
  <h2>Create Your Wallet</h2>
  <p class="sub">Join the Republic of Nowhere</p>
  <div class="bonus-badge">🎁 50 NYN free on signup • +20 NYN per referral (max 3)</div>
  {% if msg %}<div class="alert {{ msg_type }}">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Username</label><input type="text" name="username" placeholder="Choose a username" required maxlength="30" autocomplete="off"></div>
    <div class="fg"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div class="fg"><label>Password</label>
      <div class="input-wrap"><input type="password" name="password" id="p1" placeholder="Min 8 chars, use uppercase & symbols" required minlength="8" oninput="checkPwd(this.value,'pwd-bar','pwd-hint')"><button type="button" class="eye-btn" onclick="togglePwd('p1')">👁</button></div>
      <div class="pwd-bar" id="pwd-bar"></div>
      <div class="pwd-hint" id="pwd-hint"></div>
    </div>
    <div class="fg"><label>Confirm Password</label>
      <div class="input-wrap"><input type="password" name="confirm" id="p2" placeholder="Repeat password" required><button type="button" class="eye-btn" onclick="togglePwd('p2')">👁</button></div>
    </div>
    <div class="fg"><label>Referral Code (optional)</label><input type="text" name="referral" placeholder="Enter code for +20 NYN bonus"></div>
    <div class="recaptcha-wrap"><div class="g-recaptcha" data-sitekey="{{ site_key }}"></div></div>
    <button type="submit" class="btn btn-primary btn-full">Create Wallet & Get 50 NYN ⚡</button>
  </form>
  <div style="text-align:center;margin-top:20px;font-size:0.875em;color:var(--text2);">Already have a wallet? <a href="/login">Login here</a></div>
  <div style="text-align:center;margin-top:12px;"><button class="theme-btn" onclick="toggleTheme()">🌙 Toggle Theme</button></div>
</div>
</div>
</body></html>"""

LOGIN_HTML = """<!DOCTYPE html><html><head><title>Login - NYN</title>""" + STYLES + """</head><body>
<div class="auth-page">
<div class="auth-card">
  <div class="auth-logo"><span>⚡ NYN NoyanCoin</span><div style="font-size:0.75em;color:var(--text2);margin-top:4px;">Republic of Nowhere</div></div>
  <h2>Welcome Back</h2>
  <p class="sub">Login to your NYN wallet</p>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  {% if attempts is not none and attempts < 5 and attempts > 0 %}<div class="alert warning">⚠️ {{ attempts }} attempts remaining before lockout</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Username</label><input type="text" name="username" {% if username %}value="{{ username }}"{% endif %} placeholder="Your username" required autocomplete="username"></div>
    <div class="fg"><label>Password</label>
      <div class="input-wrap"><input type="password" name="password" id="lp" placeholder="Your password" required autocomplete="current-password"><button type="button" class="eye-btn" onclick="togglePwd('lp')">👁</button></div>
    </div>
    {% if show_2fa %}<div class="fg"><label>2FA Code</label><input type="text" name="two_fa_code" placeholder="6-digit authenticator code" maxlength="6" autocomplete="off"></div>{% endif %}
    <button type="submit" class="btn btn-primary btn-full">Login ⚡</button>
  </form>
  <div style="text-align:center;margin-top:20px;font-size:0.875em;color:var(--text2);">No wallet yet? <a href="/register">Create one free</a></div>
  <div style="text-align:center;margin-top:12px;"><button class="theme-btn" onclick="toggleTheme()">🌙 Toggle Theme</button></div>
</div>
</div>
</body></html>"""

VERIFY_HTML = """<!DOCTYPE html><html><head><title>Verify Email - NYN</title>""" + STYLES + """</head><body>
<div class="auth-page">
<div class="auth-card">
  <div class="auth-logo"><span>⚡ NYN NoyanCoin</span></div>
  <h2>Verify Your Email</h2>
  <p class="sub">Enter the 6-digit code sent to your inbox</p>
  <div class="alert info">📧 Check your inbox AND spam/junk folder</div>
  <div class="alert warning">⚠️ If in spam, mark as "Not Spam"</div>
  {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
  <form method="POST">
    <div class="fg"><label>Verification Code</label><input type="text" name="otp" class="otp-input" placeholder="000000" maxlength="6" required autocomplete="off" autofocus></div>
    <button type="submit" class="btn btn-primary btn-full">Verify & Activate Wallet ⚡</button>
  </form>
  <div style="text-align:center;margin-top:16px;font-size:0.875em;"><a href="/resend-otp">Resend verification code</a></div>
</div>
</div>
</body></html>"""

SETUP_2FA_HTML = """<!DOCTYPE html><html><head><title>Setup 2FA - NYN</title>""" + STYLES + """
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="breadcrumb"><a href="/settings">Settings</a> › <a href="/settings/security">Security</a> › <span>Setup 2FA</span></div>
  <div class="page-header"><h1>🔐 Setup Two-Factor Authentication</h1></div>
  <div class="card" style="max-width:500px;">
    {% if msg %}<div class="alert error">{{ msg }}</div>{% endif %}
    <div class="alert info" style="margin-bottom:16px;">
      1. Download <strong>Google Authenticator</strong> or <strong>Authy</strong><br>
      2. Scan the QR code below<br>
      3. Enter the 6-digit code to confirm
    </div>
    <div style="background:white;padding:16px;border-radius:10px;display:flex;justify-content:center;margin:16px 0;"><div id="qr2fa"></div></div>
    <div style="text-align:center;margin-bottom:16px;">
      <div style="font-size:0.8em;color:var(--text2);margin-bottom:6px;">Manual entry key:</div>
      <code style="background:var(--bg);padding:8px 12px;border-radius:6px;font-size:0.85em;color:var(--orange);">{{ secret }}</code>
    </div>
    <form method="POST">
      <div class="fg"><label>Enter 6-digit code from authenticator</label><input type="text" name="token" class="otp-input" placeholder="000000" maxlength="6" required autocomplete="off" autofocus></div>
      <button type="submit" class="btn btn-primary btn-full">Verify & Enable 2FA ⚡</button>
    </form>
    <script>new QRCode(document.getElementById("qr2fa"),{text:"{{ qr_uri }}",width:180,height:180,colorDark:"#000",colorLight:"#fff"});</script>
  </div>
</div>
</div>
</body></html>"""

BACKUP_CODES_HTML = """<!DOCTYPE html><html><head><title>Backup Codes - NYN</title>""" + STYLES + """</head><body>
{{ sidebar | safe }}
<div class="main-content">
{{ topbar | safe }}
<div class="page">
  <div class="page-header"><h1>🔐 2FA Enabled!</h1><p>Save your backup codes</p></div>
  <div class="card" style="max-width:500px;">
    <div class="alert warning" style="margin-bottom:16px;">⚠️ Save these codes now — they won't be shown again. Each code can only be used once.</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;justify-content:center;">
      {% for code in codes %}<span class="backup-code">{{ code }}</span>{% endfor %}
    </div>
    <button onclick="var t=Array.from(document.querySelectorAll('.backup-code')).map(e=>e.textContent).join('\\n');navigator.clipboard.writeText(t);this.textContent='✓ Copied!';" class="btn btn-secondary btn-full">📋 Copy All Codes</button>
    <a href="/settings/security" class="btn btn-primary btn-full" style="display:block;text-align:center;text-decoration:none;margin-top:8px;">I've saved my codes ✓</a>
  </div>
</div>
</div>
</body></html>"""