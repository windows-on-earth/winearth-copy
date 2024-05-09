import unittest
import winearth_copy.arguments


class TestParseArguments(unittest.TestCase):
    def test_parse_arguments(self):
        args = winearth_copy.arguments.parse_arguments(
            ["--config", "config_file.txt", "--query-date", "20240101"]
        )
        self.assertEqual(args.configuration_file, "config_file.txt")
        self.assertEqual(args.query_date, "20240101")

    def test_parse_arguments_missing_config(self):
        with self.assertRaises(SystemExit):
            winearth_copy.arguments.parse_arguments(["--query-date", "20240101"])
