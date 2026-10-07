import colorsys


def rgb_to_hex(r, g, b):
    """Convert RGB values to a HEX color string."""
    return '#{:02X}{:02X}{:02X}'.format(int(r), int(g), int(b))


def rgb_to_cmyk(r, g, b):
    """Convert RGB values to CMYK (used in print design)."""
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k == 1:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c*100), round(m*100), round(y*100), round(k*100)


def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV. Used internally for harmony calculations."""
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def get_complementary(r, g, b):
    """Return the complementary color (opposite on the color wheel)."""
    h, s, v = rgb_to_hsv(r, g, b)
    h_new = (h + 0.5) % 1.0
    r2, g2, b2 = colorsys.hsv_to_rgb(h_new, s, v)
    return int(r2*255), int(g2*255), int(b2*255)


def get_analogous(r, g, b):
    """Return two analogous colors (±30° on the color wheel)."""
    h, s, v = rgb_to_hsv(r, g, b)
    h1 = (h + 30/360) % 1.0
    h2 = (h - 30/360) % 1.0
    r1, g1, b1 = colorsys.hsv_to_rgb(h1, s, v)
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
    return (int(r1*255), int(g1*255), int(b1*255)), \
           (int(r2*255), int(g2*255), int(b2*255))


def get_triadic(r, g, b):
    """Return two triadic colors (±120° on the color wheel)."""
    h, s, v = rgb_to_hsv(r, g, b)
    h1 = (h + 120/360) % 1.0
    h2 = (h + 240/360) % 1.0
    r1, g1, b1 = colorsys.hsv_to_rgb(h1, s, v)
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
    return (int(r1*255), int(g1*255), int(b1*255)), \
           (int(r2*255), int(g2*255), int(b2*255))


def get_harmonies(r, g, b):
    """Return all three harmony types for a given color."""
    return {
        'complementary': [get_complementary(r, g, b)],
        'analogous':     list(get_analogous(r, g, b)),
        'triadic':       list(get_triadic(r, g, b))
    }