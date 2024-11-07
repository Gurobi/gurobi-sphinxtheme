import unittest

from docs_gurobi_com.versions import VersionHandler


class TestHandlerCurrentDefaults(unittest.TestCase):

    def setUp(self):
        self.handler = VersionHandler()

    def test_v11(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "11.0",
            "READTHEDOCS_CANONICAL_URL": "https://docs.gurobi.com/opti/11.0/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": False,
            "grb_rtd_version": "11.0",
            "grb_current_version": "11.0",
            "grb_version_status": "current",
            "grb_current_url": "https://docs.gurobi.com/opti/current/",
            "grb_this_url": "https://docs.gurobi.com/opti/11.0/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_v12(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "12.0",
            "READTHEDOCS_CANONICAL_URL": "<docs-url>/12.0/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": True,
            "grb_rtd_version": "12.0",
            "grb_current_version": "11.0",
            "grb_version_status": "beta",
            "grb_current_url": "<docs-url>/current/",
            "grb_this_url": "<docs-url>/12.0/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)


class TestHandler_v11(unittest.TestCase):

    def setUp(self):
        self.handler = VersionHandler()
        self.handler.GUROBI_CURRENT_RELEASE = "11.0"
        self.handler.GUROBI_BETA_RELEASE = "12.0"

    def test_local(self):
        environ = {}
        expected = {"grb_readthedocs": False}
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_current(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "current",
            "READTHEDOCS_CANONICAL_URL": "<docs-url>/current/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": False,
            "grb_rtd_version": "current",
            "grb_current_version": "11.0",
            "grb_version_status": "current",
            "grb_current_url": "<docs-url>/current/",
            "grb_this_url": "<docs-url>/current/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_latest(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "latest",
            "READTHEDOCS_CANONICAL_URL": "<docs-url>/latest/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": True,
            "grb_rtd_version": "latest",
            "grb_current_version": "11.0",
            "grb_version_status": "dev",
            "grb_current_url": "<docs-url>/current/",
            "grb_this_url": "<docs-url>/latest/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_v10(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "10.0",
            "READTHEDOCS_CANONICAL_URL": "<my-docs-url>/10.0/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": True,
            "grb_rtd_version": "10.0",
            "grb_current_version": "11.0",
            "grb_version_status": "old",
            "grb_current_url": "<my-docs-url>/current/",
            "grb_this_url": "<my-docs-url>/10.0/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_v11(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "11.0",
            "READTHEDOCS_CANONICAL_URL": "https://docs.gurobi.com/opti/11.0/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": False,
            "grb_rtd_version": "11.0",
            "grb_current_version": "11.0",
            "grb_version_status": "current",
            "grb_current_url": "https://docs.gurobi.com/opti/current/",
            "grb_this_url": "https://docs.gurobi.com/opti/11.0/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_v12(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "12.0",
            "READTHEDOCS_CANONICAL_URL": "<docs-url>/12.0/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": True,
            "grb_rtd_version": "12.0",
            "grb_current_version": "11.0",
            "grb_version_status": "beta",
            "grb_current_url": "<docs-url>/current/",
            "grb_this_url": "<docs-url>/12.0/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_v99(self):
        environ = {
            "READTHEDOCS": "True",
            "READTHEDOCS_VERSION_TYPE": "branch",
            "READTHEDOCS_VERSION": "99.0",
            "READTHEDOCS_CANONICAL_URL": "<docs-url>/99.0/",
        }
        expected = {
            "grb_readthedocs": True,
            "grb_show_banner": True,
            "grb_rtd_version": "99.0",
            "grb_current_version": "11.0",
            "grb_version_status": "dev",
            "grb_current_url": "<docs-url>/current/",
            "grb_this_url": "<docs-url>/99.0/",
        }
        context = self.handler.create_context(environ)
        self.assertEqual(context, expected)

    def test_is_released_version(self):
        assert self.handler.is_released_version("2.0")
        assert self.handler.is_released_version("10.0")
        assert self.handler.is_released_version("11.0")
        assert not self.handler.is_released_version("12.0")
        assert not self.handler.is_released_version("12.9")
        assert not self.handler.is_released_version("12.9.dev")
        assert not self.handler.is_released_version("v12-nonlinear")

    def test_is_current_version(self):
        assert not self.handler.is_current_version("2.0")
        assert not self.handler.is_current_version("10.0")
        assert self.handler.is_current_version("11.0")
        assert not self.handler.is_current_version("12.0")
        assert not self.handler.is_current_version("12.9")
        assert not self.handler.is_current_version("12.9.dev")
        assert not self.handler.is_current_version("v12-nonlinear")

    def test_is_beta_version(self):
        assert not self.handler.is_beta_version("2.0")
        assert not self.handler.is_beta_version("10.0")
        assert not self.handler.is_beta_version("11.0")
        assert self.handler.is_beta_version("12.0")
        assert not self.handler.is_beta_version("12.9")
        assert not self.handler.is_beta_version("12.9.dev")
        assert not self.handler.is_beta_version("v12-nonlinear")
