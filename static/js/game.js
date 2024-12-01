let currentRow = 0;
let currentCol = 0;
let input = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
let rows = document.querySelectorAll(".row");
let alertMessage = document.getElementById('alert-message');

// Replace with API
let wordList = ["ALBUM","HINGE","MONEY","SCRAP","GAMER","GLASS","SCOUR","BEING","DELVE","YIELD","METAL","TIPSY","SLUNG","FARCE","GECKO","SHINE","CANNY","MIDST","BADGE","HOMER","TRAIN","STORY","HAIRY","FORGO","LARVA","TRASH","ZESTY","SHOWN","HEIST","ASKEW","INERT","OLIVE","PLANT","OXIDE","CARGO","FOYER","FLAIR","AMPLE","CHEEK","SHAME","MINCE","CHUNK","ROYAL","SQUAD","BLACK","STAIR","SCARE","FORAY","COMMA","NATAL","SHAWL","FEWER","TROPE","SNOUT","LOWLY","STOVE","SHALL","FOUND","NYMPH","EPOXY","DEPOT","CHEST","PURGE","SLOSH","THEIR","RENEW","ALLOW","SAUTE","MOVIE","CATER","TEASE","SMELT","FOCUS","TODAY","WATCH","LAPSE","MONTH","SWEET","HOARD","CLOTH","BRINE","AHEAD","MOURN","NASTY","RUPEE","CHOKE","CHANT","SPILL","VIVID","BLOKE","TROVE","THORN","OTHER","TACIT","SWILL","DODGE","SHAKE","CAULK","AROMA","CYNIC","ROBIN","ULTRA","ULCER","PAUSE","HUMOR","FRAME","ELDER","SKILL","ALOFT","PLEAT","SHARD","MOIST","THOSE","LIGHT","WRUNG","COULD","PERKY","MOUNT","WHACK","SUGAR","KNOLL","CRIMP","WINCE","PRICK","ROBOT","POINT","PROXY","SHIRE","SOLAR","PANIC","TANGY","ABBEY","FAVOR","DRINK","QUERY","GORGE","CRANK","SLUMP","BANAL","TIGER","SIEGE","TRUSS","BOOST","REBUS","UNIFY","TROLL","TAPIR","ASIDE","FERRY","ACUTE","PICKY","WEARY","GRIPE","CRAZE","PLUCK","BRAKE","BATON","CHAMP","PEACH","USING","TRACE","VITAL","SONIC","MASSE","CONIC","VIRAL","RHINO","BREAK","TRIAD","EPOCH","USHER","EXULT","GRIME","CHEAT","SOLVE","BRING","PROVE","STORE","TILDE","CLOCK","WROTE","RETCH","PERCH","ROUGE","RADIO","SURER","FINER","VODKA","HERON","CHILL","GAUDY","PITHY","SMART","BADLY","ROGUE","GROUP","FIXER","GROIN","DUCHY","COAST","BLURT","PULPY","ALTAR","GREAT","BRIAR","CLICK","GOUGE","WORLD","ERODE","BOOZY","DOZEN","FLING","GROWL","ABYSS","STEED","ENEMA","JAUNT","COMET","TWEED","PILOT","DUTCH","BELCH","OUGHT","DOWRY","THUMB","HYPER","HATCH","ALONE","MOTOR","ABACK","GUILD","KEBAB","SPEND","FJORD","ESSAY","SPRAY","SPICY","AGATE","SALAD","BASIC","MOULT","CORNY","FORGE","CIVIC","ISLET","LABOR","GAMMA","LYING","AUDIT","ROUND","LOOPY","LUSTY","GOLEM","GONER","GREET","START","LAPEL","BIOME","PARRY","SHRUB","FRONT","WOOER","TOTEM","FLICK","DELTA","BLEED","ARGUE","SWIRL","ERROR","AGREE","OFFAL","FLUME","CRASS","PANEL","STOUT","BRIBE","DRAIN","YEARN","PRINT","SEEDY","IVORY","BELLY","STAND","FIRST","FORTH","BOOBY","FLESH","UNMET","LINEN","MAXIM","POUND","MIMIC","SPIKE","CLUCK","CRATE","DIGIT","REPAY","SOWER","CRAZY","ADOBE","OUTDO","TRAWL","WHELP","UNFED","PAPER","STAFF","CROAK","HELIX","FLOSS","PRIDE","BATTY","REACT","MARRY","ABASE","COLON","STOOL","CRUST","FRESH","DEATH","MAJOR","FEIGN","ABATE","BENCH","QUIET","GRADE","STINK","KARMA","MODEL","DWARF","HEATH","SERVE","NAVAL","EVADE","FOCAL","BLUSH","AWAKE","HUMPH","SISSY","REBUT","CIGAR"];

function getRandomWord() {
    let randomIndex = Math.floor(Math.random() * wordList.length);
    return wordList[randomIndex];
}

let word = getRandomWord();
console.log(word);

