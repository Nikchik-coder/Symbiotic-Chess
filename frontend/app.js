const API_URL = 'http://127.0.0.1:5000';
let selectedSquares = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchGameState();
    document.getElementById('move-button').addEventListener('click', handleMove);
    document.getElementById('merge-button').addEventListener('click', handleMerge);
    document.getElementById('disintegrate-button').addEventListener('click', handleDisintegrate);
    document.getElementById('reset-button').addEventListener('click', handleReset);
});

async function fetchGameState() {
    try {
        const response = await fetch(`${API_URL}/state`);
        const state = await response.json();
        renderBoard(state);
    } catch (error) {
        console.error('Error fetching game state:', error);
    }
}

function renderBoard(state) {
    const chessboard = document.getElementById('chessboard');
    chessboard.innerHTML = '';
    
    // Create labels
    createLabels();

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 0 ? 'light' : 'dark');
            square.dataset.row = row;
            square.dataset.col = col;
            
            const piece = state.board[row][col];
            if (piece) {
                square.innerHTML = getPieceSymbol(piece);
                square.classList.add('piece');
                square.style.color = piece.color === 'white' ? '#fff' : '#000';
            }
            
            square.addEventListener('click', () => handleSquareClick(row, col));
            chessboard.appendChild(square);
        }
    }
    
    updateGameInfo(state);
}

function createLabels() {
    const rankLabels = document.getElementById('rank-labels');
    const fileLabels = document.getElementById('file-labels');
    rankLabels.innerHTML = '';
    fileLabels.innerHTML = '';

    for (let i = 0; i < 8; i++) {
        const rank = document.createElement('div');
        rank.innerText = 8 - i;
        rankLabels.appendChild(rank);

        const file = document.createElement('div');
        file.innerText = String.fromCharCode('a'.charCodeAt(0) + i);
        fileLabels.appendChild(file);
    }
}

function getPieceSymbol(piece) {
    const symbols = {
        'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
        'A': 'A', 'C': 'C', 'M': 'M', 'G': 'G'
    };
    
    const [displayType, isSpecial] = piece.display_info;
    let symbol = symbols[displayType.toUpperCase()] || '?';
    
    if (piece.combined_pieces.length > 0 && !isSpecial) {
        symbol += '+';
    }
    
    return symbol;
}


function handleSquareClick(row, col) {
    const algebraic = colRowToAlgebraic(col, row);
    const moveInput = document.getElementById('move-input');
    
    if (selectedSquares.length === 0) {
        selectedSquares.push(algebraic);
        highlightSquare(row, col, true);
    } else if (selectedSquares.length === 1) {
        selectedSquares.push(algebraic);
        moveInput.value = selectedSquares.join('');
        handleMove();
    }
}

function highlightSquare(row, col, isSelected) {
    const square = document.querySelector(`.square[data-row='${row}'][data-col='${col}']`);
    if (isSelected) {
        square.classList.add('selected');
    } else {
        square.classList.remove('selected');
    }
}

function colRowToAlgebraic(col, row) {
    const file = String.fromCharCode('a'.charCodeAt(0) + col);
    const rank = 8 - row;
    return `${file}${rank}`;
}

async function handleMove() {
    const move = document.getElementById('move-input').value;
    if (move.length === 4) {
        await fetch(`${API_URL}/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ move })
        });
        resetSelection();
        fetchGameState();
    }
}

async function handleMerge() {
    const move = document.getElementById('move-input').value;
    if (move.length === 4) {
        const pos1 = move.substring(0, 2);
        const pos2 = move.substring(2, 4);
        await fetch(`${API_URL}/merge`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pos1, pos2 })
        });
        resetSelection();
        fetchGameState();
    }
}

async function handleDisintegrate() {
    const move = document.getElementById('move-input').value;
    if (move.length === 4) {
        const pos = move.substring(0, 2);
        const target_pos = move.substring(2, 4);
        await fetch(`${API_URL}/disintegrate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pos, target_pos })
        });
        resetSelection();
        fetchGameState();
    }
}

async function handleReset() {
    await fetch(`${API_URL}/reset`, { method: 'POST' });
    resetSelection();
    fetchGameState();
}

function resetSelection() {
    document.getElementById('move-input').value = '';
    selectedSquares = [];
    document.querySelectorAll('.square.selected').forEach(s => s.classList.remove('selected'));
}

function updateGameInfo(state) {
    document.getElementById('turn-display').innerText = `${state.current_turn.charAt(0).toUpperCase() + state.current_turn.slice(1)}'s Turn`;
    document.getElementById('status-message').innerText = state.status_message;
    document.getElementById('last-move').innerText = state.last_move ? `Last move: ${state.last_move}` : '';
    
    const whiteCaptured = document.getElementById('captured-by-white');
    whiteCaptured.innerHTML = state.captured_pieces.black.map(getPieceSymbol).join(' ');

    const blackCaptured = document.getElementById('captured-by-black');
    blackCaptured.innerHTML = state.captured_pieces.white.map(getPieceSymbol).join(' ');
}
