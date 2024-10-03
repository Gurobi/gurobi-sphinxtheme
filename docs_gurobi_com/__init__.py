import pathlib

from sphinx.util import logging

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


def setup(app):
    app.add_html_theme("docs_gurobi_com", here / "theme")
