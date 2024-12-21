from enum import Enum

class Theme(Enum):
    LIGHT = {
        'background': '#ffffff',  # White background
        'button_bg': '#f0f0f0',  # Light gray button background
        'button_fg': '#000000',  # Black text
        'border': '#cccccc',     # Light gray border
        'hover': '#e0e0e0',      # Slightly darker gray for hover
        'button_active': '#d0d0d0',  # Even darker gray for active state
        'toggle_bg': '#4CAF50',  # Green for toggle buttons
        'toggle_fg': '#ffffff',  # White text for toggle buttons
        'x_color': '#2196F3',    # Blue for X
        'o_color': '#f44336'     # Red for O
    }
    
    DARK = {
        'background': '#2c2c2c',  # Dark gray background
        'button_bg': '#3c3c3c',  # Slightly lighter gray button background
        'button_fg': '#ffffff',  # White text
        'border': '#1c1c1c',     # Darker gray border
        'hover': '#4c4c4c',      # Lighter gray for hover
        'button_active': '#5c5c5c',  # Even lighter gray for active state
        'toggle_bg': '#4CAF50',  # Green for toggle buttons
        'toggle_fg': '#ffffff',  # White text for toggle buttons
        'x_color': '#64B5F6',    # Light blue for X
        'o_color': '#FF7043'     # Light red for O
    }