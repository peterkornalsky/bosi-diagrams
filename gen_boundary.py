from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1568, 902
BG = (255, 255, 255)
SECTION_BG = (255, 255, 240)
BOX_BG = (232, 224, 240)
BOX_BORDER = (147, 112, 219)
SECTION_BORDER = (180, 180, 180)
TEXT_COLOR = (51, 51, 51)
TITLE_COLOR = (51, 51, 51)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("arial.ttf", 20)
    font_box = ImageFont.truetype("arial.ttf", 16)
except:
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
        font_box = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_box = ImageFont.load_default()

def draw_section(x, y, w, h, title):
    draw.rectangle([x, y, x + w, y + h], fill=SECTION_BG, outline=SECTION_BORDER, width=2)
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw) / 2, y + 10), title, fill=TITLE_COLOR, font=font_title)

def draw_box(x, y, w, h, lines):
    draw.rectangle([x, y, x + w, y + h], fill=BOX_BG, outline=BOX_BORDER, width=2)
    total_h = len(lines) * 22
    start_y = y + (h - total_h) / 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_box)
        tw = bbox[2] - bbox[0]
        draw.text((x + (w - tw) / 2, start_y + i * 22), line, fill=TEXT_COLOR, font=font_box)

MARGIN = 40
GAP = 60
sec_w = (W - 2 * MARGIN - GAP) // 2
sec_h = H - 2 * MARGIN

# BOSI section (left)
bosi_x = MARGIN
bosi_y = MARGIN
draw_section(bosi_x, bosi_y, sec_w, sec_h, "BOSI Scope (All New)")

bosi_items = [
    ["SQS Consumer"],
    ["4 Orchestrators"],
    ["2 API Clients"],
    ["Webhook Endpoint"],
    ["OTel + HealthChecks + Polly"],
]

box_w = 280
box_h = 60
bosi_box_x = bosi_x + (sec_w - box_w) / 2
spacing = (sec_h - 50 - len(bosi_items) * box_h) / (len(bosi_items) + 1)

for i, lines in enumerate(bosi_items):
    by = bosi_y + 50 + spacing * (i + 1) + box_h * i
    draw_box(bosi_box_x, by, box_w, box_h, lines)

# BO section (right)
bo_x = MARGIN + sec_w + GAP
bo_y = MARGIN
draw_section(bo_x, bo_y, sec_w, sec_h, "BO Scope (Extend Only)")

bo_items = [
    ["DB: +SiAccountId", "+SiPremiumAmount", "+SiAccountStatus"],
    ["API: +GET related-products", "2 new endpoints"],
    ["UI: Related Products", "config changes"],
    ["Premium Calculation", "adjustments"],
    ["Events: +enrich with", "relatedProductId"],
    ["DD Batch: +include", "SiPremiumAmount"],
]

bo_box_h = 70
spacing_bo = (sec_h - 50 - len(bo_items) * bo_box_h) / (len(bo_items) + 1)

for i, lines in enumerate(bo_items):
    by = bo_y + 50 + spacing_bo * (i + 1) + bo_box_h * i
    draw_box(bo_x + (sec_w - box_w) / 2, by, box_w, bo_box_h, lines)

out = os.path.join(os.path.dirname(__file__), "boundary.png")
img.save(out, "PNG")
print(f"Saved to {out}")
