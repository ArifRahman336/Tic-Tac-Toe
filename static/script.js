// ===============================
// Ultimate Tic-Tac-Toe Frontend
// ===============================

let gameOver = false;


// ===============================
// INIT ON PAGE LOAD
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("game-board");
    if (!board) return;

    renderBoard();

    // 🔥 Fetch initial state to activate boards
    fetch("/reset", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            updateBoardUI(data);
            updateTurnText(data.currentPlayer || "X");
        });
});

function updateMatchupPanel() {
    const meta = document.getElementById("game-meta");
    if (!meta) return;

    const mode = meta.dataset.mode;
    const p1Name = meta.dataset.p1Name;
    const p2Name = meta.dataset.p2Name;

    document.getElementById("player-left").innerText = p1Name;
    document.getElementById("player-right").innerText =
        mode === "ai" ? "AI 🤖" : p2Name;
}

// ===============================
// INIT
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("game-board");
    if (board) {
        renderBoard();
        // updateStatus("Play in any board");
    }
    loadTheme();
});

// ===============================
// BOARD RENDER
// ===============================
function renderBoard() {
    const container = document.getElementById("game-board");
    container.innerHTML = "";

    for (let b = 0; b < 9; b++) {
        const sb = document.createElement("div");
        sb.className = "small-board";

        for (let c = 0; c < 9; c++) {
            const cell = document.createElement("button");
            cell.className = "cell";
            cell.onclick = () => handleClick(b, c);
            sb.appendChild(cell);
        }

        container.appendChild(sb);
    }
}

// ===============================
// CLICK HANDLER
// ===============================
function handleClick(board, cell) {
    if (gameOver) return;

    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board, cell })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) return;

        updateBoardUI(data);

        if (data.winner) {
            gameOver = true;
            showWinnerPopup(data.winner);
        }
    });
}



// ===============================
// UPDATE BOARD UI
// ===============================
function updateBoardUI(data) {
    const boards = document.getElementsByClassName("small-board");

    for (let b = 0; b < 9; b++) {
        const sb = boards[b];
        sb.className = "small-board"; // reset

        const status = data.smallBoardStatus[b];

        // ---------- BOARD RESULT ----------
        if (status === "X") sb.classList.add("won-x");
        else if (status === "O") sb.classList.add("won-o");
        else if (status === "D") sb.classList.add("draw");

        // ---------- ACTIVE / FREE PLAY ----------
        if (status === null) {
            if (data.nextBoard === -1 || data.nextBoard === b) {
                sb.classList.add("active");

                if (data.currentPlayer === "X") {
                    sb.classList.add("x-turn");
                } else {
                    sb.classList.add("o-turn");
                }
            }
        }

        // ---------- BIG OVERLAY ----------
        const oldOverlay = sb.querySelector(".board-overlay");
        if (oldOverlay) oldOverlay.remove();

        if (status === "X" || status === "O") {
            const overlay = document.createElement("div");
            overlay.className = `board-overlay ${status}`;
            overlay.innerText = status;
            sb.appendChild(overlay);
        }

        // ---------- CELLS ----------
        for (let c = 0; c < 9; c++) {
            const cell = sb.children[c];
            const val = data.board[b][c];

            cell.innerText = val || "";
            cell.className = "cell";
            if (val) cell.classList.add(val);

            cell.disabled =
                val ||
                status !== null ||
                (data.nextBoard !== -1 && data.nextBoard !== b);
        }
    }

    // ---------- TURN TEXT (FIXED) ----------
    if (data.aiMove) {
        updateTurnText("AI");

        // show next human turn after short delay
        setTimeout(() => {
            updateTurnText(data.currentPlayer);
        }, 900);

        return; // 🔑 prevent overwrite
    }

    updateTurnText(data.currentPlayer);
}



// ===============================
// TURN TEXT
// ===============================
function updateTurnText(symbol) {
    const meta = document.getElementById("game-meta");
    const status = document.getElementById("status");
    if (!meta || !status) return;

    const mode = meta.dataset.mode;
    const p1Name = meta.dataset.p1Name;
    const p2Name = meta.dataset.p2Name;
    const p1Symbol = meta.dataset.p1Symbol;

    if (symbol === "AI") {
        status.innerText = "AI’s move";
        status.className = "status turn-indicator turn-o";
        return;
    }

    if (symbol === p1Symbol) {
        status.innerText = `${p1Name}’s move`;
        status.className = "status turn-indicator turn-x";
    } else {
        status.innerText =
            mode === "ai"
                ? "AI’s move"
                : `${p2Name}’s move`;
        status.className = "status turn-indicator turn-o";
    }
}

// ===============================
// STATUS HELPER
// ===============================
function updateStatus(text) {
    const el = document.getElementById("status");
    if (el) el.innerText = text;
}

// // ===============================
// // RESET GAME
// // ===============================
// function resetGame() {
//     fetch("/reset", { method: "POST" })
//         .then(res => res.json())
//         .then(data => {
//             gameOver = false;
//             renderBoard();
//             updateBoardUI(data);
//             updateStatus("Play in any board");
//         });
// }
function resetGame() {
    fetch("/reset", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            gameOver = false;

            renderBoard();
            updateBoardUI(data);

            updateTurnText(data.currentPlayer);
        });
}


// ===============================
// THEME SYSTEM
// ===============================
const themes = ["theme-blue", "theme-purple", "theme-green", "theme-slate"];

function loadTheme() {
    const saved = localStorage.getItem("theme") || themes[0];
    themes.forEach(t => document.body.classList.remove(t));
    document.body.classList.add(saved);
}

function toggleThemePopup() {
    const popup = document.getElementById("theme-popup");
    if (popup) popup.classList.toggle("hidden");
}

function selectTheme(theme) {
    themes.forEach(t => document.body.classList.remove(t));
    document.body.classList.add(theme);
    localStorage.setItem("theme", theme);

    const popup = document.getElementById("theme-popup");
    if (popup) popup.classList.add("hidden");
}
function showWinnerPopup(winnerSymbol) {
    const modal = document.getElementById("winner-modal");
    const text = document.getElementById("winner-text");
    const meta = document.getElementById("game-meta");

    const mode = meta.dataset.mode;
    const p1Name = meta.dataset.p1Name;
    const p2Name = meta.dataset.p2Name;
    const p1Symbol = meta.dataset.p1Symbol;

    let winnerName;

    if (winnerSymbol === "D") {
        winnerName = "It's a Draw 🤝";
        text.classList.remove("glow");
    } else if (winnerSymbol === p1Symbol) {
        winnerName = `${p1Name} Wins 🎉`;
        text.classList.add("glow");
    } else {
        winnerName =
            mode === "ai"
                ? "AI Wins 🤖"
                : `${p2Name} Wins 🎉`;
        text.classList.add("glow");
    }

    text.innerText = winnerName;
    modal.classList.remove("hidden");
}

function playAgain() {
    fetch("/reset", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            gameOver = false;

            // Hide winner popup
            const modal = document.getElementById("winner-modal");
            if (modal) modal.classList.add("hidden");

            // Reset UI
            renderBoard();
            updateBoardUI(data);
            updateStatus("Play in any board");
        });
}


