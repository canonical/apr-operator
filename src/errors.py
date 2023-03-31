# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

class SmutError(RuntimeError):
    """Base class for all errors raised by smut and charms."""


class SmutServiceError(SmutError):
    """Base class for errors where the smut service is involved."""
