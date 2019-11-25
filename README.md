# JaycarAssistant
## An assistant for locating components at Jaycar
### Demo Video
[![Thumbnail of a YouTube Video](https://img.youtube.com/vi/laD6pSP1EGY/0.jpg)](https://www.youtube.com/watch?v=laD6pSP1EGY "Click to Watch on YouTube")
### Configuration
- The Layouts for each type of item are stored as CSV spreadsheets in the CSVs folder, the items are separated using `,` for each new box, `&` for each item in the same box, `|` for the voltage of the item and a newline for each new row
- The CSV spreadsheets can be opened using excel, to make it easier replace `&` with a newline (`Ctrl + J` in the find dialogue or `Shift + Enter` when editing), but replace them back before saving
- `data_file.py` contains the code for reading the CSVs, the pricing, the display message and the colour info
- The main `app.py` shouldn't need to be touched unless you are changing the text
- This branch is preconfigured for Strathpine Jaycar
### Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [Flask](https://pypi.org/project/Flask/)
- [Flask-FontAwesome](https://pypi.org/project/Flask-FontAwesome/)
#### This repo includes
- [Bootstrap](https://getbootstrap.com/)
- [jQuery](https://jquery.com/)