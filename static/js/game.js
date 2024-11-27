let currentRow = 0;
let currentCol = 0;
let word = "PLANT";
let input = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
let rows = document.querySelectorAll(".row");

document.addEventListener("keydown", (e) => {
    if (document.activeElement != document.getElementById("chat-input")) {
        const key = e.key.toUpperCase();

        if (key === "ENTER") {
            if (currentCol == 5) {
                let tilesArray = rows[currentRow].querySelectorAll(".inner");
                tilesArray.forEach((tile, i) => {
                    setTimeout(() => {
                        let textElement = tile.querySelector(".inner-text");
                        let guessChar = textElement.textContent;
                        let actualChar = word[i];

                        tile.classList.remove("expand-shrink");
                        if (guessChar == actualChar) {
                            tile.classList.add("correct-flip");
                        } else if (guessChar != actualChar && word.includes(guessChar)) {
                            tile.classList.add("partial-flip");
                        } else {
                            tile.classList.add("incorrect-flip");
                        }

                    }, i * 200);
                });
                if (currentRow < 5) {
                    currentRow ++;
                    currentCol = 0;
                }
            }

        } else if (key === "BACKSPACE") {
            if (currentCol > 0) {
                currentCol -= 1;
                input[currentRow][currentCol] = ''

                let tilesArray = rows[currentRow].querySelectorAll(".inner");
                tile = tilesArray[currentCol];
                textElement = tile.querySelector(".inner-text");
                textElement.innerHTML = '';
                textElement.style.opacity = "1";
                tile.classList.remove("expand-shrink");
                tile.style.borderColor = "#3a3a3c";
            }

        } else if (/^[A-Z]$/.test(key)) { // Allow only A-Z letters
            if (currentCol < 5) {
                input[currentRow][currentCol] = key

                let tilesArray = rows[currentRow].querySelectorAll(".inner");
                tile = tilesArray[currentCol];
                textElement = tile.querySelector(".inner-text");
                textElement.innerHTML = key;
                textElement.style.opacity = "1";
                tile.classList.add("expand-shrink");
                tile.style.borderColor = "#565758";

                currentCol += 1;
            }
        }
    }
});