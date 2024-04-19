import os
import pathlib
import re

here = pathlib.Path(__file__).parent


def setup_context(app, pagename, templatename, context, doctree):
    """
    Configures jinja variables based on readthedocs environment variables. If
    they are not set, no version warning banner is shown.

    A build on readthedocs will have the following jinja variables available:

      gurobi_rtd = "true"
      gurobi_rtd_version = # version tag: 10.0, 11.0, stable, latest
      gurobi_rtd_version_type = # "branch" for deployments, "external" for PRs
      gurobi_rtd_canonical_url = # the root url of the deployment
      gurobi_rtd_stable_url = # root url of the stable deployment
      gurobi_gh_issue_url = # url to open a github issue for this repo

      pagename = # current page (defined by sphinx)
      theme_version_warning = "true" # can be set to 'false' in html_theme_options
      theme_feedback_banner = "true" # can be set to 'false' in html_theme_options

    With these jinja variables, the URL of the current page in an RTD deployment
    should be:

      {{ gurobi_rtd_canonical_url }}{{ pagename }}.html

    and the same page on the stable branch (i.e. for redirect links) should be:

      {{ gurobi_rtd_stable_url }}{{ pagename }}.html

    A basic testing setup for the stable branch is:

      export READTHEDOCS="True"
      export READTHEDOCS_VERSION_TYPE="branch"
      export READTHEDOCS_GIT_CLONE_URL="git@github.com:Gurobi/repo.git"
      export READTHEDOCS_VERSION="stable"
      export READTHEDOCS_CANONICAL_URL="./stable/"

    To display the "old version" warning set:

      export READTHEDOCS_VERSION="10.0"
      export READTHEDOCS_CANONICAL_URL="./10.0/"

    To display the "in development" warning set:

      export READTHEDOCS_VERSION="latest"
      export READTHEDOCS_CANONICAL_URL="./latest/"
    """

    if os.environ.get("READTHEDOCS") == "True":

        # Version and url information. Store these in distinct jinja variables
        # to prevent clashes with themes we inherit from.
        context["gurobi_rtd"] = "true"
        context["gurobi_rtd_version"] = os.environ.get("READTHEDOCS_VERSION")
        context["gurobi_rtd_version_type"] = os.environ.get("READTHEDOCS_VERSION_TYPE")
        context["gurobi_rtd_canonical_url"] = os.environ.get(
            "READTHEDOCS_CANONICAL_URL"
        )

        # For branch (i.e. not pull request) builds, get the canonical URL of
        # the stable version.
        if context["gurobi_rtd_version_type"] == "branch":
            stem, mid, _ = context["gurobi_rtd_canonical_url"].rpartition(
                context["gurobi_rtd_version"]
            )
            if not (mid and stem.endswith("/")):
                raise ValueError("Unexpected value: url={} version={}".format(
                    context["gurobi_rtd_canonical_url"],
                    context["gurobi_rtd_version"],
                ))
            context["gurobi_rtd_stable_url"] = stem + "stable/"

        # URL for the issues page of the source repo.
        git_clone_url = os.environ.get("READTHEDOCS_GIT_CLONE_URL")
        match = re.match(r"git@github\.com:Gurobi/([\w-]+)\.git", git_clone_url)
        if not match:
            raise ValueError(f"Unexpected value: GIT_CLONE_URL={git_clone_url}")
        repo_name = match.group(1)
        context["gurobi_gh_issue_url"] = (
            f"https://github.com/Gurobi/{repo_name}/issues/new?labels=bug&template=bug_report.md"
        )


def update_config(app):
    """
    Sets options for furo, without theme users having to do it themselves.
    See https://chrisholdgraf.com/blog/2022/sphinx-update-config/
    """
    app.builder.theme_options.update({
        "light_css_variables": {
            "color-brand-primary": "#DD2113",
            "color-brand-content": "#1675a9",
        },
        "dark_css_variables": {
            "color-brand-primary": "#DD2113",
            "color-brand-content": "#1675a9",
        },
        "sidebar_hide_name": True,
        "light_logo": "gurobi_light.svg",
        "dark_logo": "gurobi_dark.svg",
    })


def setup(app):
    app.add_html_theme("gurobi_sphinxtheme", here / "theme")
    app.connect("html-page-context", setup_context)
    app.connect("builder-inited", update_config)
