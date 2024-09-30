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

function getVersionName(slug) {
  if (slug === "11.0") {
    return "11.0 (Current)";
  } else if (slug == "12.0") {
    return "12.0 (Beta)";
  } else if (slug == "latest") {
    return "latest (dev)";
  } else {
    return slug;
  }
}

function getVersionsArray(config) {
  return config.versions.active
    .filter(version => version.slug !== "current")
    .sort((a, b) => parseFloat(b.slug) - parseFloat(a.slug))
    .map(version => ({
      slug: version.slug,
      name: getVersionName(version.slug),
      url: getVersionedURLString(version.urls.documentation)
    }));
}

function getThisVersionSlug() {
  var thisVersionSlug = getMetaContentByName("readthedocs-version-slug");
  if (thisVersionSlug == "current") {
    thisVersionSlug = "11.0";
  }
  return thisVersionSlug;
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
  const thisVersionSlug = getThisVersionSlug();
  const thisVersionName = getVersionName(thisVersionSlug);
  const versionsArray = getVersionsArray(config);

  const flyout = `
    <div class="rst-versions" data-toggle="rst-versions" role="note">
      <span class="rst-current-version" data-toggle="rst-current-version">
        <span class="fa fa-book"> Gurobi</span>
        Version ${thisVersionName}
        <span class="fa fa-caret-down"></span>
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
            <dd>
              <a href="${config.projects.current.urls.downloads}">Downloads</a>
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
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

});
