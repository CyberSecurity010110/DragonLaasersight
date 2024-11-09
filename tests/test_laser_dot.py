# tests/test_laser_dot.py

import unittest
from src.laser_dot import LaserDot

class TestLaserDot(unittest.TestCase):
    def setUp(self):
        self.laser_dot = LaserDot()

    def test_initial_config(self):
        self.assertEqual(self.laser_dot.config["dot_size"], 15)
        self.assertEqual(self.laser_dot.config["dot_color"], "#0000FF")
        self.assertEqual(self.laser_dot.config["opacity"], 0.7)
        self.assertEqual(self.laser_dot.config["brightness"], 1.0)
        self.assertTrue(self.laser_dot.config["visible"])

    def test_update_size(self):
        self.laser_dot.update_size(20)
        self.assertEqual(self.laser_dot.config["dot_size"], 20)

    def test_update_opacity(self):
        self.laser_dot.update_opacity(0.5)
        self.assertEqual(self.laser_dot.config["opacity"], 0.5)

    def test_update_brightness(self):
        self.laser_dot.update_brightness(0.5)
        self.assertEqual(self.laser_dot.config["brightness"], 0.5)

if __name__ == '__main__':
    unittest.main()
