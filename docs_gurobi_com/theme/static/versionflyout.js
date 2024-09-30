// Once we are rendering the flyout ourselves, we just disable the flyout in
// the RTD dashboard. This (presumably) sets flyout.enabled to false in the
// addons json payload, which disables building the default flyout.

// Selector based on:
// https://github.com/python/cpython/pull/116966/files
//
// Flyout (to do) based on:
// https://github.com/readthedocs/sphinx_rtd_theme/pull/1526/files
//
// With assistance from chatGPT

// Retrieve content attribute from a meta tag with the given name
function getMetaContentByName(name) {
  var metaTag = document.querySelector('meta[name="' + name + '"]');
  if (metaTag) {
      return metaTag.getAttribute('content');
  } else {
      return null;  // Return null if the meta tag is not found
  }
}

function appendToBaseUrl(baseUrl, relativeUrl) {
  // Ensure the relative URL does not start with a slash
  if (relativeUrl.startsWith('/')) {
      relativeUrl = relativeUrl.substring(1);
  }

  // Create a new URL object, which will handle combining base and relative paths
  return new URL(relativeUrl, baseUrl).href;
}

// Resolve the path to the given docs version
function getVersionedURLString(baseUrl) {
  var relativeUrl = getMetaContentByName("readthedocs-resolver-filename");
  return appendToBaseUrl(baseUrl, relativeUrl);
}

// Customise naming by version slug.
// This way we are explicit about the meaning of 'current' and can
// mark the beta version explicitly.
// Note: the explicit 11.0 version and 'current' are separate links, though
// they hold the same content.
function getVersionName(slug) {
  if (slug === "current") {
    return "Current (11.0)";
  } else if (slug == "12.0") {
    return "12.0 (Beta)";
  } else {
    return slug;
  }
}

// Process the config.versions.active section of the addons payload, returning
// a new versions array for rendering the flyout.
// 1. Sorts so that we have the order:
//    - current
//    - numeric versions in descending order
//    - other non-numeric slugs
// 2. Maps each element with an adjusted name and a URL for the same page in
//    in the target version
function getVersionsArray(config) {
  return config.versions.active
    .sort((a, b) => {
      if (a.slug == "current") return -1;
      if (b.slug == "current") return 1;
      return parseFloat(b.slug) - parseFloat(a.slug)
    })
    .map(version => ({
      slug: version.slug,
      name: getVersionName(version.slug),
      url: getVersionedURLString(version.urls.documentation)
    }));
}

function renderVersions(versions, thisVersionSlug) {
  if (!versions.length) {
    return "";
  }
  const versionsHTML = `
    <dl>
      <dt>Versions</dt>
      ${versions
        .map(
          (version) => `
      <dd ${version.slug === thisVersionSlug ? 'class="rtd-current-item"' : ""}>
        <a href="${version.url}">${version.name}</a>
      </dd>
      `,
        )
        .join("\n")}
    </dl>
  `;
  return versionsHTML;
}

function renderDownloads(config) {
  if (!Object.keys(config.versions.current.downloads).length) {
    return "";
  }
  const downloadsNameDisplay = {
    pdf: "PDF",
    epub: "Epub",
    htmlzip: "HTML",
  };

  const downloadsHTML = `
    <dl>
      <dt>Downloads</dt>
      ${Object.entries(config.versions.current.downloads)
        .map(
          ([name, url]) => `
        <dd>
          <a href="${url}">${downloadsNameDisplay[name]}</a>
        </dd>
      `,
        )
        .join("\n")}
    </dl>
  `;
  return downloadsHTML;
}

document.addEventListener("readthedocs-addons-data-ready", function (event) {
  const config = event.detail.data();
  const thisVersionSlug = config.versions.current.slug;
  const thisVersionName = getVersionName(thisVersionSlug);
  const versionsArray = getVersionsArray(config);

  const flyout = `
    <div class="rst-versions" data-toggle="rst-versions" role="note">
      <span class="rst-current-version" data-toggle="rst-current-version">
        <span class="fa fa-book"> Gurobi</span>
        ${thisVersionName}
        <span class="fa fa-caret-up"></span>
      </span>
      <div class="rst-other-versions">
        <div class="injected">
          ${renderVersions(versionsArray, thisVersionSlug)}
          ${renderDownloads(config)}
          <dl>
            <dt>On Read the Docs</dt>
            <dd>
              <a href="${config.projects.current.urls.home}">Project Home</a>
            </dd>
            <dd>
              <a href="${config.projects.current.urls.builds}">Builds</a>
            </dd>
          </dl>
          <hr />
          <small>
            <span>Hosted by <a href="https://about.readthedocs.com">Read the Docs</a></span>
          </small>
        </div>
      </div>
  `;

  // Inject the generated flyout into the body HTML element.
  document.getElementById("custom-rtd-flyout-content").innerHTML = flyout;

  document.querySelector(".rst-current-version").addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      var spanElement = document.querySelector('span.fa-caret-down');
      if (spanElement) {
        spanElement.classList.replace('fa-caret-down', 'fa-caret-up');
      }
      content.style.display = "none";
    } else {
      var spanElement = document.querySelector('span.fa-caret-up');
      if (spanElement) {
        spanElement.classList.replace('fa-caret-up', 'fa-caret-down');
      }
      content.style.display = "block";
    }
  });

});
