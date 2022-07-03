from domain import helpers
from domain.models import Tile
from domain.primaryports import GenerateMosaicCommand
from domain.representations import SuccessResponse, BadRequestResponse, ErrorResponse
from mediatr import Mediator
from typing import Union
from PIL import Image
import glob
import logging
import os


@Mediator.handler
class GenerateMosaicCommandHandler:
    async def handle(self, request: GenerateMosaicCommand) -> Union[SuccessResponse, BadRequestResponse, ErrorResponse]:
        try:
            await self.handle_impl(request)
        except ValueError as e:
            return BadRequestResponse(str(e.with_traceback()))
        except Exception as e:
            return ErrorResponse(str(e.with_traceback()))

    async def handle_impl(self, request: GenerateMosaicCommand) -> Union[SuccessResponse, BadRequestResponse, ErrorResponse]:
        if not os.path.exists(request.original):
            raise ValueError(f'image file path {request.original} does NOT exist!')
        if not os.path.exists(request.tileset):
            raise ValueError(f'image tileset path {request.tileset} does NOT exist!')
        if request.tilesize < 0:
            raise ValueError(f'tile size must be a positive integer!')
        if request.tilesize < 16:
            logging.warning({'msg': 'small tile size detected, use with caution', 'tilesize': request.tilesize})

        original_img = Image.open(request.original)
        tiles: list[Tile] = list()
        for tile_file in glob.glob(request.tileset):
            tile_img = Image.open(tile_file)
            original_dims = tile_img.size[:]
            tile_img.resize((request.tilesize, request.tilesize))
            tiles.append(Tile(name=tile_file, img=tile_img, original_dims=original_dims, scaled_dims=tile_img.size))

        mosaic = self.build_mosaic(original_img, tiles, request.tilesize, request.colour_match_approach)
        mosaic.save(request.output_file_path)

        return SuccessResponse()

    def build_mosaic(self, original_img: Image.Image, tiles: list[Tile], tilesize: int, colour_match_approach: str) -> Image.Image:
        new_width = helpers.round_to_multiple(original_img.width, tilesize)
        new_height = helpers.round_to_multiple(original_img.height, tilesize)
        original_img.resize((new_width, new_height))
        mosaic_img = Image.new(mode='RGBA', size=(new_width, new_height))
        pass
