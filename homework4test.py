import unittest
from individual_and_family import *
from userstories import *

checker = UserStoryChecker()
class testUserStory17(unittest.TestCase):

    def test_marriageChecker(self):
        self.assertEqual(checker.marriage_to_descend(), False)
        print("Passed Equivalence")
        self.assertFalse(checker.marriage_to_descend(), Family)
        print("Passed did not return a family")
        self.assertFalse(checker.marriage_to_descend(), Individual)
        print("-----passed------")
        self.assertFalse(checker.marriage_to_descend(), int)
        print("-----passed------")
        self.assertFalse(checker.marriage_to_descend(), str)
        print("-----passed------")

    def runTest():
        test_marriageChecker()
      

if __name__ == "__main__":
    unittest.main()





