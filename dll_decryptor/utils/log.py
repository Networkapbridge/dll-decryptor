from __future__ import annotations

import logging
import sys


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)