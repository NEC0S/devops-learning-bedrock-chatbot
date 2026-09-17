<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Simple Bedrock Chatbot</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 600px;
      margin: 40px auto;
      padding: 0 20px;
      background: #f5f5f5;
    }
    h1 { font-size: 20px; }
    #chat {
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 15px;
      height: 400px;
      overflow-y: auto;
      margin-bottom: 10px;
    }
    .msg { margin: 8px 0; padding: 8px 12px; border-radius: 8px; max-width: 80%; }
    .user { background: #daf1ff; margin-left: auto; text-align: right; }
    .bot { background: #eee; }
    #inputRow { display: flex; gap: 8px; }
    #messageInput { flex: 1; padding: 10px; border-radius: 6px; border: 1px solid #ccc; }
    #sendBtn { padding: 10px 16px; border: none; border-radius: 6px; background: #007bff; color: white; cursor: pointer; }
    #sendBtn:disabled { background: #aaa; }
  </style>
</head>
<body>
  <h1>Simple Bedrock Chatbot</h1>
  <div id="chat"></div>
  <div id="inputRow">
    <input type="text" id="messageInput" placeholder="Type a message..." />
    <button id="sendBtn">Send</button>
  </div>

  <script>
    const API_ENDPOINT = "${chat_endpoint}";
    const sessionId = crypto.randomUUID();

    const chatEl = document.getElementById("chat");
    const inputEl = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");

    function addMessage(text, sender) {
      const div = document.createElement("div");
      div.className = "msg " + sender;
      div.textContent = text;
      chatEl.appendChild(div);
      chatEl.scrollTop = chatEl.scrollHeight;
    }

    async function sendMessage() {
      const text = inputEl.value.trim();
      if (!text) return;

      addMessage(text, "user");
      inputEl.value = "";
      sendBtn.disabled = true;

      try {
        const res = await fetch(API_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, message: text })
        });
        const data = await res.json();
        addMessage(data.reply || data.error || "No response", "bot");
      } catch (err) {
        addMessage("Error: " + err.message, "bot");
      } finally {
        sendBtn.disabled = false;
      }
    }

    sendBtn.addEventListener("click", sendMessage);
    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") sendMessage();
    });
  </script>
</body>
</html>
