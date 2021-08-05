import unittest
import app


class dataValidation(unittest.TestCase):
    def test_string(self):
        self.assertTrue(app.is_string("khanya"), True)


    def test_length(self):
        self.assertTrue(app.length("khanya"), True)


    def test_number(self):
        self.assertTrue(app.is_number("3846346832"), True)


if __name__ == '__main__':
    unittest.main()
