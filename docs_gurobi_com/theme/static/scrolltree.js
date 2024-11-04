// Once the page is loaded, scroll the toctree if necessary so that the section
// the user is in is clearly visible.

document.addEventListener('DOMContentLoaded', function () {

    // Find the div containing the scrollable sidebar section, and the sidebar link
    // to the current page.
    const scrollElement = document.querySelector('.sidebar-scroll');
    const parentTocElement = document.querySelector('.toctree-l1.current');
    const currentPageTocElement = document.querySelector('.current.reference.internal');

    // No selected TOC element; nothing to consider (only happens on topmost page)
    if (currentPageTocElement == null) {
        console.log("No TOC element; nothing to scroll");
        return;
    }

    // We want the entire current section of the doc to be in view in the toc. If
    // this is already the case, there's nothing to do.
    const scrollElementRect = scrollElement.getBoundingClientRect();
    const parentTocElementRect = parentTocElement.getBoundingClientRect();
    const currentPageTocElementRect = currentPageTocElement.getBoundingClientRect();

    if (parentTocElementRect.bottom < scrollElementRect.bottom) {
        console.log("Expanded section is fully visible; nothing to scroll");
        return;
    }

    // Offset required to bring the parent element of the current section to the
    // top of the TOC view.
    const parentMinScroll = parentTocElementRect.top - scrollElementRect.top;
    // Offset required to bring the current section link clearly into the TOC view.
    const currentMinScroll = currentPageTocElementRect.bottom - scrollElementRect.bottom;

    if (parentMinScroll < currentMinScroll) {
        console.log("Scrolling current element to bottom of view");
        offset = currentMinScroll;
    } else {
        console.log("Scrolling parent element to top of view");
        offset = parentMinScroll;
    }

    // Scroll the sidebar pane only
    console.log("Scrolling sidebar by offset %f", offset);
    scrollElement.scrollTo({
        top: offset,
        behavior: 'auto',
    });

});
