# Timer Pong

A physics-based bouncing ball simulation with interactive paddles and a timer.

## Project Description

The **Timer Pong** is an interactive game where balls bounce around within a defined screen boundary, interacting with paddles and walls. Users control two paddles to keep the balls in play within the time limit.

Features:
- **Physics-based Ball Motion:** Balls move and collide with walls, paddles, using realistic physics.
- **Two Paddles:** One controlled with arrow keys, the other with `A` and `D` keys.
- **Game Timer:** A countdown timer when it reach 0 the game will end in a draw.
- **Background:** The simulation uses a custom background.
- **Game Over and Restart Mechanism:** A clear message appears when time runs out or a ball exits the boundary, with the option to restart.

## How to Install and Run the Project

Ensure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

## Usage

link here

## Project design and implementation

![image](https://github.com/user-attachments/assets/efb06c88-3861-495a-93f3-676d89d585f1)

## Class Descriptions and Interactions

### Ball
- Purpose: Represents a ball in the simulation. It handles:
  - Movement based on its velocity (`vx`, `vy`).
  - Collisions with walls, other balls, and paddles.
  - Drawing itself on the screen using Turtle graphics.

 Interactions:
- Interacts with the `BouncingSimulator` to simulate motion and collisions.
- Collaborates with `Paddle` to detect collisions and bounce off paddles.
- Updates its state (position, velocity) based on time and interactions.


### Paddle
- Purpose: Represents a paddle in the simulation. It handles:
  - Movement controlled by the user.
  - Collision detection with balls.

 Interactions:
- Controlled by the `BouncingSimulator` via player input (keyboard).
- Detects and responds to `Ball` collisions.
- Draws itself on the screen using Turtle graphics.


### Event
- Purpose: Represents an event that happens at a specific time during the simulation. This could be:
  - A ball collision.
  - A redraw of the screen.

 Interactions:
- Managed by the `BouncingSimulator` using a priority queue (`heapq`).
- Contains references to the `Ball` and/or `Paddle` objects involved in the event.
- Ensures the event is valid based on the current state of the objects involved (checked via `is_valid()`).


### GameTimer
- Purpose: Tracks and displays the remaining time in the game.

 Interactions:
- Integrated into the `BouncingSimulator` to manage the overall game time.
- Displays the time left on the screen.
- Triggers game over when time reaches zero.


### GameOverScreen
- Purpose: Displays messages when the game ends, such as:
  - "Game Over"
  - "Time's Up! It's a Draw!"
- Allows the player to restart the game by pressing a key.

 Interactions:
- Controlled by the `BouncingSimulator` to show game-over messages.
- Listens for the restart key (`'R'`) to reset the simulation and start a new game.


### BouncingSimulator
- Purpose: The core class of the simulation. It coordinates the entire game:
  - Manages all `Ball` and `Paddle` objects.
  - Handles events (using the `Event` class) to predict and resolve interactions.
  - Tracks the game time using `GameTimer`.
  - Responds to user input for paddle movement.
  - Ends the game when conditions (time limit or collision) are met.

 Interactions:
- Creates and manages `Ball`, `Paddle`, `GameTimer`, and `GameOverScreen` objects.
- Uses the `Event` class to predict, schedule, and process future events (collisions, screen redraws).
- Responds to user input for moving paddles (via keyboard).
- Ends the game when time runs out or when a ball hits the bottom wall.
- Uses `GameOverScreen` to display messages and handle game restarts.

## Code Modifications and Extensions

### 1. Added a Second Paddle
- Extended the `Paddle` class to support two paddles: one controlled by the arrow keys and the other by `A`/`D`.
- Modified `BouncingSimulator` to manage two paddles independently.

### 2. Game Over on Horizontal Wall Collision
- Updated the `Ball` class to detect when it hits the horizontal (top or bottom) walls.
- Integrated a "Game Over" state into `BouncingSimulator` when such collisions occur.

### 3. Added Restart Functionality
- Created a `GameOverScreen` class to display "Game Over" or "Draw" messages.
- Implemented a restart mechanism in `BouncingSimulator` to reset the game state when the user presses `R`.

### 4. Implemented a Timer
- Added the `GameTimer` class to track the game duration.
- Integrated the timer into `BouncingSimulator` to end the game in a draw when the timer reaches zero.

### 5. Background
- Added a custom background in `BouncingSimulator`.

