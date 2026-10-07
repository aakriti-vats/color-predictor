import streamlit as st
import numpy as np
import io
from color_extractor import load_image, extract_colors
from color_utils import rgb_to_hex, rgb_to_cmyk, get_harmonies
from palette_generator import create_palette_image

st.set_page_config(
    page_title="AI Color Predictor",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 AI Color Predictor for Artists")
st.markdown("Upload any artwork or photo to extract its dominant color palette.")

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    n_colors = st.slider("Number of colors to extract", 3, 10, 5)
    show_harmonies = st.checkbox("Show color harmonies", value=True)
    show_cmyk = st.checkbox("Show CMYK values", value=True)

# ── Upload ────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload an image", type=["jpg", "jpeg", "png", "webp"]
)

if uploaded is not None:

    # ── Two column layout ─────────────────────────────
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Original image")
        st.image(uploaded, use_column_width=True)

    # ── Run AI ────────────────────────────────────────
    with st.spinner("Analyzing colors with AI..."):
        image = load_image(uploaded)
        colors, percentages = extract_colors(image, n_colors)

    with col2:
        st.subheader("Color palette")
        palette_img = create_palette_image(colors, percentages)
        st.image(palette_img, use_column_width=True)

        # Download button
        buf = io.BytesIO()
        palette_img.save(buf, format="PNG")
        st.download_button(
            label="Download palette as PNG",
            data=buf.getvalue(),
            file_name="my_palette.png",
            mime="image/png"
        )

    # ── Color detail cards ────────────────────────────
    st.subheader("Color details")
    cols = st.columns(len(colors))

    for i, (color, pct) in enumerate(zip(colors, percentages)):
        r, g, b = int(color[0]), int(color[1]), int(color[2])
        hex_val = rgb_to_hex(r, g, b)

        with cols[i]:
            st.markdown(
                f'<div style="background:{hex_val}; height:60px; '
                f'border-radius:8px; margin-bottom:8px;"></div>',
                unsafe_allow_html=True
            )
            st.caption(f"**{hex_val}**")
            st.caption(f"RGB: ({r}, {g}, {b})")
            st.caption(f"Area: {pct}%")

            if show_cmyk:
                c, m, y, k = rgb_to_cmyk(r, g, b)
                st.caption(f"CMYK: {c}, {m}, {y}, {k}")

    # ── Color harmonies ───────────────────────────────
    if show_harmonies:
        st.subheader("Color harmonies")
        st.markdown("Based on the most dominant color in your image.")

        primary = (int(colors[0][0]), int(colors[0][1]), int(colors[0][2]))
        harmonies = get_harmonies(*primary)

        h_col1, h_col2, h_col3 = st.columns(3)

        with h_col1:
            st.markdown("**Complementary**")
            for c in harmonies['complementary']:
                hex_c = rgb_to_hex(*c)
                st.markdown(
                    f'<div style="background:{hex_c}; height:40px; '
                    f'border-radius:6px; margin-bottom:4px;"></div>'
                    f'<p style="font-size:12px;">{hex_c}</p>',
                    unsafe_allow_html=True
                )

        with h_col2:
            st.markdown("**Analogous**")
            for c in harmonies['triadic']:
                hex_c = rgb_to_hex(*c)
                st.markdown(
                    f'<div style="background:{hex_c}; height:40px; '
                    f'border-radius:6px; margin-bottom:4px;"></div>'
                    f'<p style="font-size:12px;">{hex_c}</p>',
                    unsafe_allow_html=True
                )

else:
    st.info("Upload an image above to get started.")