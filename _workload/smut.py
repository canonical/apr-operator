import json
import logging
import os
import random
from pathlib import Path
from typing import Dict

from fastapi import FastAPI
from uvicorn import run

SMUT_CONFIG = Path(os.getenv('SMUT_CONFIG'))
SMUT_LOGS = Path(os.getenv('SMUT_LOGS'))

logger = logging.getLogger(__file__)
logger.addHandler(logging.FileHandler(SMUT_LOGS))
logger.setLevel('INFO')


def serve(cfg: Dict):
    app = FastAPI()

    @app.get("/")
    async def root():
        sides = cfg['sides']
        roll = random.randint(0, sides)
        logger.debug(f'rolled {roll}')
        return {"roll": str(roll)}

    logger.info('Ready...')
    run(app, host="0.0.0.0")


def smut():
    cfg = SMUT_CONFIG
    if not cfg.exists():
        raise RuntimeError('config not found, cannot smut.')
    parsed_cfg = json.loads(cfg.read_text())
    logger.debug(f'found cfg at {cfg}')
    serve(parsed_cfg)


if __name__ == '__main__':
    smut()
