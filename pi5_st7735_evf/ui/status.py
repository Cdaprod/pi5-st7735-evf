from PIL import Image, ImageDraw, ImageFont


def no_signal_screen(width: int, height: int, detail: str = "HDMI disconnected",
                     last_mode: str = "") -> Image.Image:
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    title = "NO SIGNAL"
    box = draw.textbbox((0, 0), title, font=font)
    draw.text(((width - (box[2] - box[0])) // 2, max(4, height // 2 - 12)), title,
              fill="white", font=font)
    draw.text((4, height // 2 + 4), detail[:max(1, width // 6)], fill=(160, 160, 160), font=font)
    if last_mode:
        draw.text((4, height - 12), last_mode, fill=(120, 120, 120), font=font)
    return image
