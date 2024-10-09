import os
# TODO
"""
* change connectinos bugged to blobfish first time form is submited as node 2
* in view connections show a <- and -> button to toggle different views like viewing characters, names, levels
* add character main to player info
* come up with a good definition for friends
* better graph visual
* google form to gather data and easy way to fill add form data. Q1 Your name, Q2 Your main, Q3 Your level, Q4 Your friends
* google doc or something to show image
* if possible auto update graph images from script
* seperate pages and scripts
* Homepage Describing the project. Shows how many people have been added
* create a validate structure test thing to prevent issues

* Interactive graph
* lore about person
* hover node = Highlight node and neighbors
"""

if __name__ == "__main__":
    app_dir = r"\src\GUI\Homepage.py"
    current_dir = os.getcwd()
    os.system(f"streamlit run {current_dir}{app_dir}")

