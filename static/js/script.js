let chatMessages = {};
setInterval(updateChat, 500);

function sendChat() {
    let userInput = document.getElementById("chat-input");
    let userInputValue = userInput.value;

    userInput.value = "";
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    const messageJSON = {"message": userInputValue};
    request.open("POST", "/chat-messages");
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(messageJSON));

    userInput.focus();
}

function chatMessageHTML(messageJSON) {
    const username = messageJSON.username;
    const message = messageJSON.message;
    const messageId = messageJSON.id;
    const from_user = messageJSON.from_user;
    const like_count = messageJSON.like_count;

    let origin = "other";
    if (from_user) {
        origin = "original";
    }

    let messageHTML = `
        <div class="message-container" id="message_${messageId}">
            ${username} &emsp;
            <button onclick="likeMessage('${messageId}')"> 👍 </button> 
            <span id="like_count_${messageId}">${like_count}</span> <br>
            <button onclick="deleteMessage('${messageId}')"> X </button>
            <div class="${origin}"> ${message} </div>
        </div>
        `
    return messageHTML
}

function deleteMessage(messageId) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("POST", "/chat-messages/" + messageId);
    request.send();
}

function likeMessage(messageId){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            const response = JSON.parse(this.response)
            document.getElementById(`like_count_${messageId}`).textContent = response.like_count;
        }
    }

    request.open("POST", "/chat-messages/like/" + messageId);
    request.send();
}

function addMessageToChat(messageJSON) {
    const chatMessages = document.querySelector('.chat-log');
    chatMessages.insertAdjacentHTML("beforeend", chatMessageHTML(messageJSON))
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function updateChat() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updateChatMessages(JSON.parse(this.response));
        }
    }
    request.open("GET", "/chat-messages");
    request.send();
}

function updateChatMessages(serverMessages) {
    let serverIndex = 0
    let localIndex = 0;

    while (serverIndex < serverMessages.length && localIndex < chatMessages.length) {
        let fromServer = serverMessages[serverIndex];
        let localMessage = chatMessages[localIndex];
        if (fromServer["id"] !== localMessage["id"]) {
            // this message has been deleted
            const messageElem = document.getElementById("message_" + localMessage["id"]);
            messageElem.parentNode.removeChild(messageElem);
            localIndex++;
        } else {
            serverIndex++;
            localIndex++;
        }
    }

    while (localIndex < chatMessages.length) {
        let localMessage = chatMessages[localIndex];
        const messageElem = document.getElementById("message_" + localMessage["id"]);
        messageElem.parentNode.removeChild(messageElem);
        localIndex++;
    }

    while (serverIndex < serverMessages.length) {
        addMessageToChat(serverMessages[serverIndex]);
        serverIndex++;
    }
    chatMessages = serverMessages;
}