import docutils.nodes
from sphinx.builders.text import TextBuilder
from sphinx.util import logging

logger = logging.getLogger(__name__)


class CheckVisitor(docutils.nodes.NodeVisitor):
    # Visit nodes in a doctree and issue a warning for any failed checks

    def __init__(self, docname, doctree):
        super().__init__(doctree)
        self.docname = docname

    def unknown_visit(self, node):
        pass

    def unknown_departure(self, node):
        pass

    def visit_image(self, node):
        alt_text = node.attributes.get("alt", "")
        if not alt_text:
            uri = node.attributes.get("uri", "")
            logger.warning(
                f"Missing alt text for image '{uri}' in document '{self.docname}'"
            )


class CheckBuilder(TextBuilder):

    name = "check"

    def write_doc(self, docname, doctree):
        # Don't write any output; just run checks using the node visitor
        visitor = CheckVisitor(docname, doctree)
        doctree.walkabout(visitor)
