from __future__ import annotations
from datetime import datetime
from logging import config as logging_config
import argparse
import linecache
import logging
import os

if __name__ == '__main__':
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
    parsed_args = parser.parse_args()
