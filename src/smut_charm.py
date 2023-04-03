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

from src.apr import Apr

logger = logging.getLogger(__name__)


class AprCharm(CharmBase):
    """Apr charm shared logic."""

    def __new__(cls, *args: Any, **kwargs: Dict[Any, Any]):
        """Forbid the usage of Apr directly."""
        if cls is AprCharm:
            raise TypeError("This is a base class and cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self._apr = None

    @property
    def apr(self):
        if not self._apr:
            self._apr = Apr(
                sides=int(self.config.get('sides')),
                is_up=self._is_apr_up(),
            )
        return self._apr

    @contextmanager
    def safe_yield(self, maintenance_message: str, catch: Tuple[Type[Exception]] = (Exception,)) -> bool:
        self.unit.status = MaintenanceStatus(maintenance_message)
        try:
            yield
        except catch as e:
            self.unit.status = ErrorStatus(str(e))
        self.unit.status = ActiveStatus()

    def _on_install(self, _event) -> None:
        """Install the apr software."""
        with self.safe_yield("Installing apr software"):
            self.install()

    def _on_start(self, _event) -> None:
        """Start the apr software."""
        with self.safe_yield("Starting apr software"):
            self.start()

    def __notimpl__(self):
        raise NotImplementedError()

    _is_apr_up = __notimpl__
    start = __notimpl__
    install = __notimpl__
