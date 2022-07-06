from __future__ import print_function
from domain import helpers
from domain.models import Tile
from domain.primaryports import GenerateMosaicCommand
from domain.representations import SuccessResponse, BadRequestResponse, ErrorResponse
from mediatr import Mediator
from pathlib import Path
from PIL import Image
from typing import Union
import glob
import logging
import numpy as np
import os
import scipy
import scipy.misc
import scipy.cluster

# SUPPORTED_IMAGE_FILE_EXTENSIONS = ['jpg', 'png', 'gif', 'webp', 'tiff', 'psd', 'raw', 'bmp']
SUPPORTED_IMAGE_FILE_EXTENSIONS = ['jpg', 'png']


@Mediator.handler
class GenerateMosaicCommandHandler:
    async def handle(self, request: GenerateMosaicCommand) -> Union[SuccessResponse, BadRequestResponse, ErrorResponse]:
        try:
            await self.handle_impl(request)
        except ValueError as e:
            return BadRequestResponse(str(e))
        except Exception as e:
            return ErrorResponse(str(e))

    async def handle_impl(self, request: GenerateMosaicCommand) -> Union[
        SuccessResponse, BadRequestResponse, ErrorResponse]:
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
        # regex match against image files in the tileset
        file_list = []
        for supported_extension in SUPPORTED_IMAGE_FILE_EXTENSIONS:
            file_list.extend(glob.glob(f'*.{supported_extension}', root_dir=request.tileset, recursive=True))
        for tile_file in file_list:
            tile_img = Image.open(os.path.join(request.tileset, tile_file))
            original_dims = tile_img.size[:]
            tile_img = tile_img.resize((request.tilesize, request.tilesize))
            dominant_colour = self.get_dominant_colour(tile_img, tile_file)
            tiles.append(Tile(name=tile_file, img=tile_img, original_dims=original_dims, scaled_dims=tile_img.size,
                              dominant_colour=dominant_colour))

        mosaic = self.build_mosaic(original_img, tiles, request.tilesize, request.colour_match_approach)

        if not os.path.exists(request.output_file_path):
            Path(request.output_file_path).touch(exist_ok=True)

        mosaic.save(request.output_file_path)

        return SuccessResponse()

    def build_mosaic(self, original_img: Image.Image, tiles: list[Tile], tilesize: int,
                     colour_match_approach: str) -> Image.Image:
        new_width = helpers.round_to_multiple(original_img.width, tilesize)
        new_height = helpers.round_to_multiple(original_img.height, tilesize)
        original_img.resize((new_width, new_height))
        mosaic_img = Image.new(mode='RGB', size=(new_width, new_height))

        logging.debug({'msg': 'Attempting to generate photomosaic'})
        for j in range(0, new_height, tilesize):
            for i in range(0, new_width, tilesize):
                original_img_section = original_img.crop((i, j, i + tilesize, j + tilesize))
                dominant_colour_for_section = self.get_dominant_colour(original_img_section,
                                                                       f'original image section at ({i}, {j})')
                # cosine similarity between 2 vectors
                best_match = sorted(tiles, key=lambda x: helpers.cosine_similarity(dominant_colour_for_section, x.dominant_colour), reverse=True)[0]
                mosaic_img.paste(best_match.img, (i, j))

        logging.debug({'msg': 'Photomosaic generated'})

        return mosaic_img

    def get_dominant_colour(self, img: Image.Image, img_name: str):
        try:
            logging.debug({'msg': 'attempting to find dominant colour', 'img_name': img_name})
            NUM_CLUSTERS = 5
            logging.debug({'msg': 'reading image'})
            ar = np.asarray(img)
            shape = ar.shape
            ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
            logging.debug({'msg': 'finding clusters'})
            codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
            logging.debug({'msg': 'found clusters'})
            # logging.debug({'msg': ''})
            # assign codes
            vecs, dist = scipy.cluster.vq.vq(ar, codes)
            # count occurrences
            counts, bins = scipy.histogram(vecs, len(codes))
            # find most frequent
            index_max = scipy.argmax(counts)
            colour = codes[index_max]
            logging.debug({'msg': 'found dominant colour', 'colour': colour, 'img_name': img_name})
            return colour[:3]

        except Exception as e:
            logging.error({'msg': 'error whilst getting dominant colour', 'img_name': img_name, 'error': str(e)})
            return None
