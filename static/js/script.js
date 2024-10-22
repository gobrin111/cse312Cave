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
} //this works and is done

function chatMessageHTML(messageJSON) { //adds the message from the db to the chat box
    const username = messageJSON.username;
    const message = messageJSON.message;
    const messageId = messageJSON.id;
    const color = messageJSON.color;
    const like_number = messageJSON.like_number;
    console.log(messageJSON.like_number);
    let messageHTML = "<div class='message-container' id='message_"+messageId+"'> <button onclick='deleteMessage(\""+messageId+"\")'>X</button>" + username +": <br/> <button onclick='likeMessage(\""+messageId+"\")'>👍</button> "+like_number+" <div style='background-color: " + color + "'>"+message+"</div> </div>"
    return messageHTML
} //this is a helper to another function, but this should be done

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

// function getCookie(name) {
//   // Create a regular expression to find the cookie by name
//   const cookieArr = document.cookie.split("; ");
//
//   // Loop through the cookie array
//   for (let i = 0; i < cookieArr.length; i++) {
//     let cookie = cookieArr[i].trim();
//     // Check if this cookie matches the name
//     if (cookie.startsWith(name + "=")) {
//       return cookie.substring(name.length + 1); // Return the cookie value
//     }
//   }
//   return "none";
// }
function likeMessage(messageId){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    // getting the user's auth_token and sending it with the messageid
    // const auth_token = getCookie("auth_token");
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