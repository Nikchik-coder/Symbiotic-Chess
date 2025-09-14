# Symbiotic Chess

A chess variant where you can merge your pieces to create powerful new units with combined abilities.

## Features

- **Standard Chess Rules**: Implements all the standard rules of chess.
- **Merge Mechanic**: Combine adjacent pieces of different types to create a single, powerful piece with the abilities of both.
- **Disintegrate Mechanic**: Split a merged piece into its original components for tactical flexibility.
- **Special Combined Pieces**: Create unique pieces like the Chancellor (Rook + Knight) and Archbishop (Bishop + Knight).
- **Web-Based UI**: Play the game in your browser with a clean and intuitive interface.
- **API-Based Architecture**: A Flask-based backend provides a RESTful API for game state and actions.

## Project Structure

- **`backend/`**: Contains the Flask server (`server.py`) and the core game logic (`game.py`).
  - **`server.py`**: The main entry point for the backend. It exposes the API endpoints for the game.
  - **`game.py`**: Contains the `SymbioticChessGame` class, which manages the game state and rules.
- **`frontend/`**: Contains the web-based user interface.
  - **`index.html`**: The main HTML file for the game.
  - **`style.css`**: The stylesheet for the game.
  - **`app.js`**: The JavaScript file that handles the game's UI and interaction with the backend.

## How to Launch the Game

There are two ways to launch the game: for playing online with a friend, or for local development.

### Playing Online (Recommended)

This is the easiest way to start a game and share it with someone else.

**1. Prerequisites**

Before launching the game for the first time, you need to set up the environment.

*   **Python Backend:** Navigate to the `backend` directory, create a virtual environment, and install the required Python dependencies:
    ```bash
    cd backend
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    pip install -r ../requirements.txt
    cd ..
    ```

*   **Localtunnel:** You also need to install `localtunnel`, which requires Node.js and npm. If you don't have it, you can install it globally with:
    ```bash
    npm install -g localtunnel
    ```

**2. Launch**

Run the `start_online_game.sh` script. This script is designed for macOS/Linux systems, or Windows systems with a bash-like shell (like Git Bash or WSL).

```bash
./start_online_game.sh
```

This will start the backend and frontend servers and create a public URL for your game. The script will print a link that you can open in your browser and share with a friend.

To stop the game, press `Ctrl+C` in the terminal where you ran the script. This will also execute the `stop_game.sh` script to clean up running processes.

### Local Development Setup

If you want to run the servers manually for development purposes, follow these steps.

**1. Set up the Backend**

First, navigate to the `backend` directory, create a virtual environment, and install the required dependencies (if you haven't already from the 'Playing Online' setup):

```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
# source venv/bin/activate
pip install -r ../requirements.txt
```

Next, start the Flask server:

```bash
python server.py
```

The server will start on `http://127.0.0.1:5000`.

**2. Launch the Frontend**

To launch the frontend, you will need to serve the `frontend` directory on a local web server. The easiest way to do this is with the `Live Server` extension in Visual Studio Code.

Alternatively, you can use Python's built-in HTTP server from the project root:

```bash
# Make sure you are in the root directory of the project
cd frontend
python -m http.server
```

This will start a web server on `http://localhost:8000`.

**3. Play the Game**

Once both the backend and frontend are running, open your web browser and navigate to the address where the frontend is being served (e.g., `http://localhost:8000`). You should see the game board and be able to start playing.

## How to Play

- **To move a piece:** Click on the piece you want to move, and then click on the square you want to move it to.
- **To merge pieces:** Enter the positions of the two pieces you want to merge in the input box (e.g., `e1d1`) and click the "Merge" button.
- **To disintegrate a piece:** Enter the position of the piece you want to disintegrate and the target square in the input box (e.g., `c4b5`) and click the "Disintegrate" button.
- **To reset the game:** Click the "Reset Game" button.