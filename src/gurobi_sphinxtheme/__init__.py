__version__ = "0.1.0"

from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx

_THEME_PATH = (Path(__file__).parent / "theme" / "gurobi").resolve()


def setup(app: Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    app.require_sphinx("4.0")

    app.add_html_theme("gurobi", str(_THEME_PATH))

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
