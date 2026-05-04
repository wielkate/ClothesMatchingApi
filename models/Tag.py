from enum import Enum


class Tag(Enum):
    UNKNOWN = "Unknown"
    TOP = "Top" # shirt, blouse, t-shirt
    BOTTOM = "Bottom" # pants, skirt, shorts, jeans
    MID_LAYER = "Mid layer" # sweater, hoodie, jacket
    OUTERWEAR = "Outerwear" # coat, raincoat, trench