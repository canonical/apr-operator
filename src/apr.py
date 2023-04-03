# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Workload abstraction layer for apr operator."""

import logging

import pydantic

from src.state import AprState, AprStateBackend

logger = logging.getLogger(__name__)


class AprConfig(pydantic.BaseModel):
    sides: int

    @pydantic.validator("sides")
    def _validate_sides(self, value):
        if not value in (2, 4, 6, 8, 10, 12, 20, 30, 40, 100):
            raise ValueError(f"How unplatonic: {value}.")  # Barbaric.


class Apr:
    """Apr software facade."""

    def __init__(self, sides: int, is_up: bool):
        self._sides = sides
        backend = AprStateBackend()
        self._state = AprState(is_up=is_up, temperature_in_delft=backend.temperature_in_delft())

    def _generate_config(self):
        return {"sides": self._sides}

    @property
    def config(self) -> AprConfig:
        """Apr configuration object."""
        return AprConfig(**self._generate_config())
