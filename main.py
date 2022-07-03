from __future__ import annotations
from datetime import datetime

from domain.handlers import GenerateMosaicCommandHandler
from domain.primaryports import GenerateMosaicCommand
from domain.representations import BadRequestResponse, ErrorResponse
from logging import config as logging_config
from mediatr import Mediator
import argparse
import asyncio
import linecache
import logging
import os


async def main():
    # logging setup
    logging_config.fileConfig(os.path.join(os.path.curdir, 'logging_config.ini'))
    logging.info({'msg': 'app logging configured'})
    timestamp = datetime.now()
    output_file_name = f"{timestamp.strftime('%H_%M_%S')}_out.jpeg"
    output_path = os.path.join(os.path.curdir, timestamp.strftime('%Y_%m_%d'), output_file_name)

    # 1-based index
    program_description = linecache.getline(os.path.join(os.path.curdir, 'README.md'), 2)

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('--original', required=True, type=str)
    parser.add_argument('--tileset', required=True, type=str)
    parser.add_argument('--tilesize', required=False, default=16)
    parser.add_argument('--colour-match-approach', required=False, default='dominant')
    parsed_args = parser.parse_args()

    generate_mosaic_command = GenerateMosaicCommand(
        parsed_args.original,
        parsed_args.tileset,
        parsed_args.tilesize,
        parsed_args.colour_match_approach,
        output_path)

    mediator = Mediator()
    mediator.register_handler(GenerateMosaicCommandHandler)
    result = await mediator.send_async(generate_mosaic_command)

    if isinstance(result, ErrorResponse) or isinstance(result, BadRequestResponse):
        logging.info({'msg': 'something went wrong', 'err': result.message})
    else:
        logging.info({'msg': f'Photomosaic generated at {output_path}'})

if __name__ == '__main__':
    asyncio.run(main())
