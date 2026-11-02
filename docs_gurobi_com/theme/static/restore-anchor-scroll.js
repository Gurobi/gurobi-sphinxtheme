// Chromium re-applies the URL fragment scroll after each layout until the page
// has loaded, but stops for good once anything scrolls, including a step of a
// smooth scroll animation. Layouts that are only temporary, such as the one
// MathJax forces while measuring equations, can therefore leave the scroll
// pointing at a stale position. Once the page (and MathJax, if present) has
// loaded, scroll to the target again, and keep doing so briefly while late
// layout shifts (such as web fonts loading) settle, unless the reader has
// already scrolled themselves.
//
// Smooth scrolling is disabled meanwhile: with it, the fragment scroll is
// itself an animation, which would stop the browser from re-applying it and
// would carry on towards a stale destination after our correction.
(function () {
  if (!window.location.hash) return;

  var SETTLE_MILLISECONDS = 2000;
  var root = document.documentElement;
  var readerHasScrolled = false;

  root.style.scrollBehavior = "auto";

  ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (eventName) {
    window.addEventListener(eventName, function () {
      readerHasScrolled = true;
    }, { once: true, passive: true });
  });

  function scrollToFragmentTarget() {
    if (readerHasScrolled) return;
    var target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
    if (target) target.scrollIntoView();
  }

  function keepTargetInPlaceWhileLayoutSettles() {
    scrollToFragmentTarget();
    var observer = new ResizeObserver(scrollToFragmentTarget);
    observer.observe(root);
    window.setTimeout(function () {
      observer.disconnect();
      root.style.scrollBehavior = "";
    }, SETTLE_MILLISECONDS);
  }

  window.addEventListener("load", function () {
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      window.MathJax.startup.promise.then(keepTargetInPlaceWhileLayoutSettles);
    } else {
      keepTargetInPlaceWhileLayoutSettles();
    }
  });
})();
