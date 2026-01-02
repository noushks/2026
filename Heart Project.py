# pip install pillow

from PIL import Image, ImageDraw, ImageFont

# --- 1) Build a simple pixel-heart mask (1 = filled, 0 = empty) ---
heart_mask = [
    "0011110000111100",
    "0111111001111110",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "0111111111111110",
    "0011111111111100",
    "0001111111111000",
    "0000111111110000",
    "0000011111100000",
    "0000001111000000",
    "0000000110000000",
]

px = 18  
pad = 6  

h_rows = len(heart_mask)
h_cols = len(heart_mask[0])
heart_w = h_cols * px
heart_h = h_rows * px

# text:
text_str = "i love you bonku"
text_gap = 18  
font_size = 46

font_candidates = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
font = None
for fp in font_candidates:
    try:
        font = ImageFont.truetype(fp, font_size)
        break
    except:
        pass
if font is None:
    font = ImageFont.load_default()


dummy = Image.new("RGBA", (10, 10), (255, 255, 255, 0))
d = ImageDraw.Draw(dummy)
bbox = d.textbbox((0, 0), text_str, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

# canvas size
W = max(heart_w + pad * 2, text_w + pad * 2)
H = heart_h + pad * 2 + text_gap + text_h + pad

img = Image.new("RGBA", (W, H), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# draws heart 
outline_color = (0, 0, 0, 255)
fill_color = (220, 30, 30, 255)
highlight_color = (255, 255, 255, 255)

# Helper to check mask
def filled(r, c):
    return heart_mask[r][c] == "1"

# Top-left position of heart
ox = (W - heart_w) // 2
oy = pad

# Draw outline:
for r in range(h_rows):
    for c in range(h_cols):
        if not filled(r, c):
            continue
        # 4-neighborhood check for edges
        neighbors = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
        is_edge = any(
            nr < 0 or nr >= h_rows or nc < 0 or nc >= h_cols or not filled(nr, nc)
            for nr, nc in neighbors
        )
        x0 = ox + c * px
        y0 = oy + r * px
        x1 = x0 + px
        y1 = y0 + px

        if is_edge:
            draw.rectangle([x0, y0, x1, y1], fill=outline_color)

# Draw fill slightly:
inset = max(2, px // 6)
for r in range(h_rows):
    for c in range(h_cols):
        if not filled(r, c):
            continue
        x0 = ox + c * px + inset
        y0 = oy + r * px + inset
        x1 = ox + (c + 1) * px - inset
        y1 = oy + (r + 1) * px - inset
        draw.rectangle([x0, y0, x1, y1], fill=fill_color)

# Add a small pixel highlight near top-left:
for r in range(1, 4):
    for c in range(2, 6):
        if filled(r, c):
            x0 = ox + c * px + inset
            y0 = oy + r * px + inset
            x1 = ox + (c + 1) * px - inset
            y1 = oy + (r + 1) * px - inset
            draw.rectangle([x0, y0, x1, y1], fill=highlight_color)

# text 
tx = (W - text_w) // 2
ty = oy + heart_h + text_gap
draw.text((tx, ty), text_str, font=font, fill=(0, 0, 0, 255), stroke_width=2, stroke_fill=(255, 255, 255, 255))

# for saving to files: 
img.save("pixel_heart_bonku.png")
print("Saved: pixel_heart_bonku.png")
