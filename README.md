# **Chess Journey: Python Chess Game with Custom GUI and AI**

A completely reworked school project, created based on the tutorial series ["Chess Engine in Python" by Eddie Sharick](https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_).

This project implements chess rules logic using the [python-chess](https://github.com/niklasf/python-chess) library, custom graphical user interface (GUI) components using [pygame-ce](https://github.com/pygame-community/pygame-ce) and [pygame-gui](https://github.com/MyreMylar/pygame_gui), configuration management via [Pydantic Settings](https://github.com/pydantic/pydantic-settings), as well as integration with the powerful [Stockfish](https://stockfishchess.org/) chess engine (allowing you to play both against the computer and on your own).

> [!NOTE]  
**This repository is archived.** See [End of Journey](#end-of-journey) for context.

## **Available Documentation**

- [English Documentation](README.md) (current document).
- [Документация на русском языке](README_RU.md).

## **Project Structure**

```bash
.
├── docs/
│   ├── architecture_en.md      # Detailed system architecture documentation (in English)
│   ├── architecture_ru.md      # Detailed system architecture documentation (in Russian)
│   └── journey-learnings.md    # Key learnings obtained during development (Russian only)
└── src/
    ├── chess_game/             # Source code of the fully reworked chess game
    └── legacy/                 # Original tutorial code for memory
```

## **Quick Start**

### **Prerequisites**
- Package manager [Pixi](https://pixi.sh/latest/).

### **Installation and Running**

1. **Clone the repository**
    ```bash
    git clone https://github.com/Sierra-Arn/chess-journey.git  
    cd chess-journey
    ```

2. **Install dependencies**
   ```bash
   pixi install
   ```

3. **Set up environment configuration**
   ```bash
   pixi run copy-env
   ```

4. **Set up Stockfish**
    - Download the appropriate [Stockfish binary](https://stockfishchess.org/download/) for your platform.
    - Place the file in the `src/chess_game/assets/stockfish/` directory.
    - Update the file path in the `.env` configuration file if necessary.

5. **Run the chess game**
    ```bash
    pixi run launch-chess-game
    ```
    If you want to better understand the architecture, check out the [architecture documentation](docs/architecture_en.md).

6. **[Optional] Run the original code**
    ```bash
    pixi run setup-legacy-images
    pixi run launch-legacy-code
    ```

## **License**

This project is distributed under the [BSD-3-Clause License](LICENSE).

## **Known Issues**

- **Castling in Chess960**  
Castling in Chess960 variants does not work due to input handling conflicts in the graphical interface. Chess960 castling requires moving the king to the rook's square, but the current mouse click handler selects the rook piece on that square instead of processing it as a valid destination square for the king's move, preventing castling from occurring. However, when the AI makes a castling move, it works correctly since the AI uses the python-chess library directly.

- **GameScreen.update()**  
The `update()` method is never explicitly called in the code, but for some reason it is necessary for proper timer display. Removing this unused method breaks the timer's ability to properly display current time values.

- **AI Settings**  
Text input fields can be clicked when AI settings are active (visual bug, text input does not occur).

## **Possible Improvements**

- **Enhanced Slider Interface**  
Sliders currently do not display their current numeric values. It would be great to add visual feedback showing the current value, and ideally update the displayed value in real-time while dragging the slider, providing immediate feedback on parameter adjustments.

- **Move Logging**  
Implement proper game move logging and display in standard chess notation. The original tutorial code had basic move display functionality, but this feature was intentionally omitted in the rework to focus on core architectural improvements. Adding this functionality would restore the full game history for users.

- **Robust Error Handling**  
Add proper validation of user settings and implement comprehensive `None` checking throughout the code to improve application stability.

- **Full Pawn Promotion**  
Expand pawn promotion to support all piece types in addition to the queen.

- **Proper UI Layout Management**  
Replace hardcoded positions, sizes, and margins with a proper layout system for widgets and screens.

- **PyGame GUI Themes**  
Add PyGame GUI themes to enhance visual design and user experience.

## **End of Journey**

This project was never intended to be a finished chess application. It was created as an educational project, with the goal of learning through practice. The project initially aimed to create a minimal viable product (MVP) demonstrating modern Python development practices, object-oriented architecture, and integration with modern libraries such as `python-chess`, `pygame-ce`, and `pygame_gui`.

The **Known Issues** and **Possible Improvements** described above were deliberately left unfixed as conscious decisions made in the spirit of rapid development. Moreover, creating a full-featured game in PyGame implies using Python, and choosing Python for games is questionable when specialized high-performance alternatives like [Godot](https://github.com/godotengine/godot) exist for serious game development.