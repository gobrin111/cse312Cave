function sendChat() {
    let userInput = document.getElementById("chat-input");
    let userInputValue = userInput.value;
    userInput.value = "";
    userInput.focus();
}