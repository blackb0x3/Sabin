from PIL import Image


class Tile:
    def __init__(self, name: str, img: Image.Image, original_dims: tuple[int, int], scaled_dims: tuple[int, int], dominant_colour: tuple[float, float, float]):
        self.name = name
        self.img = img
        self.original_dims = original_dims
        self.scaled_dims = scaled_dims
        self.dominant_colour = dominant_colour
