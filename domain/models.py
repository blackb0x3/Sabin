from PIL import Image


class Tile:
    name: str
    img: Image.Image
    original_dims: tuple[int, int]
    scaled_dims: tuple[int, int]
    average_colour: tuple[float, float, float]
    dominant_colours: list[tuple[float, float, float]]
