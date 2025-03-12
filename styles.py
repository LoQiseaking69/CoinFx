# styles.py - Defines UI colors, fonts, and reusable widget styling

GUI_THEME = {
    "bg_color": "#121212",  # Dark Mode Background
    "fg_color": "#E0E0E0",  # Text Color
    "button_color": "#1DB954",  # Green for Start/Stop Trading
    "error_color": "#E53935",  # Red for Alerts
    "font": ("Arial", 12),
}

def apply_style(widget, style_type="default"):
    """Applies a predefined style to a Tkinter widget."""
    styles = {
        "default": {"bg": GUI_THEME["bg_color"], "fg": GUI_THEME["fg_color"], "font": GUI_THEME["font"]},
        "button": {"bg": GUI_THEME["button_color"], "fg": "#FFFFFF", "font": GUI_THEME["font"], "padx": 10, "pady": 5},
        "error": {"bg": GUI_THEME["error_color"], "fg": "#FFFFFF", "font": GUI_THEME["font"], "padx": 10, "pady": 5},
    }
    widget.config(**styles.get(style_type, styles["default"]))