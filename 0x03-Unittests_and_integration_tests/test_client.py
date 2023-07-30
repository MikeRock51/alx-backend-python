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
from unittest.mock import patch, PropertyMock, MagicMock, Mock
import unittest
from parameterized import parameterized, parameterized_class
from typing import Dict
from fixtures import TEST_PAYLOAD
import requests


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
    def test_has_license(self, repo: Dict, license: str,
                         expected: bool) -> None:
        """Performs a unittest on GithubOrgClient.has_license"""
        hL = GithubOrgClient.has_license(repo, license)
        self.assertEqual(hL, expected)


@parameterized_class([
    'org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'
], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient.public_repos method in an integration test"""
    @classmethod
    def setUpClass(cls) -> None:
        """Called before tests are executed"""
        payloads = {
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
            'https://api.github.com/orgs/google': cls.org_payload,
        }

        def get_payload(url):
            """Returns mocked data for the requested url"""
            if url in payloads:
                return Mock(**{'json.return_value': payloads[url]})
            return requests.HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Performs a test on GithubOrgClient.public_repos"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,)

    def test_public_repos_with_license(self) -> None:
        """Performs a test on GithubOrgClient.public_repos with license"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,)

    @classmethod
    def tearDownClass(cls) -> None:
        """Called after all tests are executed"""
        cls.get_patcher.stop()
