# Hangman Game System

This repository contains a Hangman game system implemented with a Flask server and a Python client using the `requests` library. The system manages user registration, authentication, and gameplay for registered users.

## Features

1. **User Management**:
   - Each user has the following attributes:
     - Name
     - ID
     - Password
     - Number of games played
     - Unique words that appeared in previous games
     - Number of wins
   - User data is stored persistently in a file.

2. **Authentication**:
   - Only registered users can play the game.
   - Unregistered users are prompted to register.
   - Users must log in to play.
   - Sessions last for 10 minutes, after which users must log in again.

3. **Word Management**:
   - The server maintains a word bank in a file.
   - Words are randomly selected for each game.

4. **Gameplay**:
   - The game logic is handled on the client side.
   - The client interacts with the server for user authentication, word retrieval, and game result updates.

## Project Structure

```
MyClientSide/
    funcs.py          # Client-side logic for user interaction and gameplay
    hangMan.py        # Hangman graphics for the game
    logo.py           # ASCII logo for the game
    main.py           # Entry point for the client
    bad.mp3           # Sound for incorrect guesses
    good.mp3          # Sound for correct guesses
    __pycache__/      # Compiled Python files
    .idea/            # IDE configuration files

pythonProject-Server/
    main.py           # Flask server implementation
    player.py         # User management class
    players.txt       # Persistent storage for user data
    words.txt         # Word bank for the game
    __pycache__/      # Compiled Python files
    .idea/            # IDE configuration files
```

## How to Run

### Server
1. Navigate to the `pythonProject-Server` directory.
2. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```
3. Start the server:
   ```bash
   python main.py
   ```

### Client
1. Navigate to the `MyClientSide` directory.
2. Install dependencies:
   ```bash
   pip install requests pygame colorama
   ```
3. Start the client:
   ```bash
   python main.py
   ```

## System Requirements

- Python 3.9 or higher for the server.
- Python 3.11 or higher for the client.
- Flask and Flask-CORS for the server.
- Requests, Pygame, and Colorama for the client.

## Gameplay Instructions

1. Run the server and client as described above.
2. Follow the prompts on the client to:
   - Register as a new user.
   - Log in with your credentials.
   - Play the Hangman game.
3. After 10 minutes, you will need to log in again to continue playing.

## Notes

- The server uses cookies to manage user sessions.
- The client plays sounds for correct and incorrect guesses.
- The game tracks user statistics, including the number of games played, unique words encountered, and wins.

Enjoy the game!
