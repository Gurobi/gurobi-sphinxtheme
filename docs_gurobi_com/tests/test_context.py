import unittest

from docs_gurobi_com.context import ContextBuilder


class TestContextVersion11(unittest.TestCase):

    def setUp(self):
        self.builder = ContextBuilder()
        self.builder.GUROBI_CURRENT_RELEASE = "11.0"
        self.builder.GUROBI_BETA_RELEASE = "12.0"

    def test_local(self):
        environ = {}
        expected = {"grb_readthedocs": False}
        context = self.builder.create_context(environ)
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
        context = self.builder.create_context(environ)
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
        context = self.builder.create_context(environ)
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
        context = self.builder.create_context(environ)
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
        context = self.builder.create_context(environ)
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
        context = self.builder.create_context(environ)
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
        context = self.builder.create_context(environ)
        self.assertEqual(context, expected)
