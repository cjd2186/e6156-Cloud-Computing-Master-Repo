import unittest
from unittest.mock import patch
from composite_svc_sync import fetch_sync  # Replace 'your_module' with the actual module name

class TestFetchSync(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_sync(self, mock_requests_get):
        # Mocking the response
        expected_data = {"key": "value"}
        mock_requests_get.return_value.json.return_value = expected_data

        # Input resource
        test_resource = {
            "url": "http://example.com/api/resource",
            "resource": "example_resource"
        }

        # Calling the function
        result = fetch_sync(test_resource)

        # Assertions
        mock_requests_get.assert_called_once_with("http://example.com/api/resource")
        self.assertEqual(result["resource"], "example_resource")
        self.assertEqual(result["data"], expected_data)

if __name__ == '__main__':
    unittest.main()