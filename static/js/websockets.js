// let ws = true;
// updates the chat using polling, if websockets are off
if(!ws){
    setInterval(updateChat, 500);
}


const socket = io({autoConnect: false})
if(ws){
    socket.connect()
}

// testing to see if the user is properly connected
socket.on("connect", function(){
    socket.emit("test", "user_stuff");
})

// listens for any new comments added to the database
socket.on("updateChat", function (server_data){
    addMessageToChat(server_data);
})

// listens for any deletion of a comment
socket.on("deleteUpdate", function(messageId){
    let message_2b_deleted = document.getElementById(messageId);
    message_2b_deleted.remove();
})

// listens to the server for any changes in the likes for the comments
socket.on("likeMessage_client", function (server_data){
    let update_like = document.getElementById(server_data.message_id);
    update_like.textContent = server_data.num;
})

// client listens to the server to get the updated time so that there is no client side timing
socket.on('timer_update', function (data) {
    let time_left = data.remaining_time;
    // console.log(time_left)
    let timer_box = document.getElementById("time");
    timer_box.textContent = "Time: " + String(time_left);
})


// start timer button calls this function when clicked
function timer_button(){
    //calls server to start timer and resets current score on browser
    // console.log("button clicked")
    socket.emit("timer_start");

}


// game stuff below

// updates the current score that a user has
socket.on('update_active_score', function(data){
    let score = String(data.score);
    if (score === "invalid"){
        document.getElementById(`score`).textContent = "Score: 0";
    } else {
        document.getElementById(`score`).textContent = "Score: " + score;
    }
})


socket.on('update_leaderboard', function (){
    updateBoard()
})