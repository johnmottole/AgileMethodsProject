import unittest
from userstories import *
from individual_and_family import *
class Test(unittest.TestCase):
    def test_bigamy(self):
        ind1 = Individual()
        ind1.name = "Husband1"
        ind1.id = "I01"
        ind2 = Individual()
        ind2.name = "Husband2"
        ind2.id = "I02"
        ind3 = Individual()
        ind3.name = "Wife"
        ind3.id = "I03"
        fam1 = Family()
        fam1.husband_name = ind1.name
        fam1.husband_id = ind1.id
        fam1.wife_name = ind3.name
        fam1.wife_id = ind3.id
        fam2 = Family()
        fam2.husband_name = ind2.name
        fam2.husband_id = ind2.id
        fam2.wife_name = ind3.name
        fam2.wife_id = ind3.id
        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind1,ind2,ind3]
        storyChecker.families = [fam1,fam2]
        bigamy_list = storyChecker.no_bigamy()
        self.assertEquals(bigamy_list,[ind3.id])
    def test_parents_too_old(self):
        ind1 = Individual()
        ind1.name = "Husband"
        ind1.id = "I01"
        ind1.birthday = "7 JUN 1950"
        ind2 = Individual()
        ind2.name = "Wife"
        ind2.id = "I02"
        ind2.birthday = "7 JUN 1949"
        ind3 = Individual()
        ind3.name = "Child1"
        ind3.id = "I03"
        ind3.birthday = "7 JUN 2010"
        ind4 = Individual()
        ind4.name = "Child2"
        ind4.id = "I04"
        ind4.birthday = "7 JUN 2040"
        fam1 = Family()
        fam1.husband_name = ind1.name
        fam1.husband_id = ind1.id
        fam1.wife_name = ind2.name
        fam1.wife_id = ind2.id
        fam1.children = [ind3.id,ind4.id]
        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind1, ind2, ind3, ind4]
        storyChecker.families = [fam1]
        error_list = storyChecker.parents_to_old()
        self.assertIn("Error US12: " + ind3.name + "(" + ind3.id + ") is more than 60 years younger than mother",error_list)
        self.assertIn("Error US12: " + ind4.name + "(" + ind4.id + ") is more than 60 years younger than mother",error_list)
        self.assertIn("Error US12: " + ind4.name + "(" + ind4.id + ") is more than 80 years younger than father",error_list)

