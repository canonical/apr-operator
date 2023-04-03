#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
import shlex
from logging import getLogger
from subprocess import PIPE, run
from typing import Literal

logger = getLogger(__file__)


def get_substrate() -> Literal["k8s", "machine"]:
    """Are we on kubernetes or on machine?"""
    proc = run(*shlex.split("cat /proc/1/sched | head -n 1"), text=True, stdout=PIPE)
    out = proc.stdout
    substrate: Literal["k8s", "machine"]
    if out.startswith("pebble"):
        substrate = "k8s"
    elif out.startswith("systemd"):
        substrate = "machine"
    else:
        logger.error(f"unknown substrate prefix: {out.split()[0]}; guessing machine.")
        substrate = "machine"

    logger.info(f"detected substrate: {substrate}")
    return substrate


if __name__ == "__main__":
    from ops.main import main

    _sub = get_substrate()
    if _sub == "machine":
        from machine_charm import AprMachineCharm

        logger.info("starting up machine charm")
        main(AprMachineCharm)
    elif _sub == "k8s":
        from k8s_charm import AprK8sCharm

        logger.info("starting up k8s charm")
        main(AprK8sCharm)
    raise TypeError(_sub)
