# System Override

**System Override** is a puzzle-platformer game built in Python using Pygame. Navigate through challenging levels, activate switches, reveal hidden doors, and reach the exit. The game combines logic, timing, and strategy, with visual feedback through green tiles and hidden obstacles.

---

## 🕹️ Features

- **Switch & Door Mechanics:** Press switches to reveal doors and unlock paths.  
- **Green Tile Feedback:** Switches illuminate green tiles when activated for visual guidance.  
- **Hidden Obstacles:** Some walls and doors are hidden, adding puzzle complexity.  
- **Timed Levels:** Each level has a countdown timer to increase challenge.  
- **Multiple Levels:** Includes 15 handcrafted levels with increasing difficulty.  
- **Simple Controls:** Move with `WASD` and interact with switches using `SPACE`.  

---

## 🎮 Installation & Running

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/system-override.git
   cd system-override
````

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # macOS/Linux
   ```

3. **Install Pygame:**

   ```bash
   pip install pygame
   ```

4. **Run the game:**

   ```bash
   python main.py
   ```

---

## 🕹️ Controls

* **Move Player:** `W` = Up, `A` = Left, `S` = Down, `D` = Right
* **Activate Switch:** `SPACE`

---

## 📂 Project Structure

```
system-override/
├── main.py        # Game entry point
├── objects.py     # Game objects: Wall, Door, Switch, Exit, GreenTile
├── player.py      # Player movement logic
├── levels.py      # Level definitions
├── README.md      # Project documentation
└── venv/          # Virtual environment (optional)
```

---

## 🛠️ Next Steps / Future Improvements

* Add **timed switches** and **moving obstacles** for more challenge.
* Implement **enemy AI** or **hazard zones**.
* Expand **level designs** to increase gameplay time.
* Enhance **UI/HUD** with score tracking, sound effects, and animations.
* Include **save/load functionality** and level progression.
