window.addEventListener("load", (event) => {
    setTimeout(function() {
        wordleFlip();
    }, 500);
});

function wordleFlip() {
    let tiles = document.getElementsByClassName("inner");
    let tilesArray = Array.from(tiles);

    tilesArray.forEach((tile, i) => {
        const textElement = tile.querySelector(".inner-text");
        setTimeout(() => {
            textElement.style.opacity = "1";
            tile.classList.add("expand-shrink");
            tile.style.borderColor = "#565758";
        }, i * 200);
    });

    tilesArray.forEach((tile, i) => {
        setTimeout(() => {
         tile.classList.remove("expand-shrink");
         tile.classList.add("flip");
        }, (i * 200) + 1200);
    });
}
