# importing easygui module
from easygui import *

# message to be displayed
text = "Select which lists to include the member:"

# window title
title = "Twitter Lists Adder"

# item choices
choices = ["nba", "nfl", "futebol"]

# creating a multi choice box
output = multchoicebox(text, title, choices)
test = mul
print(output)