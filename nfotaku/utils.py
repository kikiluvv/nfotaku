def is_valid_hex_color(color: str) -> bool:
    return color.startswith("#") and len(color) == 7
