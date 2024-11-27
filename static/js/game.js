let currentRow = 0
let currentCol = 0
let word = "PLANT"
let input = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
let rows = document.querySelectorAll(".row");

document.addEventListener("keydown", (e) => {
    const key = e.key.toUpperCase();

    if (key === "ENTER") {
        if (currentCol == 5) {
            // check word
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

function wordleFlipPartial(tiles, tilesArray) {
    tilesArray.forEach((tile, i) => {
        setTimeout(() => {
            tile.classList.remove("expand-shrink");
            tile.classList.add("partial-flip");
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