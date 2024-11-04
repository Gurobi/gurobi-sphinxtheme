import bs4
from sphinx.util import logging

logger = logging.getLogger(__name__)


def extend_toctree(pagename, context):
    """Replace the toctree generator in the page context with one that injects
    the page toc under the current page element."""

    toctree_original = context["toctree"]

    def toctree_adjusted(*args, **kwargs):
        """Parse sphinx's generated toctree and the page toc. Inject the page
        toc under the current page element."""
        toctree_html = toctree_original(*args, **kwargs)
        toctree_soup = bs4.BeautifulSoup(toctree_html, features="html.parser")
        current_links = toctree_soup.find_all("li", class_="current")

        if current_links:
            toc_soup = bs4.BeautifulSoup(context["toc"], features="html.parser")
            # The page toc begins with a parent element which matches the
            # current page element in the toctree. Hence, the next <ul> tree
            # level needs to be inserted under the deepest "current" node.
            ul_elements = toc_soup.find_all("ul")
            if len(ul_elements) > 1:
                current_page = current_links[-1]
                if current_page.find("a").attrs["href"] != "#":
                    raise ValueError(
                        f"extend_toctree({pagename=}): "
                        "unexpected value for current page href"
                    )
                if ul_elements[0].find("a").attrs["href"] != "#":
                    raise ValueError(
                        f"extend_toctree({pagename=}): "
                        "unexpected value for internal href"
                    )
                sections = ul_elements[1]
                current_page.append(sections)
                toctree_html = str(toctree_soup)
                logger.debug(f"toctree() manipulated for {pagename=}")

        return toctree_html

    context["toctree"] = toctree_adjusted
