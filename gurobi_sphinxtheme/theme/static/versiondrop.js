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

// Function to populate the dropdown with versions
function populateVersionDropdown(versions) {
    const dropdown = document.getElementById("version-dropdown");

    var thisVersionSlug = getMetaContentByName("readthedocs-version-slug");
    if (thisVersionSlug == "current") {
        thisVersionSlug = "11.0";
    }

    [...versions]
      .sort((a, b) => parseFloat(b.slug) - parseFloat(a.slug))
      .forEach(version => {
        var textContent = "";

        if (version.slug == "current") {
            // skip, it's just an alias
            return;
        } else if (version.slug == "12.0") {
            // beta
            textContent = "12.0 (Beta)";
        } else if (version.slug == "11.0") {
            // current
            textContent = "11.0 (Current)";
        } else {
            // old
            textContent = version.slug;
        }

        const option = document.createElement("option");
        option.value = getVersionedURLString(version.urls.documentation);
        option.textContent = textContent;
        if (version.slug === thisVersionSlug) {
            option.selected = true;
        }
        dropdown.appendChild(option);
    });
}

// Function to redirect user to the selected version page
function navigateToVersion() {
    const dropdown = document.getElementById("version-dropdown");
    const selectedUrl = dropdown.value;

    if (selectedUrl) {
        window.location.href = selectedUrl;
    }
}

// Populate the dropdown once the RTD data is loaded
document.addEventListener("readthedocs-addons-data-ready", function(event) {
    const config = event.detail.data();
    populateVersionDropdown(config.versions.active);
});
