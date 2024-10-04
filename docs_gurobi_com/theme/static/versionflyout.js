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
        <span class="fa fa-book">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -100 1664 1664" width="13" height="13" style="transform: scaleY(-1) translateY(-1px);">
            <path fill="var(--color-foreground-primary)" d="M1639 1058q40 -57 18 -129l-275 -906q-19 -64 -76.5 -107.5t-122.5 -43.5h-923q-77 0 -148.5 53.5t-99.5 131.5q-24 67 -2 127q0 4 3 27t4 37q1 8 -3 21.5t-3 19.5q2 11 8 21t16.5 23.5t16.5 23.5q23 38 45 91.5t30 91.5q3 10 0.5 30t-0.5 28q3 11 17 28t17 23q21 36 42 92t25 90q1 9 -2.5 32t0.5 28q4 13 22 30.5t22 22.5q19 26 42.5 84.5t27.5 96.5q1 8 -3 25.5t-2 26.5q2 8 9 18t18 23t17 21q8 12 16.5 30.5t15 35t16 36t19.5 32t26.5 23.5t36 11.5t47.5 -5.5l-1 -3q38 9 51 9h761q74 0 114 -56t18 -130l-274 -906q-36 -119 -71.5 -153.5t-128.5 -34.5h-869q-27 0 -38 -15q-11 -16 -1 -43q24 -70 144 -70h923q29 0 56 15.5t35 41.5l300 987q7 22 5 57q38 -15 59 -43zM575 1056q-4 -13 2 -22.5t20 -9.5h608q13 0 25.5 9.5t16.5 22.5l21 64q4 13 -2 22.5t-20 9.5h-608q-13 0 -25.5 -9.5t-16.5 -22.5zM492 800q-4 -13 2 -22.5t20 -9.5h608q13 0 25.5 9.5t16.5 22.5l21 64q4 13 -2 22.5t-20 9.5h-608q-13 0 -25.5 -9.5t-16.5 -22.5z" />
          </svg>
          Gurobi
        </span>
        ${thisVersionName}
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24">
          <path fill="var(--color-foreground-primary)" d="M12 5.83L15.17 9 16.59 7.59 12 3 7.41 7.59 8.83 9 12 5.83zM12 18.17L8.83 15 7.41 16.41 12 21l4.59-4.59L15.17 15 12 18.17z"/>
        </svg>
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
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });

});
