# Sphinx theme for all Gurobi documentation

## Usage

The docs repos that use this theme install from the `main` branch, so only
the following is needed:

`requirements.txt`:

```
gurobi-sphinxtheme @ git+https://github.com/Gurobi/gurobi-sphinxtheme.git@main
```

`conf.py`:

```
project = "<project title>"
copyright = "2025, Gurobi Optimization, LLC"
author = "Gurobi Optimization, LLC"
html_title = "<title to appear in browser tabs>"

html_theme = "gurobi_sphinxtheme"
html_favicon = "https://www.gurobi.com/favicon.ico"
```

We also have a `dev` branch for development which should only be used by
private documentation branches to allow us to review theme changes.

## Styling

Based on [furo](https://github.com/pradyunsg/furo), with minor tweaks.
The stylesheet `gurobi.css` resets some header text sizes.

## Banners

The following banners are added in `page.html`:

- An 'under construction' warning banner on all sites (to be removed in future)
- A version warning banner directing users to the latest release if necessary
- An epilogue banner directing users to search features and support

Banners are configured based on [environment variables set by
readthedocs](https://docs.readthedocs.io/en/stable/reference/environment-variables.html)
and theme options specified in `theme.conf`. Check `setup_context` in
`__init__.py` for details.

**Note that** the 'stable' equivalent version of Gurobi is hard-coded in the
`page.html` template. This needs to be updated when we release a new branch (and
all docs branches should be rebuilt with the new configuration). I can't figure
out a better way yet, as the typical methods don't work:

1. Readthedocs has version warning banners implemented in the new 'beta addons',
   but enabling these cause myriad other problems for us (e.g. subprojects are
   broken).
2. `sphinx-version-warning` is unmaintained. It also relies on querying the RTD
   API for the latest equivalent stable version, which seems to only work if all
   the infrastructure is public.

## Development

We have a `dev` branch which is used to develop the theme further. This
branch should be used only on any Gurobi documentation for the latest
version which is private and not publicly visible. That allows to review
theme changes before we merge them into the `main` branch which is used for
public Gurobi documentation. To used the `dev` branch for a documentation
you need to do the following:

`requirements.txt`:

```
gurobi-sphinxtheme @ git+https://github.com/Gurobi/gurobi-sphinxtheme.git@dev
```

A handy trick when working on the theme is to install in editable mode and use
`livehtml` on one of the docs repos to auto reload. This requires full rebuilds
on every theme change so choose one of the smaller repos if possible.

```
pip install -e </path/to/gurobi-sphinxtheme>
export READTHEDOCS="True"
export READTHEDOCS_VERSION_TYPE="branch"
export READTHEDOCS_GIT_CLONE_URL="git@github.com:Gurobi/repo.git"
export READTHEDOCS_GIT_COMMIT_HASH="aabbccddeeffgg"
export READTHEDOCS_VERSION="10.0"
export READTHEDOCS_CANONICAL_URL="./10.0/"
make SPHINXOPTS="-a --watch </path/to/gurobi-sphinxtheme>" livehtml
```
