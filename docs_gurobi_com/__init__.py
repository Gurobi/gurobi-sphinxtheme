import pathlib

from sphinx.util import logging

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


def update_config(config):
    # Update configuration with some common properties used across
    # docs.gurobi.com. Note that this overrides settings from individual
    # project's conf.py files.
    config.copyright = "2024, Gurobi Optimization, LLC"
    config.author = "Gurobi Optimization, LLC"
    config.html_favicon = "https://www.gurobi.com/favicon.ico"


def builder_inited(app):
    update_config(app.config)


def setup(app):
    app.add_html_theme("docs_gurobi_com", here / "theme")
    app.connect("builder-inited", builder_inited)
