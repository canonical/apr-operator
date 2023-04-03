#!/usr/bin/env python3

# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""A  juju charm for Grafana Agent on Kubernetes."""
import logging

from apr_charm import AprCharm

logger = logging.getLogger(__name__)

APR_CONFIG = "/apr.cfg"
APR_LOGS = "/apr.log"


class AprK8sCharm(AprCharm):
    """Kubernetes version of the Apr charm."""

    def __init__(self, *args):
        super().__init__(*args)

    def install(self) -> None:
        """Install the apr software."""

    def start(self) -> None:
        """Start the apr software."""
