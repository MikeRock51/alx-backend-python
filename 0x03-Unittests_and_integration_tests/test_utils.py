#!/usr/bin/env python3
"""
    Create a TestAccessNestedMap class that inherits
    from unittest.TestCase.

    Implement the TestAccessNestedMap.test_access_nested_map
    method to test that the method returns what it is supposed to.

    Decorate the method with @parameterized.expand to test
    the function for following inputs:
        - nested_map={"a": 1}, path=("a",)
        - nested_map={"a": {"b": 2}}, path=("a",)
        - nested_map={"a": {"b": 2}}, path=("a", "b")

    For each of these inputs, test with assertEqual
    that the function returns the expected result.
    The body of the test method should not be longer than 2 lines.
"""
import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """Tests utils.access_nested_map method for right output"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a"), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test utils.access_nested_map method for correct output"""
        output = access_nested_map(nested_map, path)
        self.assertEqual(output, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"),)
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that key error is raised"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests utils.get_json method"""
    @parameterized.expand([
        ("http://example.com", {"payload": True},),
        ("http://holberton.io", {"payload": False},),
    ])
    def test_get_json(self, url, payload):
        """Mock Test of utils.get_json method"""
        mockResponse = Mock()
        mockResponse.json.return_value = payload

        with patch('requests.get', return_value=mockResponse) as mockGet:
            response = get_json(url)
            self.assertEqual(response, payload)
            mockGet.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Tests utils.memoize method"""
    def test_memoize(self):
        """
            Tests that a_method is only called once
            when a_property called twice
        """
        class TestClass:
            """Test Class"""
            def a_method(self):
                """Returns 42"""
                return 42

            @memoize
            def a_property(self):
                """
                    Returns the return value of a_method or
                    retrieves the memoized value if exists
                """
                return self.a_method()

        @patch.object(TestClass, 'a_method')
        def mock_a_method(self, mock):
            obj = TestClass()
            obj.a_property()
            obj.a_property()

            mock.assert_called_once()
