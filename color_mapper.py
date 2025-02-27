import json
from math import sqrt

# Minecraft map colors (base colors from minecraft 1.12+)
MAP_COLORS = {
    0: (0, 0, 0),
    1: (89, 125, 39),
    2: (109, 153, 48),
    3: (127, 178, 56),
    4: (67, 94, 29),
    5: (174, 164, 115),
    6: (213, 201, 140),
    7: (247, 233, 163),
    8: (130, 123, 86),
    9: (140, 140, 140),
    10: (171, 171, 171),
    11: (199, 199, 199),
    12: (105, 105, 105),
    13: (180, 0, 0),
    14: (220, 0, 0),
    15: (255, 0, 0),
    16: (135, 0, 0),
    17: (112, 112, 180),
    18: (138, 138, 220),
    19: (160, 160, 255),
    20: (84, 84, 135),
    21: (117, 117, 117),
    22: (144, 144, 144),
    23: (167, 167, 167),
    24: (88, 88, 88),
    25: (0, 87, 0),
    26: (0, 106, 0),
    27: (0, 124, 0),
    28: (0, 65, 0),
    29: (180, 180, 180),
    30: (220, 220, 220),
    31: (255, 255, 255),
    32: (135, 135, 135),
    33: (115, 118, 129),
    34: (141, 144, 158),
    35: (164, 168, 184),
    36: (86, 88, 97),
    37: (106, 76, 54),
    38: (130, 94, 66),
    39: (151, 109, 77),
    40: (79, 57, 40),
    41: (79, 79, 79),
    42: (96, 96, 96),
    43: (112, 112, 112),
    44: (59, 59, 59),
    45: (45, 45, 180),
    46: (55, 55, 220),
    47: (64, 64, 255),
    48: (33, 33, 135),
    49: (100, 84, 50),
    50: (123, 102, 62),
    51: (143, 119, 72),
    52: (75, 63, 38),
    53: (180, 177, 172),
    54: (220, 217, 211),
    55: (255, 252, 245),
    56: (135, 133, 129),
    57: (152,  89,  36),
    58: (186, 109,  44),
    59: (216, 127,  51),
    60: (114,  67,  27),
    61: (125,  53, 152),
    62: (153,  65, 186),
    63: (178,  76, 216),
    64: ( 94,  40, 114),
    65: ( 72, 108, 152),
    66: ( 88, 132, 186),
    67: (102, 153, 216),
    68: ( 54,  81, 114),
    69: (161, 161,  36),
    70: (197, 197,  44),
    71: (229, 229,  51),
    72: (121, 121,  27),
    73: ( 89, 144,  17),
    74: (109, 176,  21),
    75: (127, 204,  25),
    76: ( 67, 108,  13),
    77: (170,  89, 116),
    78: (208, 109, 142),
    79: (242, 127, 165),
    80: (128,  67,  87),
    81: ( 53,  53,  53),
    82: ( 65,  65,  65),
    83: ( 76,  76,  76),
    84: ( 40,  40,  40),
    85: (108, 108, 108),
    86: (132, 132, 132),
    87: (153, 153, 153),
    88: ( 81,  81,  81),
    89: ( 53,  89, 108),
    90: ( 65, 109, 132),
    91: ( 76, 127, 153),
    92: ( 40,  67,  81),
    93: ( 89,  44, 125),
    94: (109,  54, 153),
    95: (127,  63, 178),
    96: ( 67,  33,  94),
    97: ( 36,  53, 125),
    98: ( 44,  65, 153),
    99: ( 51,  76, 178),
    100: ( 27,  40,  94),
    101: ( 72,  53,  36),
    102: ( 88,  65,  44),
    103: (102,  76,  51),
    104: ( 54,  40,  27),
    105: ( 72,  89,  36),
    106: ( 88, 109,  44),
    107: (102, 127,  51),
    108: ( 54,  67,  27),
    109: (108,  36,  36),
    110: (132,  44,  44),
    111: (153,  51,  51),
    112: ( 81,  27,  27),
    113: ( 17,  17,  17),
    114: ( 21,  21,  21),
    115: ( 25,  25,  25),
    116: ( 13,  13,  13),
    117: (176, 168,  54),
    118: (215, 205,  66),
    119: (250, 238,  77),
    120: (132, 126,  40),
    121: ( 64, 154, 150),
    122: ( 79, 188, 183),
    123: ( 92, 219, 213),
    124: ( 48, 115, 112),
    125: ( 52,  90, 180),
    126: ( 63, 110, 220),
    127: ( 74, 128, 255),
    128: ( 39,  67, 135),
    129: (  0, 153,  40),
    130: (  0, 187,  50),
    131: (  0, 217,  58),
    132: (  0, 114,  30),
    133: ( 91,  60,  34),
    134: (111,  74,  42),
    135: (129,  86,  49),
    136: ( 68,  45,  25),
    137: ( 79,   1,   0),
    138: ( 96,   1,   0),
    139: (112,   2,   0),
    140: ( 59,   1,   0),
    141: (147, 124, 113),
    142: (180, 152, 138),
    143: (209, 177, 161),
    144: (110,  93,  85),
    145: (112,  57,  25),
    146: (137,  70,  31),
    147: (159,  82,  36),
    148: ( 84,  43,  19),
    149: (105,  61,  76),
    150: (128,  75,  93),
    151: (149,  87, 108),
    152: ( 78,  46,  57),
    153: ( 79,  76,  97),
    154: ( 96,  93, 119),
    155: (112, 108, 138),
    156: ( 59,  57,  73),
    157: (131,  93,  25),
    158: (160, 114,  31),
    159: (186, 133,  36),
    160: ( 98,  70,  19),
    161: ( 72,  82,  37),
    162: ( 88, 100,  45),
    163: (103, 117,  53),
    164: ( 54,  61,  28),
    165: (112,  54,  55),
    166: (138,  66,  67),
    167: (160,  77,  78),
    168: ( 84,  40,  41),
    169: ( 40,  28,  24),
    170: ( 49,  35,  30),
    171: ( 57,  41,  35),
    172: ( 30,  21,  18),
    173: ( 95,  75,  69),
    174: (116,  92,  84),
    175: (135, 107,  98),
    176: ( 71,  56,  51),
    177: ( 61,  64,  64),
    178: ( 75,  79,  79),
    179: ( 87,  92,  92),
    180: ( 46,  48,  48),
    181: ( 86,  51,  62),
    182: (105,  62,  75),
    183: (122,  73,  88),
    184: ( 64,  38,  46),
    185: ( 53,  43,  64),
    186: ( 65,  53,  79),
    187: ( 76,  62,  92),
    188: ( 40,  32,  48),
    189: ( 53,  35,  24),
    190: ( 65,  43,  30),
    191: ( 76,  50,  35),
    192: ( 40,  26,  18),
    193: ( 53,  57,  29),
    194: ( 65,  70,  36),
    195: ( 76,  82,  42),
    196: ( 40,  43,  22),
    197: (100,  42,  32),
    198: (122,  51,  39),
    199: (142,  60,  46),
    200: ( 75,  31,  24),
    201: ( 26,  15,  11),
    202: ( 31,  18,  13),
    203: ( 37,  22,  16),
    204: ( 19,  11,   8),
    205: (133,  33,  34),
    206: (163,  41,  42),
    207: (189,  48,  49),
    208: (100,  25,  25),
    209: (104,  44,  68),
    210: (127,  54,  83),
    211: (148,  63,  97),
    212: ( 78,  33,  51),
    213: ( 64,  17,  20),
    214: ( 79,  21,  25),
    215: ( 92,  25,  29),
    216: ( 48,  13,  15),
    217: ( 15,  88,  94),
    218: ( 18, 108, 115),
    219: ( 22, 126, 134),
    220: ( 11,  66,  70),
    221: ( 40, 100,  98),
    222: ( 50, 122, 120),
    223: ( 58, 142, 140),
    224: ( 30,  75,  74),
    225: ( 60,  31,  43),
    226: ( 74,  37,  53),
    227: ( 86,  44,  62),
    228: ( 45,  23,  32),
    229: ( 14, 127,  93),
    230: ( 17, 155, 114),
    231: ( 20, 180, 133),
    232: ( 10,  95,  70),
    233: ( 70,  70,  70),
    234: ( 86,  86,  86),
    235: (100, 100, 100),
    236: ( 52,  52,  52),
    237: (152, 123, 103),
    238: (186, 150, 126),
    239: (216, 175, 147),
    240: (114, 92, 77),
    241: (89, 117, 105),
    242: (109, 144, 129),
    243: (127, 167, 150),
    244: (67, 88, 79),
}