function resetGame() {
    currentRow = 0;
    currentCol = 0;
    input = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']];
    word = getRandomWord();
    console.log(word);
    rows.forEach(row => {
        let tilesArray = row.querySelectorAll(".inner");
        tilesArray.forEach((tile, i) => {
            let textElement = tile.querySelector(".inner-text");
            textElement.innerHTML = '';
            textElement.style.opacity = "0";
            tile.classList.remove("expand-shrink", "correct-flip", "partial-flip", "incorrect-flip");
            tile.style.borderColor = "#3a3a3c";
            tile.style.backgroundColor = "#121213";
        });
    });
}

function isWord(word) {
    return fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word.toLowerCase()}`)
        .then(response => {
            if (response.ok || wordList.includes(word)) {
                return true;
            } else {
                return false;
            }
        })
        .catch(error => {
            if (wordList.includes(word)){
                return true;
            }
            return false;
        });
}

document.addEventListener("keydown", (e) => {
    if (document.activeElement != document.getElementById("chat-input")) {
        let key = e.key.toUpperCase();

        if (key === "ENTER") {
            if (currentCol == 5) {
                isWord(input[currentRow].join('')).then(result => {
                    if (result) {
                        let tilesArray = rows[currentRow].querySelectorAll(".inner");
                        let charFreq = {};
                        for (let char of word){
                            charFreq[char] = (charFreq[char] || 0) + 1;
                        }
                        tilesArray.forEach((tile, i) => {
                            setTimeout(() => {
                                let textElement = tile.querySelector(".inner-text");
                                let guessChar = textElement.textContent;
                                let actualChar = word[i];

                                tile.classList.remove("expand-shrink");
                                if (guessChar == actualChar && charFreq[guessChar] > 0) {
                                    tile.classList.add("correct-flip");
                                    charFreq[guessChar]--;
                                } else if (word.includes(guessChar) && charFreq[guessChar] > 0) {
                                    tile.classList.add("partial-flip");
                                    charFreq[guessChar]--;
                                } else {
                                    tile.classList.add("incorrect-flip");
                                }

                            }, i * 200);
                        });

                        if (input[currentRow].join('') == word) {
                            let map = {
                                0: 20,
                                1: 10,
                                2: 5,
                                3: 4,
                                4: 2,
                                5: 1,
                            }
                            let score = map[currentRow];

                            if(ws){

                            } else {
                                const request = new XMLHttpRequest();

                                request.onreadystatechange = function () {
                                    if (this.readyState === 4 && this.status === 200) {
                                        console.log(this.response);
                                        const response = JSON.parse(this.response)
                                        if (response.score === "invalid"){
                                            document.getElementById(`score`).textContent = "Score: 0";
                                        } else {
                                            document.getElementById(`score`).textContent = "Score: " + response.score;
                                        }
                                    }
                                }

                                request.open("POST", "/send_score", true);
                                request.setRequestHeader("Content-Type", "application/json");

                                request.send(JSON.stringify({"score" : score}));
                            }

                            setTimeout(resetGame, 2000);

                        } else {
                            currentRow++;
                            currentCol = 0;
                        }

                        if (currentRow == 6) {
                            alertMessage.textContent = "The word was " + word;
                            setTimeout(() => {
                                alertMessage.textContent = "";
                            }, 2000);

                            let score = -5;

                            if(ws){

                            } else {
                                const request = new XMLHttpRequest();

                                request.onreadystatechange = function () {
                                    console.log(this.response);
                                    const response = JSON.parse(this.response)
                                    if (response.score === "invalid"){
                                        document.getElementById(`score`).textContent = "Score: 0";
                                    } else {
                                        document.getElementById(`score`).textContent = "Score: " + response.score;
                                    }
                                }

                                request.open("POST", "/send_score");
                                request.setRequestHeader("Content-Type", "application/json");

                                request.send(JSON.stringify({"score" : score}));
                            }

                            setTimeout(resetGame, 2000);
                        }

                    } else {
                        alertMessage.textContent = "*Word not found*";
                        setTimeout(() => {
                            alertMessage.textContent = "";
                        }, 1000);
                    }

                }).catch(error => {
                    alertMessage.textContent = "*Could not verify the word*";
                    setTimeout(() => {
                        alertMessage.textContent = "";
                    }, 1000);
                });

            } else {
                alertMessage.textContent = "*Word not long enough*";
                setTimeout(() => {
                    alertMessage.textContent = "";
                }, 1000);
            }

        } else if (key === "BACKSPACE") {
            if (currentCol > 0) {
                currentCol -= 1;
                input[currentRow][currentCol] = ''

                let tilesArray = rows[currentRow].querySelectorAll(".inner");
                let tile = tilesArray[currentCol];
                let textElement = tile.querySelector(".inner-text");
                textElement.innerHTML = '';
                textElement.style.opacity = "0";
                tile.classList.remove("expand-shrink");
                tile.style.borderColor = "#3a3a3c";
            }

        } else if (/^[A-Z]$/.test(key)) { // Allow only A-Z letters
            if (currentCol < 5) {
                input[currentRow][currentCol] = key

                let tilesArray = rows[currentRow].querySelectorAll(".inner");
                let tile = tilesArray[currentCol];
                let textElement = tile.querySelector(".inner-text");
                textElement.innerHTML = key;
                textElement.style.opacity = "1";
                tile.classList.add("expand-shrink");
                tile.style.borderColor = "#565758";

                currentCol += 1;
            }
        }
    }
});