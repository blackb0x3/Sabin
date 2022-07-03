import mediatr


class GenerateMosaicCommand(mediatr.GenericQuery):
    def __init__(self, original: str, tileset: str, tilesize: int, colour_match_approach: str, output_file_path: str):
        self.original = original
        self.tileset = tileset
        self.tilesize = tilesize
        self.colour_match_approach = colour_match_approach
        self.output_file_path = output_file_path

    def __str__(self):
        return f"original: {self.original} | tileset: {self.tileset} | tilesize: {self.tilesize}"
