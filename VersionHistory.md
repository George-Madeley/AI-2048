# Version History

## v1.3 Improving the Scoring Algorithm

### 1.3.4

- Added code to Compare which spots errors related to two tile spawns (only one tile should spawn). Asks user to correct mistake.
- First successful finish of program.

### 1.3.3

- Improved `DifferenceInLog2` algorithm.
- Improved array comparison.

### 1.3.2

- The state children generation bug has been fixed.
- New color values have been generated.

### 1.3.1

- `GetBestChildStateScore` ammended to find either the highest or lowest score in the tree.
- `DifferenceInLog2` has been implimented which scores the game state based on the difference between each tiles log2 value.

### 1.3.0

- Fixed issue where the same redundant move is made repeatedly without progressing the game.

## v1.2 Unsupervised Learning

### v1.2.1

- `app.py` now compares the read array to the predicted array.
- Any colors of known values that are not in the known color list are automatically added.
- Any misread values are checked and their color is added to the color list.
- add .gitignore file.

### v1.2.0

- `graph.py` now sorts the color csv file in order of the tile value.
- `graph.py` now removes duplicate values from color.csv to color-copy.csv.

## v1.1 Game States

### v1.1.4

- Added more color data to 512.

### v1.1.3

- Fixed issue where agent remakes same move even though the outcome is the same.

### v1.1.2

- Agent has methods of searching the state tree to find leaf with best score.

### v1.1.1

- Fixed error in left and right child state generation.
- States have two methods of calculating their score.

### v1.1.0

- Created `state.py` with `GameState` class.
- `GameState` can generate children game states for each move made.

## v1.0 Basic Functionality

### v1.0.10

- Clean up.
- Documentation.

### v1.0.9

- Created `graph.py` to graph the feature vectors from color.csv to a 3D graph.

### v1.0.8

- Replaceced Nearest Centroid with K-Nearest Neighbor.
- Add more data to the Color.csv file.

### v1.0.7

- Added `launch.json`.
- Fixed errors in `ReadColorFile()` in `streamio.py`.
- Create `ClickMouse()` function in `interface.py` which clicks the mouse at a given location.
- floored the identified color values.
- `GetTileNumber()` now asks the user to iudentify the color if it is not reconised.

### v1.0.6

- Created the `app.py` file.
- Created the base functions in `app.py` to run the agent, read the screen, and record data.
- Updated `appsettings.json` to include url.
- Renamed `record.py` to `streamio.py`.
- Updated `streamio.py` with comments and renamed functions.
- Created base for `agent.py`.

### v1.0.5

- Added the functionality to read the config file.
- Added the functionality to read the colors csv file.
- Added the functionality to append to the colors csv file.

### v1.0.4

- Fixed some errors.

### v1.0.3

- Added functionality to press up, down, left, and right arrow keys.

### v1.0.2

- Created `interface.py`
- Created `appsettings.json`
- Created `colors.csv`
- Added functionality to take screenshot.
- Added functionality to read data from screenshots.

### v1.0.1

- Created `record.py`.
- Added functionality to record to CSV file.

### v1.0.0

- Initialised Repo
