# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Workload abstraction layer for smut operator."""

import logging
import pydantic

from src.state import SmutState, SmutStateBackend

logger = logging.getLogger(__name__)


class SmutConfig(pydantic.BaseModel):
    sides: int

    @pydantic.validator('sides')
    def _validate_sides(self, value):
        if not value in (2, 4, 6, 8, 10, 12, 20, 30, 40, 100):
            raise ValueError(f"How unplatonic: {value}.")  # Barbaric.


class Smut:
    """Smut software facade."""
    def __init__(self, sides: int, is_up: bool):
        self._sides = sides
        backend = SmutStateBackend()
        self._state = SmutState(is_up=is_up,
                                temperature_in_delft=backend.temperature_in_delft())

    def _generate_config(self):
        return {
            "sides": self._sides
        }

    @property
    def config(self) -> SmutConfig:
        """Smut configuration object."""
        return SmutConfig(**self._generate_config())
