class VersionHandler:

    GUROBI_CURRENT_RELEASE = "12.0"
    GUROBI_BETA_RELEASE = None
    CURRENT_RELEASE_MIN = 12.0
    CURRENT_RELEASE_MAX = 12.0

    def is_released_version(self, version):
        """Expects a version label from conf.py"""
        try:
            numeric = float(version)
            return numeric <= self.CURRENT_RELEASE_MAX
        except ValueError:
            return False

    def is_beta_version(self, version):
        """Expects a version label from conf.py"""
        return version == self.GUROBI_BETA_RELEASE

    def create_context(self, environ):
        """Given an environment variable dictionary (e.g. os.environ return jinja
        variables to use the html builds).

        Returns:

            {
                "grb_readthedocs": True/False
                "grb_show_banner": True/False
                "grb_rtd_version": <readthedocs version slug>
                "grb_current_version": <version number of current release>
                "grb_version_status": one of: "current", "beta", "dev", "old"
                "grb_this_url": "/url/to/this/build"
                "grb_current_url": "/url/to/current/build"
            }
        """
        context = {}

        readthedocs = environ.get("READTHEDOCS", "") == "True"
        version = environ.get("READTHEDOCS_VERSION", "")
        version_type = environ.get("READTHEDOCS_VERSION_TYPE", "")
        canonical_url = environ.get("READTHEDOCS_CANONICAL_URL", "")

        try:
            numeric_version = float(version)
        except ValueError:
            numeric_version = None

        context["grb_readthedocs"] = readthedocs
        if readthedocs and version_type == "branch":
            if version == "current":
                # Readthedocs 'current'
                context["grb_show_banner"] = False
                context["grb_version_status"] = "current"
            elif version == self.GUROBI_BETA_RELEASE:
                # Version specifically marked as the current beta
                context["grb_show_banner"] = True
                context["grb_version_status"] = "beta"
            elif numeric_version is None:
                # Non-numeric development versions e.g. v12-nonlinear
                context["grb_show_banner"] = True
                context["grb_version_status"] = "dev"
            elif numeric_version > self.CURRENT_RELEASE_MAX:
                # Numeric development version (if we ever have it) e.g. 12.9
                context["grb_show_banner"] = True
                context["grb_version_status"] = "dev"
            elif numeric_version < self.CURRENT_RELEASE_MIN:
                assert numeric_version < float(self.GUROBI_CURRENT_RELEASE)
                context["grb_show_banner"] = True
                context["grb_version_status"] = "old"
            else:
                context["grb_show_banner"] = False
                context["grb_version_status"] = "current"

            stem, mid, _ = canonical_url.rpartition(version)
            assert mid and stem.endswith("/")
            context["grb_current_url"] = stem + "current/"

            context["grb_rtd_version"] = version
            context["grb_current_version"] = self.GUROBI_CURRENT_RELEASE
            context["grb_this_url"] = canonical_url

        return context
