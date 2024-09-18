# TestTest.py
# --coding:utf-8--
# Time:2024-09-18 18:50:43
# Author:Luckykefu
# Email:3124568493@qq.com
# Description: Test suite for the Test project

import unittest
import os
from src.log import get_logger

logger = get_logger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


class TestProject(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test environment")
        # Add any setup code here

    def tearDown(self):
        logger.info("Tearing down test environment")
        # Add any cleanup code here

    def test_example(self):
        logger.info("Running example test")
        self.assertEqual(1 + 1, 2, "Basic addition test")

    def test_logger(self):
        logger.info("Testing logger functionality")
        # This test doesn't assert anything, but it demonstrates that the logger works
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    # TODO: Add more specific tests for your project here
    # def test_specific_function(self):
    #     from src.your_module import your_function
    #     result = your_function(test_input)
    #     self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
