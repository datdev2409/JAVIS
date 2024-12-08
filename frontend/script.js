function sendMessage() {
  const userInput = document.getElementById('user-input').value;
  const chatMessages = document.querySelector('.chat-messages');

  // Display user message
  const userMessage = document.createElement('div');
  userMessage.classList.add('user-message');
  userMessage.textContent = userInput;
  chatMessages.appendChild(userMessage);

  // Simulate bot response (replace with actual API call)
  const botMessage = document.createElement('div');
  botMessage.classList.add('bot-message');
  botMessage.textContent = "Bot: Your balance is $1000."; // Replace with actual response
  chatMessages.appendChild(botMessage);

  document.getElementById('user-input').value = '';
}