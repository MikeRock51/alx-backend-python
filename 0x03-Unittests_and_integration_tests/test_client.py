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
from unittest.mock import patch, PropertyMock, MagicMock
import unittest
from parameterized import parameterized
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """Tests client.GithubOrgClient for correct behavior"""
    @parameterized.expand(["google", "abc"])
    def test_org(self, orgName: str) -> None:
        """Tests that client.GithubOrgClient returns the right value"""
        with patch('client.get_json') as mock:
            gitClient = GithubOrgClient(orgName)
            orgLink = gitClient.ORG_URL.format(org=orgName)
            gitClient.org()
            mock.assert_called_once_with(orgLink)

    @parameterized.expand([
        ("mock_login",
         {'repos_url': 'https://api.github.com/orgs/mock/repos'},),
    ])
    def test_public_repos_url(self, login: str, payload: Dict) -> None:
        """Performs a mock test on GithubOrgClient._public_repos_url"""
        with patch.object(GithubOrgClient, 'org',
                          PropertyMock(return_value=payload)):
            publicRepos = GithubOrgClient(login)._public_repos_url
            self.assertEqual(payload['repos_url'], publicRepos)

    @patch('client.get_json')
    def test_public_repos(self, mockedGet: MagicMock) -> None:
        """Performs a unittest on GithubOrgClient.public_repos"""
        payload = {
            'repos_url': 'https://api.github.com/orgs/mock/repos',
            "repos": [
                {"name": "Mike Rock"},
                {"name": "Musician Connect"}
            ]}

        mockedGet.return_value = payload["repos"]

        with patch.object(GithubOrgClient, '_public_repos_url',
                          PropertyMock(return_value=payload['repos_url']))\
                as mockedPR:

            repoLists = GithubOrgClient('rock-on').public_repos()
            self.assertEqual(repoLists, ["Mike Rock", "Musician Connect"])
            mockedPR.assert_called_once()

        mockedGet.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license: str, expected: bool) -> None:
        """Performs a unittest on GithubOrgClient.has_license"""
        hL = GithubOrgClient('random').has_license(repo, license)
        self.assertEqual(hL, expected)
