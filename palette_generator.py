import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from color_utils import rgb_to_hex
import io


def create_palette_image(colors, percentages):
    """Draw a visual palette with color swatches, HEX codes and percentages."""
    n = len(colors)
    fig, ax = plt.subplots(1, 1, figsize=(10, 3))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis('off')

    for i, (color, pct) in enumerate(zip(colors, percentages)):
        r, g, b = int(color[0]), int(color[1]), int(color[2])
        hex_val = rgb_to_hex(r, g, b)

        # Draw color rectangle
        rect = patches.Rectangle(
            (i, 0.25), 1, 0.75,
            linewidth=0,
            facecolor=(r/255, g/255, b/255)
        )
        ax.add_patch(rect)

        # Pick white or black text depending on brightness
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = 'white' if brightness < 128 else 'black'

        # HEX label inside swatch
        ax.text(
            i + 0.5, 0.55, hex_val,
            ha='center', va='center',
            fontsize=9, color=text_color, fontweight='bold'
        )

        # Percentage below swatch
        ax.text(
            i + 0.5, 0.12, f'{pct}%',
            ha='center', va='center',
            fontsize=9, color='#444444'
        )

    plt.tight_layout(pad=0.5)

    # Save to memory buffer and return as PIL Image
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return Image.open(buf)