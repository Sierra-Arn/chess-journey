# **Architecture Overview**

## **I. Setup Screen**
— this is the initial application interface designed for configuring chess game parameters before starting the game.

### **i. Main Layout Structure**

The component architecture of the setup screen includes the following elements:

1. **Player Setup Sections** (two `PlayerSetupWidget` components)
    - **White Player Setup** — configuration of parameters for the white player.
    - **Black Player Setup** — configuration of parameters for the black player.

2. **Game Settings**
    - **Game Mode Dropdown** — selection between standard chess and Chess960 variants.
    - **Board Orientation Dropdown** — determination of which color is positioned at the bottom of the board.

3. **"Start Game" Button** — centered control element for launching the game with current settings.

### **ii. Player Setup Widget Components**

Each `PlayerSetupWidget` contains interactive elements for controlling player parameters:

- **Player Type Dropdown** — switching between `HUMAN` and `AI`.
- **Name Input Field** — text field for human player name (disabled for AI).
- **AI Difficulty Slider** — adjustable difficulty level (1–20, disabled for human).
- **Time Control Slider** — setting time limit (1–60 minutes).

### **Dynamic Interface Behavior**

**Adaptive logic** of components ensures setting consistency:
- When `AI` type is selected: **disabling** name field, **enabling** difficulty slider.
- When `HUMAN` type is selected: **enabling** name field, **disabling** difficulty slider.

## **II. Game Screen**
— this is the main application interface where the chess game takes place, considering the settings configured on the previous screen.

### **Key Components**

The central architecture of the game screen includes:

1. **Chess Board Widget** (`ChessBoardWidget`)
    - **Central Interactive Board** — primary field for piece interaction.
    - **Chess960 Support** — automatic synchronization with random starting positions.

2. **Player Timer Widgets** (two `PlayerTimerWidget` components)
    - **White Player Timer** — display of name and countdown timer.
    - **Black Player Timer** — display of name and countdown timer.

3. **Game End Display**
    - **Overlay Label** — visualization of game result after completion.

### **Dynamic Behavior**

**Interactive logic** ensures smooth gameplay:

- **Move Highlighting** — automatic highlighting of selected piece and valid moves.
- **AI Automation** — move calculation scheduling when artificial intelligence is active.
- **Timer Switching** — automatic time update after each move.
- **Completion Checking** — immediate determination and display of game end conditions.