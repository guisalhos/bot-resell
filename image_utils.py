import os
from io import BytesIO
from rembg import remove
from PIL import Image, ImageFilter

CANVAS_SIZE = (1400, 1400)
MAX_PIECE_SIZE = (1080, 1080)

BACKGROUND_MAP = {
    "industrial_1": "static/backgrounds/industrial_1.png",
    "industrial_2": "static/backgrounds/industrial_2.png",
    "industrial_3": "static/backgrounds/industrial_3.png",
}

def add_shadow(piece, blur=18, opacity=85, offset=(18, 22)):
    alpha = piece.getchannel("A")

    shadow = Image.new("RGBA", piece.size, (0, 0, 0, 0))
    shadow.putalpha(alpha)

    shadow_pixels = []
    for px in shadow.getdata():
        shadow_pixels.append((0, 0, 0, opacity if px[3] > 0 else 0))
    shadow.putdata(shadow_pixels)

    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow, offset

def process_image(input_bytes, background_key):
    bg_path = BACKGROUND_MAP.get(background_key)

    if not bg_path or not os.path.exists(bg_path):
        raise ValueError("Fundo inválido.")

    # remove fundo
    removed = remove(input_bytes)

    piece = Image.open(BytesIO(removed)).convert("RGBA")
    background = Image.open(bg_path).convert("RGBA").resize(CANVAS_SIZE)

    # resize proporcional sem deformar
    piece.thumbnail(MAX_PIECE_SIZE, Image.LANCZOS)

    # centrar
    x = (background.width - piece.width) // 2
    y = (background.height - piece.height) // 2

    # sombra
    shadow, (sx, sy) = add_shadow(piece)

    final = background.copy()
    final.alpha_composite(shadow, (x + sx, y + sy))
    final.alpha_composite(piece, (x, y))

    output = BytesIO()
    final.save(output, format="PNG")
    return output.getvalue()