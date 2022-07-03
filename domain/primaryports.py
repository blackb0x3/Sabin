import mediatr


class GenerateMosaicCommand(mediatr.GenericQuery):
    def __init__(self, original: str, tileset: str, tilesize: str):
        self.original = original
        self.tileset = tileset
        self.tilesize = tilesize

    def __str__(self):
        return f"original: {self.original} | tileset: {self.tileset} | tilesize: {self.tilesize}"
