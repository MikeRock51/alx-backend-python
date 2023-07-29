#!/usr/bin/env python3
"""
    Familiarize yourself with the client.GithubOrgClient class.

    - In a new test_client.py file, declare the
      TestGithubOrgClient(unittest.TestCase) class
      and implement the test_org method.
    - This method should test that GithubOrgClient.org
      returns the correct value.
    - Use @patch as a decorator to make sure get_json is called once with the
      expected argument but make sure it is not executed.
    - Use @parameterized.expand as a decorator to parametrize the test with a
      couple of org examples to pass to GithubOrgClient, in this order:
        - google
        - abc

    Of course, no external HTTP calls should be made.
"""

from client import GithubOrgClient
from unittest.mock import Mock, patch
import unittest
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Tests client.GithubOrgClient for correct behavior"""
    @parameterized.expand(["google", "abc"])
    def test_org(self, orgName):
        """Tests that client.GithubOrgClient returns the right value"""
        with patch('client.get_json') as mock:
            gitClient = GithubOrgClient(orgName)
            orgLink = gitClient.ORG_URL.format(org=orgName)
            gitClient.org()
            mock.assert_called_once_with(orgLink)
