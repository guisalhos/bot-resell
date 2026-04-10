from io import BytesIO
from rembg import remove
from PIL import Image, ImageFilter
import os

CANVAS_SIZE = (1000, 1000)
MAX_PIECE_SIZE = (820, 820)

BACKGROUND_MAP = {
    "industrial_1": "static/backgrounds/industrial_1.png",
    "industrial_2": "static/backgrounds/industrial_2.png",
    "industrial_3": "static/backgrounds/industrial_3.png",
}

def add_shadow(piece, blur=14, opacity=75, offset=(14, 18)):
    alpha = piece.getchannel("A")
    shadow = Image.new("RGBA", piece.size, (0, 0, 0, 0))
    shadow.putalpha(alpha)

    shadow_pixels = []
    for px in shadow.getdata():
        shadow_pixels.append((0, 0, 0, opacity if px[3] > 0 else 0))
    shadow.putdata(shadow_pixels)

    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow, offset

def compress_before_remove(input_bytes, max_size=(1200, 1200)):
    img = Image.open(BytesIO(input_bytes)).convert("RGB")
    img.thumbnail(max_size, Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=88, optimize=True)
    return buf.getvalue()

def process_image(input_bytes, background_key):
    bg_path = BACKGROUND_MAP.get(background_key)

    if not bg_path:
        raise ValueError(f"Fundo inválido: {background_key}")

    if not os.path.exists(bg_path):
        raise ValueError(f"Ficheiro não encontrado: {bg_path}")

    # reduzir antes de usar rembg
    lighter_input = compress_before_remove(input_bytes)

    removed = remove(lighter_input)

    piece = Image.open(BytesIO(removed)).convert("RGBA")
    background = Image.open(bg_path).convert("RGBA").resize(CANVAS_SIZE)

    piece.thumbnail(MAX_PIECE_SIZE, Image.LANCZOS)

    x = (background.width - piece.width) // 2
    y = (background.height - piece.height) // 2

    shadow, (sx, sy) = add_shadow(piece)

    final = background.copy()
    final.alpha_composite(shadow, (x + sx, y + sy))
    final.alpha_composite(piece, (x, y))

    output = BytesIO()
    final.save(output, format="PNG", optimize=True)
    return output.getvalue()