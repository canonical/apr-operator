import json
import logging
import os
import random
from pathlib import Path
from typing import Dict

from fastapi import FastAPI
from uvicorn import run

APR_CONFIG = Path(os.getenv('APR_CONFIG'))
APR_LOGS = Path(os.getenv('APR_LOGS'))

logger = logging.getLogger(__file__)
logger.addHandler(logging.FileHandler(APR_LOGS))
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


def apr():
    cfg = APR_CONFIG
    if not cfg.exists():
        raise RuntimeError('config not found, cannot apr.')
    parsed_cfg = json.loads(cfg.read_text())
    logger.debug(f'found cfg at {cfg}')
    serve(parsed_cfg)


if __name__ == '__main__':
    apr()
