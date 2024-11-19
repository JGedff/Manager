from PyQt5.QtGui import QColor

# Calculate relative luminance
def get_contrast_color(baseHex):
    # Relative luminance formula sRGB: Light = 0.2126×R + 0.7152×G + 0.0722×B
    base_color = QColor(baseHex)

    luminance = (0.2126 * base_color.redF() +
                    0.7152 * base_color.greenF() +
                    0.0722 * base_color.blueF())
    return "#000000" if luminance > 0.5 else "#FFFFFF"

# Change color light by factor
def darken_color(colorHex, factor):
    # If factor == 1, it remains unchanged. If factor == 0.8, it will be 20% darker
    color = QColor(colorHex)

    darkened_color = QColor(
        max(0, int(color.red() * factor)),
        max(0, int(color.green() * factor)),
        max(0, int(color.blue() * factor))
    )
    return darkened_color.name()

def getStyleSheet(colorHex):
    return f"""
        QPushButton {{
            background-color: {colorHex};
            border: 1px solid {darken_color(colorHex, 0.7)};
            color: {get_contrast_color(colorHex)};
        }}
        QPushButton:hover {{
            background-color: {darken_color(colorHex, 0.95)};
            border: 1px solid {darken_color(colorHex, 0.65)};
            color: {get_contrast_color(darken_color(colorHex, 0.95))};
        }}
        QPushButton:pressed {{
            background-color: {darken_color(colorHex, 0.9)};
            border: 1px solid {darken_color(colorHex, 0.6)};
            color: {get_contrast_color(darken_color(colorHex, 0.9))};
        }}
    """