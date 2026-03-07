# Tic Tac Toe – AI-Powered Web Game

A web-based Tic Tac Toe game built with **Flask** and **Python**, featuring **PvP** and **AI modes** with adjustable difficulty. The game supports real-time moves, session-based settings, and a dynamic user interface.  

---

## Features

- **Player vs Player (PvP)** mode  
- **Player vs AI** mode with difficulty levels: easy, medium, hard  
- Session-based settings: player names, symbols, difficulty  
- Real-time game moves and board updates  
- Game reset functionality  
- Interactive front-end using Flask templates  

---

## Technologies Used

- **Backend:** Flask, Python  
- **Frontend:** HTML, CSS, JavaScript  
- **Game Logic:** Minimax-based AI for smart moves  

---

## Getting Started

### 1. Clone the repository  
```bash
git clone https://github.com/yourusername/tic-tac-toe.git
cd tic-tac-toe
```
### 2. Create a virtual environment and activate it
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate  
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the app
```bash
python app.py
```
### Folder Structure
```bash
tic-tac-toe/
│
├─ app.py                 # Main Flask application
├─ game.py                # Game logic for Tic Tac Toe
├─ ai.py                  # AI move calculation
├─ templates/             # HTML templates
│   ├─ home.html
│   ├─ game.html
│   └─ settings.html
├─ static/                # CSS & JS files
├─ requirements.txt       # Python dependencies
└─ README.md              # Project documentation  
```
## How to Play
- Open the game in a browser.
- Choose PvP (Player vs Player) or PvAI (Player vs AI).
- Set player names, symbols, and AI difficulty (if applicable).
- Click on cells to make moves; the game automatically switches turns.
- The game detects a winner or tie and allows resetting.
