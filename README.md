# SpaceReps
## About
This project is my attempt at replicating existing spaced repitition flashcard software.
Full functionality is currently supported for the command line with Python.
This project is currently being expanded into a web app with HTML, CSS, JavaScript, and a backend Python API.
SpaceReps does not provide any functionality that existing similar software does not.
I created this for three reasons:
1. I find this format more efficient for my study habits than using flashcard apps.
2. I want to expand my JavaScript and web development skills.
3. I really enjoy the challenge of seeing how well I can remake things.

## Usage guide
*Command Line*

After cloning, you can execute `python spacereps_command_line_program.py` from the main `spacereps` project folder to run the program.

*Web App*

After cloning, install `poetry` and `npm`, then run `poetry install` and `npm install`. Once the dependencies have installed, run `npm start`, open a web browser, and navigate to `http://localhost:8090`.
If you make changes and don't see them reflected upon refreshing the browser, hit Ctrl + Shift + R or Command + Shift + R

## Upcoming features:
- Expansion of the web app, including:
    - The ability to modify decks and the cards within them
    - More API endpoints representing existing functionality in the command line program
    - More visually appealing layout with CSS

## Possible room for expansion:
- Back the app with a database and enable user accounts to store data remotely
- Automatic deck generation via AI or Natural Language Processing models
