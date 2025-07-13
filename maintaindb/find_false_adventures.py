
import json
import os
import glob
import logging
import pathlib

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(os.sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_path = os.path.join(root, '_dc')

def find_false():
    false_files = []
    logger.info(f'Reading all files at: {input_path}')
    input_full_path = f"{str(input_path)}/*.json"
    for file in glob.glob(input_full_path):
        with open(file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to load JSON from {file}: {e}")
                continue

            if data.get('is_adventure') is False:
                false_files.append(file)

    if not false_files:
        logger.info("No JSON files have 'is_adventure' set to False.")
    else:
        logger.warning(f"{len(false_files)} JSON files have 'is_adventure' set to False:")
        for file_path in false_files:
            logger.warning(f"  - {file_path}")

if __name__ == '__main__':
    find_false()
