import tkinter as tk

def apply_style(widget, style_type):
    """Applies consistent styling to Tkinter widgets."""
    styles = {
        "button": {"bg": "#1DB954", "fg": "#FFFFFF", "font": ("Arial", 12, "bold"), "padx": 10, "pady": 5},
        "label": {"bg": "#121212", "fg": "#E0E0E0", "font": ("Arial", 12)},
        "entry": {"bg": "#FFFFFF", "fg": "#000000", "font": ("Arial", 12), "width": 20}
    }

    if style_type in styles:
        for key, value in styles[style_type].items():
            widget[key] = value

def apply_dark_theme(root):
    """Applies a dark theme to the entire Tkinter window."""
    root.configure(bg="#121212")
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            apply_style(widget, "label")