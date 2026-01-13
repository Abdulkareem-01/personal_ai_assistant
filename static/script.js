function send() {
  let msg = document.getElementById("msg").value;
  if (!msg) return;

  let chat = document.getElementById("chat");
  chat.innerHTML += `<div class="user">${msg}</div>`;
  document.getElementById("msg").value = "";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    chat.innerHTML += `<div class="bot">${data.reply.replace(/\n/g, "<br>")}</div>`;
    chat.scrollTop = chat.scrollHeight;
  });
}
