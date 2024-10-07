import pathlib

from sphinx.util import logging

import docs_gurobi_com.versions as gurobi_versions

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


def configure_latex(config, git_commit_hash=None):
    """Set common options for latex PDF builds.

    Note: for this to take effect, docs_gurobi_com must also be loaded as an
    extension, not just as html_theme (which only applies to the html builder).
    """

    # Projects should define 'version' in their conf.py file. If it's empty or
    # not defined, no version line is added to the title page (this is also a
    # valid setup, e.g. for the cloud guide which is not versioned).
    if config.version:
        if gurobi_versions.is_beta_version(config.version):
            version_string = f"Version {config.version} (beta)"
        elif gurobi_versions.is_released_version(config.version):
            version_string = f"Version {config.version}"
        else:
            version_string = f"Version {config.version} (dev)"
    else:
        version_string = ""

    # Revision string; adds the given docs commit hash below the build date
    if git_commit_hash is not None:
        short = git_commit_hash[:9]
        revision_string = f"Revision: {short}"
    else:
        revision_string = "<Not an official docs build>"

    # Preamble: include the gurobidocs package and define necessary commands
    # that are used in its \grbmaketitle
    newline = "\n"
    # fmt: off
    preamble_parts = [
        r"\usepackage{gurobidocs}",
        newline,
        r"\newcommand{\GRBversionlabel}{", version_string, "}",
        newline,
        r"\newcommand{\GRBdocrevision}{", revision_string, "}",
        newline,
    ]
    # fmt: on
    config.latex_elements["preamble"] = "".join(preamble_parts)

    # We define \grbmaketitle in gurobidocs.sty. Use it instead of
    # \sphinxmaketitle
    config.latex_elements["maketitle"] = r"\grbmaketitle"

    # Include files used in our pdf builds. Sphinx's documentation states that
    # paths are set relative to app.confdir, but fully resolved paths also seem
    # to work (pathlib's walk_up would be ideal, but it's only in python 3.12).
    latex_additional = here.joinpath("latex").resolve()
    config.latex_additional_files.extend(
        [
            str(latex_additional.joinpath("gurobipdflogo.png")),
            str(latex_additional.joinpath("gurobidocs.sty")),
        ]
    )
