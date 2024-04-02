__all__ = [
    "html_theme",
    "html_theme_options",
    "html_favicon",
    "html_css_files",
    "copyright",
    "author",
]

copyright = '2024, Gurobi Optimization'

author = 'Gurobi Optimization'

html_theme = "gurobi_sphinxtheme"

html_theme_options = {
        "light_css_variables": {
            "color-brand-primary": "#DD2113",
            "color-brand-content": "#1675a9",
            "font-size-normal": "50%",
        },
        "dark_css_variables": {
            "color-brand-primary": "#DD2113",
            "color-brand-content": "#1675a9",
            "font-size-normal": "50%",
        },
        "sidebar_hide_name": True,
        "light_logo": "gurobi_light.svg",
        "dark_logo": "gurobi_dark.svg",
    }

html_favicon = "https://www.gurobi.com/favicon.ico"

html_css_files = ['custom.css']
