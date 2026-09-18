<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>CloudCart Support</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-top: #0f172a;
    --bg-bottom: #1e293b;
    --panel: #ffffff;
    --panel-border: #e2e8f0;
    --accent: #4f46e5;
    --accent-hover: #4338ca;
    --accent-soft: #eef2ff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --user-bubble: #4f46e5;
    --bot-bubble: #f1f5f9;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    min-height: 100vh;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(160deg, var(--bg-top), var(--bg-bottom));
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }

  .app {
    width: 100%;
    max-width: 480px;
    background: var(--panel);
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 640px;
  }

  .header {
    background: linear-gradient(135deg, var(--accent), #7c3aed);
    color: white;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .header .logo {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(255,255,255,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
  }

  .header .title {
    font-weight: 700;
    font-size: 16px;
  }

  .header .subtitle {
    font-size: 12px;
    opacity: 0.85;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
  }

  .chips {
    display: flex;
    gap: 8px;
    padding: 12px 16px;
    overflow-x: auto;
    border-bottom: 1px solid var(--panel-border);
    background: #fafafa;
  }

  .chip {
    flex: none;
    background: var(--accent-soft);
    color: var(--accent);
    border: none;
    border-radius: 999px;
    padding: 7px 14px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
    transition: background 0.15s ease;
  }

  .chip:hover { background: #e0e7ff; }

  #chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    background: #ffffff;
  }

  .row {
    display: flex;
    gap: 8px;
    align-items: flex-end;
  }

  .row.user { justify-content: flex-end; }

  .avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex: none;
    background: var(--accent-soft);
  }

  .bubble {
    max-width: 75%;
    padding: 10px 14px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.45;
    white-space: pre-wrap;
  }

  .row.bot .bubble {
    background: var(--bot-bubble);
    color: var(--text-main);
    border-bottom-left-radius: 4px;
  }

  .row.user .bubble {
    background: var(--user-bubble);
    color: white;
    border-bottom-right-radius: 4px;
  }

  .typing {
    display: inline-flex;
    gap: 4px;
    padding: 12px 14px;
  }

  .typing span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #94a3b8;
    animation: bounce 1.2s infinite ease-in-out;
  }

  .typing span:nth-child(2) { animation-delay: 0.15s; }
  .typing span:nth-child(3) { animation-delay: 0.3s; }

  @keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.6; }
    30% { transform: translateY(-4px); opacity: 1; }
  }

  .input-area {
    display: flex;
    gap: 8px;
    padding: 14px 16px;
    border-top: 1px solid var(--panel-border);
    background: #ffffff;
  }

  #messageInput {
    flex: 1;
    border: 1px solid var(--panel-border);
    border-radius: 12px;
    padding: 11px 14px;
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.15s ease;
  }

  #messageInput:focus { border-color: var(--accent); }

  #sendBtn {
    border: none;
    background: var(--accent);
    color: white;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: none;
    transition: background 0.15s ease;
  }

  #sendBtn:hover { background: var(--accent-hover); }
  #sendBtn:disabled { background: #cbd5e1; cursor: not-allowed; }

  #chat::-webkit-scrollbar { width: 6px; }
  #chat::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 3px; }
</style>
</head>
<body>

<div class="app">
  <div class="header">
    <div class="logo">🛒</div>
    <div>
      <div class="title">CloudCart Support</div>
      <div class="subtitle"><span class="status-dot"></span> AI agent online</div>
    </div>
  </div>

  <div class="chips">
    <button class="chip" data-msg="What is the status of order ORD-1001?">📦 Check order ORD-1001</button>
    <button class="chip" data-msg="What is your return policy?">↩️ Return policy</button>
    <button class="chip" data-msg="Do electronics come with a warranty?">🛡️ Warranty info</button>
    <button class="chip" data-msg="Will bad weather delay my delivery to Stockholm?">⛅ Shipping delays</button>
  </div>

  <div id="chat"></div>

  <div class="input-area">
    <input type="text" id="messageInput" placeholder="Ask about an order, policy, or shipping..." autocomplete="off" />
    <button id="sendBtn" aria-label="Send">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 20L21 12L3 4V10L16 12L3 14V20Z" fill="white"/>
      </svg>
    </button>
  </div>
</div>

<script>
  var API_ENDPOINT = "${chat_endpoint}";
  var sessionId = "session-" + Math.random().toString(36).slice(2) + Date.now();

  var chatEl = document.getElementById("chat");
  var inputEl = document.getElementById("messageInput");
  var sendBtn = document.getElementById("sendBtn");

  function addBubble(text, sender) {
    var row = document.createElement("div");
    row.className = "row " + sender;

    var avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = sender === "user" ? "🧑" : "🤖";

    var bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    if (sender === "user") {
      row.appendChild(bubble);
      row.appendChild(avatar);
    } else {
      row.appendChild(avatar);
      row.appendChild(bubble);
    }

    chatEl.appendChild(row);
    chatEl.scrollTop = chatEl.scrollHeight;
    return row;
  }

  function addTypingIndicator() {
    var row = document.createElement("div");
    row.className = "row bot";
    row.id = "typingRow";

    var avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "🤖";

    var bubble = document.createElement("div");
    bubble.className = "bubble typing";
    bubble.innerHTML = "<span></span><span></span><span></span>";

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatEl.appendChild(row);
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  function removeTypingIndicator() {
    var row = document.getElementById("typingRow");
    if (row) row.remove();
  }

  function sendMessage(overrideText) {
    var text = (overrideText !== undefined ? overrideText : inputEl.value).trim();
    if (!text) return;

    addBubble(text, "user");
    inputEl.value = "";
    sendBtn.disabled = true;
    addTypingIndicator();

    fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: text })
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        removeTypingIndicator();
        addBubble(data.reply || data.error || "No response", "bot");
      })
      .catch(function (err) {
        removeTypingIndicator();
        addBubble("Error: " + err.message, "bot");
      })
      .finally(function () {
        sendBtn.disabled = false;
        inputEl.focus();
      });
  }

  sendBtn.addEventListener("click", function () { sendMessage(); });
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
  });

  var chips = document.querySelectorAll(".chip");
  for (var i = 0; i < chips.length; i++) {
    chips[i].addEventListener("click", function () {
      sendMessage(this.getAttribute("data-msg"));
    });
  }

  addBubble("Hi! I'm the CloudCart support agent. Ask me about an order, our policies, or shipping delays.", "bot");
</script>

</body>
</html>
