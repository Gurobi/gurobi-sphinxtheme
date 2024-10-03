import os
import pathlib

from sphinx.util import logging

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent

READTHEDOCS_BUILD = os.environ.get("READTHEDOCS", "") == "True"


def configure_sitemap(config):
    # Add configuration needed for the sphinx-sitemap extension on readthedocs
    if not READTHEDOCS_BUILD:
        return

    # Set canonical URL from the Read the Docs Domain
    config.html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

    # Build a sitemap using the canonical URL, excluding non-content files
    rtd_version = os.environ.get("READTHEDOCS_VERSION", "unknown")
    config.sitemap_filename = f"sitemap-{rtd_version}.xml"
    config.sitemap_url_scheme = "{link}"
    config.sitemap_excludes = [
        "index.html",
        "genindex.html",
        "404.html",
        "search.html",
    ]


def update_config(config):
    # Update configuration with some common properties used across
    # docs.gurobi.com. Note that this overrides settings from individual
    # project's conf.py files.
    config.copyright = "2024, Gurobi Optimization, LLC"
    config.author = "Gurobi Optimization, LLC"
    config.html_favicon = "https://www.gurobi.com/favicon.ico"


def builder_inited(app):
    update_config(app.config)
    configure_sitemap(app.config)


def setup(app):
    app.add_html_theme("docs_gurobi_com", here / "theme")
    app.connect("builder-inited", builder_inited)

    # The sphinx-sitemap extension requires html_baseurl to be set. This is only
    # done if running on readthedocs.
    if READTHEDOCS_BUILD:
        app.setup_extension("sphinx_sitemap")
