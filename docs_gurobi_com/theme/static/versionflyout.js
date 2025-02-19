// We are rendering the flyout ourselves so we disable the flyout in the RTD
// dashboard. This sets flyout.enabled to false in the addons json payload,
// which disables building the default flyout.

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
      name: getFlyoutVersionNameFromSlug(version.slug),
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

document.addEventListener("readthedocs-addons-internal-data-ready", function (event) {

  const config = event.detail.data();
  const thisVersionSlug = config.versions.current.slug;
  const thisVersionName = getFlyoutVersionNameFromSlug(thisVersionSlug);
  const versionsArray = getVersionsArray(config);

  const flyout = `
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
  `;

  const thisVersionLabel = `
    ${thisVersionName}
    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24">
      <path fill="var(--color-foreground-primary)" d="M12 5.83L15.17 9 16.59 7.59 12 3 7.41 7.59 8.83 9 12 5.83zM12 18.17L8.83 15 7.41 16.41 12 21l4.59-4.59L15.17 15 12 18.17z"/>
    </svg>
  `;

  // Inject the generated content into the placeholders created in versionflyout.html
  document.getElementById("grb-rtd-flyout-content").innerHTML = flyout;
  document.getElementById("grb-rtd-version-label").innerHTML = thisVersionLabel;

  document.querySelector(".grb-rtd-current-version").addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

});
