# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Common logic for both k8s and machine charms for Grafana Agent."""
import logging
from contextlib import contextmanager
from typing import Any, Dict, Tuple, Type

from ops.charm import CharmBase
from ops.framework import Framework
from ops.model import MaintenanceStatus, ErrorStatus, ActiveStatus
from requests.packages.urllib3.util import Retry  # type: ignore

from src.smut import Smut

logger = logging.getLogger(__name__)


class SmutCharm(CharmBase):
    """Smut charm shared logic."""

    def __new__(cls, *args: Any, **kwargs: Dict[Any, Any]):
        """Forbid the usage of Smut directly."""
        if cls is SmutCharm:
            raise TypeError("This is a base class and cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self._smut = None

    @property
    def smut(self):
        if not self._smut:
            self._smut = Smut(
                sides=int(self.config.get('sides')),
                is_up=self._is_smut_up(),
            )
        return self._smut

    @contextmanager
    def safe_yield(self, maintenance_message: str, catch: Tuple[Type[Exception]] = (Exception,)) -> bool:
        self.unit.status = MaintenanceStatus(maintenance_message)
        try:
            yield
        except catch as e:
            self.unit.status = ErrorStatus(str(e))
        self.unit.status = ActiveStatus()

    def _on_install(self, _event) -> None:
        """Install the smut software."""
        with self.safe_yield("Installing smut software"):
            self.install()

    def _on_start(self, _event) -> None:
        """Start the smut software."""
        with self.safe_yield("Starting smut software"):
            self.start()

    def __notimpl__(self):
        raise NotImplementedError()

    _is_smut_up = __notimpl__
    start = __notimpl__
    install = __notimpl__
