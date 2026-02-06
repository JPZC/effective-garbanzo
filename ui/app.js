const statusEl = document.getElementById("engine-status");
const historyEl = document.getElementById("history");
const commandInput = document.getElementById("command-input");

async function sendCommand() {
  const text = commandInput.value.trim();
  if (!text) return;

  appendHistory(`Enviando: ${text}`);
  commandInput.value = "";

  try {
    const response = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    appendHistory(`Respuesta: ${data.message || "Sin respuesta"}`);
  } catch (error) {
    appendHistory("Error al enviar el comando.");
  }
}

function appendHistory(message) {
  if (historyEl.querySelector(".history-item")) {
    if (historyEl.querySelector(".history-item").textContent === "Sin comandos aún.") {
      historyEl.innerHTML = '<p class="history-title">Historial</p>';
    }
  }
  const entry = document.createElement("div");
  entry.className = "history-item";
  entry.textContent = message;
  historyEl.appendChild(entry);
}

document.getElementById("send-command").addEventListener("click", sendCommand);
commandInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendCommand();
  }
});

document.getElementById("start-listen").addEventListener("click", async () => {
  statusEl.textContent = "Escuchando";
  statusEl.style.color = "#facc15";
});

document.getElementById("stop-listen").addEventListener("click", async () => {
  statusEl.textContent = "Listo";
  statusEl.style.color = "#4ade80";
});
