# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


class AprError(RuntimeError):
    """Base class for all errors raised by apr and charms."""


class AprServiceError(AprError):
    """Base class for errors where the apr service is involved."""
