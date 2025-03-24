def rgb_to_stellaris_hsv_format(r, g, b):
    # Normalize RGB values to 0-1 range
    r, g, b = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # Format output in Stellaris style
    return f"{{ flag = hsv {{ {round(h, 2)} {round(s, 2)} {round(v, 2)} }}\tmap = hsv {{ {round(h, 2)} {round(s, 2)} {round(v, 2)} }} }}"

# Example RGB color
rgb_color = (96, 52, 56)
stellaris_hsv_output = rgb_to_stellaris_hsv_format(*rgb_color)
stellaris_hsv_output
