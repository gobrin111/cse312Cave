window.addEventListener("load", (event) => {
    let tiles = document.getElementsByClassName("inner");
    let tilesArray = Array.from(tiles);
    setTimeout(function() {
        writeWord(tiles, tilesArray);
    }, 200);
});

function writeWord(tiles, tilesArray) {
        tilesArray.forEach((tile, i) => {
        const textElement = tile.querySelector(".inner-text");
        setTimeout(() => {
            textElement.style.opacity = "1";
            tile.classList.add("expand-shrink");
            tile.style.borderColor = "#565758";
        }, i * 200);
    });
}

function wordleFlipCorrect(tiles, tilesArray) {
    tilesArray.forEach((tile, i) => {
        setTimeout(() => {
         tile.classList.remove("expand-shrink");
         tile.classList.add("correct-flip");
        }, i * 200);
    });
}

function wordleFlipIncorrect(tiles, tilesArray) {
    tilesArray.forEach((tile, i) => {
        setTimeout(() => {
         tile.classList.remove("expand-shrink");
         tile.classList.add("incorrect-flip");
        }, i * 200);
    });
}


function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const request = new XMLHttpRequest();
    request.open("POST", "/login", true);
    request.setRequestHeader("Content-Type", "application/json");

    request.onreadystatechange = function () {
        if (this.readyState === 4) {
            if (this.status === 200) {
                let tiles = document.getElementsByClassName("inner");
                let tilesArray = Array.from(tiles);
                wordleFlipCorrect(tiles, tilesArray);
                setTimeout(() => {
                    window.location.href = '/';
                }, 1400);

            } else if (this.status === 403) {
                let tiles = document.getElementsByClassName("inner");
                let tilesArray = Array.from(tiles);
                wordleFlipIncorrect(tiles, tilesArray);
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 1400);
            }
        }
    };

    const loginData = JSON.stringify({ username: username, password: password });
    request.send(loginData);
}

function registerUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const password_confirm = document.getElementById("password_confirm").value;

    const request = new XMLHttpRequest();
    request.open("POST", "/register", true);
    request.setRequestHeader("Content-Type", "application/json");

    request.onreadystatechange = function () {
        if (this.readyState === 4) {
            if (this.status === 200) {
                let tiles = document.getElementsByClassName("inner");
                let tilesArray = Array.from(tiles);
                wordleFlipCorrect(tiles, tilesArray);
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 1800);

            } else if (this.status === 403) {
                let tiles = document.getElementsByClassName("inner");
                let tilesArray = Array.from(tiles);
                wordleFlipIncorrect(tiles, tilesArray);
                setTimeout(() => {
                    window.location.href = '/register.html';
                }, 1800);
            }
        }
    };

    const loginData = JSON.stringify({ username: username, password: password, password_confirm: password_confirm });
    request.send(loginData);
}
