async function sendMessage() {
  const userInput = document.getElementById('user-input').value;
  const chatMessages = document.querySelector('.chat-messages');

  // Display user message
  const userMessage = document.createElement('div');
  userMessage.classList.add('user-message');
  userMessage.textContent = userInput;
  chatMessages.appendChild(userMessage);

  // Simulate bot response (replace with actual API call)
  const botResponse = await fetch("https://2pabwb591j.execute-api.ap-southeast-1.amazonaws.com/messages", {
    method: "POST",
    body: JSON.stringify({ message: userInput }),
  })
  const botMessage = document.createElement('div');
  botMessage.classList.add('bot-message');
  botMessage.textContent = `Bot: ${await botResponse.text()}`;
  chatMessages.appendChild(botMessage);

  document.getElementById('user-input').value = '';
}