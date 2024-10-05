import os
import functools
import pathlib
import re

from sphinx.util import logging

from docs_gurobi_com.latex import configure_latex

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


def html_page_context_readthedocs(app, pagename, templatename, context, doctree):
    """
    Configures jinja variables based on readthedocs environment variables. If
    they are not set, no version warning banner is shown.

    A build on readthedocs will have the following jinja variables available:

      gurobi_rtd = "true"
      gurobi_rtd_version = # version tag: 10.0, 11.0, current, latest
      gurobi_rtd_version_type = # "branch" for deployments, "external" for PRs
      gurobi_rtd_canonical_url = # the root url of the deployment
      gurobi_rtd_current_url = # root url of the current deployment
      gurobi_gh_issue_url = # url to open a github issue for this repo

      pagename = # current page (defined by sphinx)
      theme_version_warning = "true" # can be set to 'false' in html_theme_options
      theme_feedback_banner = "true" # can be set to 'false' in html_theme_options
      theme_construction_warning = "true" # can be set to 'false' in html_theme_options

    With these jinja variables, the URL of the current page in an RTD deployment
    should be:

      {{ gurobi_rtd_canonical_url }}{{ pagename }}.html

    and the same page on the current branch (i.e. for redirect links) should be:

      {{ gurobi_rtd_current_url }}{{ pagename }}.html

    A basic testing setup for the current branch is:

      export READTHEDOCS="True"
      export READTHEDOCS_VERSION_TYPE="branch"
      export READTHEDOCS_GIT_CLONE_URL="git@github.com:Gurobi/repo.git"
      export READTHEDOCS_VERSION="current"
      export READTHEDOCS_CANONICAL_URL="./current/"

    To display the "old version" warning set:

      export READTHEDOCS_VERSION="10.0"
      export READTHEDOCS_CANONICAL_URL="./10.0/"

    To display the "in development" warning set:

      export READTHEDOCS_VERSION="latest"
      export READTHEDOCS_CANONICAL_URL="./latest/"
    """

    # Note: RTD advised to set this manually, but for now we should not. It
    # enables furo's readthedocs customisation which has not kept up with the
    # addons.
    # Tell Jinja2 templates the build is running on Read the Docs
    # context["READTHEDOCS"] = True

    # Version and url information. Store these in distinct jinja variables
    # to prevent clashes with themes we inherit from.
    context["gurobi_rtd"] = "true"
    context["gurobi_rtd_version"] = os.environ.get("READTHEDOCS_VERSION")
    context["gurobi_rtd_version_type"] = os.environ.get("READTHEDOCS_VERSION_TYPE")
    context["gurobi_rtd_canonical_url"] = os.environ.get("READTHEDOCS_CANONICAL_URL")

    # For branch (i.e. not pull request) builds, get the canonical URL of
    # the current version.
    if context["gurobi_rtd_version_type"] == "branch":
        stem, mid, _ = context["gurobi_rtd_canonical_url"].rpartition(
            context["gurobi_rtd_version"]
        )
        if mid and stem.endswith("/"):
            context["gurobi_rtd_current_url"] = stem + "current/"
        else:
            # Might not be versioned. Don't render the banner.
            logger.warning(
                "Unexpected value: url={} version={}".format(
                    context["gurobi_rtd_canonical_url"],
                    context["gurobi_rtd_version"],
                )
            )
            logger.warning("gurobi_rtd_version reset to 'current'")
            context["gurobi_rtd_current_url"] = context["gurobi_rtd_canonical_url"]
            context["gurobi_rtd_version"] = "current"

    # URL for the issues page of the source repo.
    git_clone_url = os.environ.get("READTHEDOCS_GIT_CLONE_URL")
    match = re.match(r"git@github\.com:Gurobi/([\w-]+)\.git", git_clone_url)
    if not match:
        raise ValueError(f"Unexpected value: GIT_CLONE_URL={git_clone_url}")
    repo_name = match.group(1)
    context["gurobi_gh_issue_url"] = (
        f"https://github.com/Gurobi/{repo_name}/issues/new?labels=bug&template=bug_report.md"
    )


def builder_inited(app):
    """Update configuration with some common properties used across
    docs.gurobi.com. Note that this overrides settings from individual project's
    conf.py files."""
    app.config.copyright = "2024, Gurobi Optimization, LLC"
    app.config.author = "Gurobi Optimization, LLC"
    app.config.html_favicon = "https://www.gurobi.com/favicon.ico"


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
    ]


def config_inited(app, config, git_commit_hash):
    # Note: running this at builder_inited seems to be too late.
    # TODO: fold the builder_inited commands in here (requires that all users
    # add docs_gurobi_com as an *extension*, not just a theme).
    configure_latex(config, git_commit_hash)


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
