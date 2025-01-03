import os
import functools
import pathlib
import re

from sphinx.util import logging

from docs_gurobi_com.versions import VersionHandler
from docs_gurobi_com.latex import configure_latex

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


def html_page_context_readthedocs(app, pagename, templatename, context, doctree):
    """
    Configures jinja variables based on readthedocs environment variables.

    A build on readthedocs will have the following jinja variables available:

        grb_readthedocs = True
        grb_show_banner = True/False
        grb_rtd_version = readthedocs version slug
        grb_current_version = <version number of current release>
        grb_version_status = one of: current, beta, dev, old
        grb_current_url = /url/to/current/build
        grb_this_url = /url/to/this/build

        pagename = # current page (defined by sphinx)
        theme_version_warning = "true" # can be set to 'false' in html_theme_options
        theme_feedback_banner = "true" # can be set to 'false' in html_theme_options
        theme_construction_warning = "true" # can be set to 'false' in html_theme_options

    With these jinja variables, the current page should be at:

        {{ grb_this_url }}{{ pagename }}.html

    While the URL of the same page on the 'current' branch (i.e. for redirect
    links) should be:

        {{ grb_current_url }}{{ pagename }}.html

    A basic testing setup for the current branch is:

        export READTHEDOCS="True"
        export READTHEDOCS_VERSION_TYPE="branch"
        export READTHEDOCS_VERSION="current"
        export READTHEDOCS_CANONICAL_URL="./current/"

    To display the "old version" warning set:

        export READTHEDOCS_VERSION="10.0"
        export READTHEDOCS_CANONICAL_URL="./10.0/"

    To display the "in development" warning set:

        export READTHEDOCS_VERSION="latest"
        export READTHEDOCS_CANONICAL_URL="./latest/"
    """

    version_handler = VersionHandler()
    grb_context = version_handler.create_context(os.environ)
    context.update(grb_context)

    # If custom banner HTML source was provided via html_context in conf.py, do
    # not display the default version-based warning banners.
    if context.get("grb_custom_banner", ""):
        context["grb_show_banner"] = False

    # Note: RTD adviseds to set this manually:
    #
    #   context["READTHEDOCS"] = True
    #
    # but for now we should not. It enables furo's readthedocs customisation
    # which has not kept up with the evolution of RTD addons.


def builder_inited(app):
    """Update configuration with some common properties used across
    docs.gurobi.com. Note that this overrides settings from individual project's
    conf.py files."""
    app.config.copyright = "2025, Gurobi Optimization, LLC"
    app.config.author = "Gurobi Optimization, LLC"

    # Local copy in static directory, from gurobi.com/favicon.ico
    app.config.html_favicon = "favicon.ico"

    # Uses sphinx defaults for 'last updated' footer, see
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_last_updated_fmt
    app.config.html_last_updated_fmt = ""

    # Disable sphinx default behaviour which adds a link to all images to their
    # original-size file. This doesn't suit our use of figures.
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_scaled_image_link
    app.config.html_scaled_image_link = False

    # Don't copy sources into the build
    app.config.html_copy_source = False

    # We use sphinx-tabs for language switching in examples, collapsing is not what we want
    # https://sphinx-tabs.readthedocs.io/en/latest/#sphinx-configuration
    app.config.sphinx_tabs_disable_tab_closing = True


def builder_inited_readthedocs(app):

    # Set canonical URL from the Read the Docs Domain
    app.config.html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

    # Configure sphinx-sitemap to use the canonical URL and excluding
    # non-content files
    rtd_version = os.environ.get("READTHEDOCS_VERSION", "unknown")
    app.config.sitemap_filename = f"sitemap-{rtd_version}.xml"
    app.config.sitemap_url_scheme = "{link}"
    app.config.sitemap_excludes = [
        "modindex.html",
        "genindex.html",
        "404.html",
        "search.html",
        "index_pdf.html",
    ]


def config_inited(app, config, git_commit_hash):
    # Note: running this at builder_inited seems to be too late.
    # TODO: fold the builder_inited commands in here (requires that all users
    # add docs_gurobi_com as an *extension*, not just a theme).
    configure_latex(config, git_commit_hash)
    app.add_js_file("scrolltree.js")


def setup(app):

    readthedocs = os.environ.get("READTHEDOCS", "") == "True"
    if readthedocs:
        logger.info("docs.gurobi.com theme: running in readthedocs mode")

    app.add_html_theme("docs_gurobi_com", here / "theme")

    git_commit_hash = None
    if readthedocs:
        git_commit_hash = os.environ.get("READTHEDOCS_GIT_COMMIT_HASH")

    app.connect(
        "config-inited",
        functools.partial(config_inited, git_commit_hash=git_commit_hash),
    )
    app.connect("builder-inited", builder_inited)

    # Additional configuration on readthedocs
    if readthedocs:

        app.connect("builder-inited", builder_inited_readthedocs)
        app.connect("html-page-context", html_page_context_readthedocs)

        # The sphinx-sitemap extension requires html_baseurl to be set. This is
        # only done if running on readthedocs, so only enable it there.
        app.setup_extension("sphinx_sitemap")
