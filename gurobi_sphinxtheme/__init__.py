import pathlib

from sphinx.util import logging

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


def builder_inited(app):
    """
    Sets options for furo, without theme users having to do it themselves.
    See https://chrisholdgraf.com/blog/2022/sphinx-update-config/
    """
    app.builder.theme_options.update(
        {
            "light_css_variables": {
                "color-brand-primary": "#DD2113",
                "color-brand-content": "#1675A9",
                "color-topic-title": "#1675A9",
                "color-topic-title-background": "#1675A933",
                "color-admonition-title--important": "#1675A9",
                "color-admonition-title-background--important": "#1675A933",
                "color-brand-visited": "#1675A9",
            },
            "dark_css_variables": {
                "color-brand-primary": "#DC4747",
                "color-brand-content": "#5A9BD5",
                "color-brand-visited": "#5A9BD5",
            },
            "light_logo": "gurobi_light.svg",
            "dark_logo": "gurobi_dark.svg",
        }
    )


def setup(app):
    app.add_html_theme("gurobi_sphinxtheme", here / "theme")
    app.connect("builder-inited", builder_inited)
    # Need higher priority to overrule sphinx-tabs
    app.add_css_file("gurobi-tabs.css", priority=600)
