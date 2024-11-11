class VersionHandler:

    GUROBI_CURRENT_RELEASE = "11.0"
    GUROBI_BETA_RELEASE = "12.0"

    def is_released_version(self, version):
        """Expects a version label from conf.py"""
        try:
            numeric = float(version)
            return numeric <= float(self.GUROBI_CURRENT_RELEASE)
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
            if version == "current" or version == self.GUROBI_CURRENT_RELEASE:
                context["grb_show_banner"] = False
                context["grb_version_status"] = "current"
            elif version == self.GUROBI_BETA_RELEASE:
                context["grb_show_banner"] = True
                context["grb_version_status"] = "beta"
            elif numeric_version is None or numeric_version > float(
                self.GUROBI_CURRENT_RELEASE
            ):
                context["grb_show_banner"] = True
                context["grb_version_status"] = "dev"
            else:
                assert numeric_version < float(self.GUROBI_CURRENT_RELEASE)
                context["grb_show_banner"] = True
                context["grb_version_status"] = "old"

            stem, mid, _ = canonical_url.rpartition(version)
            assert mid and stem.endswith("/")
            context["grb_current_url"] = stem + "current/"

            context["grb_rtd_version"] = version
            context["grb_current_version"] = self.GUROBI_CURRENT_RELEASE
            context["grb_this_url"] = canonical_url

        return context
