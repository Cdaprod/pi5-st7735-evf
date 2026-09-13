"""Scene canvas and compositing helpers."""
from PIL import Image
from ..theme import BACKGROUND


def scene_canvas(width: int, height: int) -> Image.Image:
    return Image.new("RGBA", (width, height), BACKGROUND + (255,))


def finish(image: Image.Image) -> Image.Image:
    return image.convert("RGB")
