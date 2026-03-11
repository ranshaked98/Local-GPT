const BACKEND_URL = "http://localhost:8000/chat";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Stores conversation history to send to backend
let history = [];

// Add a message bubble to the chat UI
function addMessage(role, text, model = "") {
  const div = document.createElement("div");
  div.classList.add("message", role);

  if (role === "ai" && model) {
    const tag = document.createElement("div");
    tag.classList.add("model-tag");
    tag.textContent = model;
    div.appendChild(tag);
  }

  const content = document.createTextNode(text);
  div.appendChild(content);
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight; // auto-scroll to bottom
}

// Send message to backend and get AI reply
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Show user message in UI
  addMessage("user", message);
  userInput.value = "";
  sendBtn.disabled = true;

  // Add to history
  history.push({ role: "user", content: message });

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history }),
    });

    const data = await response.json();

    // Show AI reply in UI
    addMessage("ai", data.reply, data.model);

    // Add AI reply to history
    history.push({ role: "assistant", content: data.reply });

  } catch (error) {
    addMessage("ai", "Error: Could not reach the backend. Is it running?");
  }

  sendBtn.disabled = false;
  userInput.focus();
}

// Send on button click
sendBtn.addEventListener("click", sendMessage);

// Send on Enter key
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
