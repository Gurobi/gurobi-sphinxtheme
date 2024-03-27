"""
This should do the trick for users of this theme in their conf.py:

  from gurobi_sphinxtheme.conf import *

This sets the html_theme and adds other common configuration.
"""

__all__ = [
    "copyright",
    "author",
    "html_theme",
    "html_favicon",
    "html_theme_options",
    "html_css_files",
    "rst_prolog",
    "latex_elements",
]

# Hopefully self-explanatory stuff
copyright = '2024, Gurobi Optimization'
author = 'Gurobi Optimization'
html_theme = "gurobi_sphinxtheme"
html_favicon = "https://www.gurobi.com/favicon.ico"

# Furo theme configuration
html_theme_options = {
        "light_css_variables": {
            "color-brand-primary": "#DD2113",
            "color-brand-content": "#DD2113",
            "font-size-normal": "50%",
        },
        "dark_css_variables": {
            "color-brand-primary": "#DD2113",
            "color-brand-content": "#DD2113",
            "font-size-normal": "50%",
        },
        "sidebar_hide_name": True,
        "light_logo": "gurobi_light.svg",
        "dark_logo": "gurobi_dark.svg",
    }

# More CSS configuration for furo
html_css_files = ['custom.css']

# Warning banner on html pages
rst_prolog = """
.. only:: html

   .. warning::

      This documentation site is still under construction. It may contain errors
      and omissions. Please visit
      `gurobi.com/documentation <https://www.gurobi.com/documentation>`_ for the
      official documentation of Gurobi.
"""

# Draft background stamp on PDF doc
latex_elements = {
    'preamble': r'''
\usepackage[colorspec=0.9]{draftwatermark}
'''
}
