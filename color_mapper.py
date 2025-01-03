import json
from math import sqrt

# Minecraft map colors (base colors from minecraft 1.12+)
MAP_COLORS = {
    "air": (0, 0, 0),
    "grass": (127, 178, 56),
    "sand": (247, 233, 163),
    "wool": (199, 199, 199),
    "fire": (255, 0, 0),
    "ice": (160, 160, 255),
    "metal": (167, 167, 167),
    "plant": (0, 124, 0),
    "snow": (255, 255, 255),
    "clay": (164, 168, 184),
    "dirt": (151, 109, 77),
    "stone": (112, 112, 112),
    "water": (64, 64, 255),
    "wood": (143, 119, 72),
    "quartz": (255, 252, 245),
    "orange": (216, 127, 51),
    "magenta": (178, 76, 216),
    "light_blue": (102, 153, 216),
    "yellow": (229, 229, 51),
    "lime": (127, 204, 25),
    "pink": (242, 127, 165),
    "gray": (76, 76, 76),
    "silver": (153, 153, 153),
    "cyan": (76, 127, 153),
    "purple": (127, 63, 178),
    "blue": (51, 76, 178),
    "brown": (102, 76, 51),
    "green": (102, 127, 51),
    "red": (153, 51, 51),
    "black": (25, 25, 25),
}