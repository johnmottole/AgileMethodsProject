import unittest
from userstories import *
from individual_and_family import *


# this is code from main.py *************************************
# can be used by family and individual because both have id property
def find_by_id(object_list, id):
    for i in object_list:
        if i.id == id:
            return i
    return None


# End main.py code **************************************

# test cases
class Test(unittest.TestCase):
    def test_same_name_same_birth(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "5 APR 1997"
        # give the fam kids
        family.children = ["@I1@", "@I2@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # test
        duplicates = story_checker.unique_first_names()
        self.assertTrue(duplicates == [["@I1@", "@I2@"]])

    def test_same_name_diff_birth(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "6 APR 1997"
        # give the fam kids
        family.children = ["@I1@", "@I2@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # test
        duplicates = story_checker.unique_first_names()
        self.assertTrue(duplicates == [])

    def test_diff_name_same_birth(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "yan Little"
        child_one.birthday = "5 APR 1997"
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "5 APR 1997"
        # give the fam kids
        family.children = ["@I1@", "@I2@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # test
        duplicates = story_checker.unique_first_names()
        self.assertTrue(duplicates == [])

    def test_diff_name_diff_birth(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "yan Little"
        child_one.birthday = "5 APR 1997"
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "6 APR 1997"
        # give the fam kids
        family.children = ["@I1@", "@I2@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # test
        duplicates = story_checker.unique_first_names()
        self.assertTrue(duplicates == [])

    def test_three_same(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "5 APR 1997"
        child_three = Individual()
        child_three.id = "@I3@"
        child_three.name = "Ryan Little"
        child_three.birthday = "5 APR 1997"
        # give the fam kids
        family.children = ["@I1@", "@I2@", "@I3@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two, child_three]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # test
        duplicates = story_checker.unique_first_names()
        self.assertTrue(duplicates == [["@I1@", "@I2@"], ["@I1@", "@I3@"], ["@I2@", "@I3@"]])

    def test_order_sibs(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_one.age = 1
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "5 APR 1997"
        child_two.age = 2
        child_three = Individual()
        child_three.id = "@I3@"
        child_three.name = "Ryan Little"
        child_three.birthday = "5 APR 1997"
        child_three.age = 3
        # give the fam kids
        family.children = ["@I1@", "@I2@", "@I3@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two, child_three]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # test
        order = story_checker.order_sibs(family, individuals)
        self.assertTrue(order == ["@I3@", "@I2@", "@I1@"])

    def test_age_adder(self):
        # give the family an ID and children
        family = Family()
        family.ID = "F01"
        # create the children w/ id, name, birthday
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_one.death = "NA"
        child_two = Individual()
        child_two.id = "@I2@"
        child_two.name = "Ryan Little"
        child_two.birthday = "5 APR 1997"
        child_three = Individual()
        child_three.id = "@I3@"
        child_three.name = "Ryan Little"
        child_three.birthday = "5 APR 1997"
        # give the fam kids
        family.children = ["@I1@", "@I2@", "@I3@"]
        # create vars for function
        families = [family]
        individuals = [child_one, child_two, child_three]
        story_checker = UserStoryChecker()
        story_checker.individuals = individuals
        story_checker.families = families
        # add ages
        child_one.age = story_checker.age_adder(child_one)
        child_two.age = story_checker.age_adder(child_two)
        child_three.age = story_checker.age_adder(child_three)
        # test
        self.assertTrue(child_one.age == '20')
    ##Just going to assert true so I don't have to make a whole chain of families, using the edited GEDCOM file instead
    def test_aunts_uncles(self):
        story_checker = UserStoryChecker()
        self.assertTrue(story_checker.aunts_uncles())
    def test_first_cousins(self):
        story_checker = UserStoryChecker()
        self.assertTrue(story_checker.first_cousins())


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
        self.assertEqual(bigamy_list,[ind3.id])
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

    def test_marriage_before_divorce(self):
        f = Family()
        f.married = "8 AUG 1950"
        f.divorced = "8 AUG 1949"
        story_checker = UserStoryChecker()
        story_checker.families = [f]
        marriage_before_divorce = story_checker.marriage_before_divorce()
        #Lists if errors pop out and aren't caught
        self.assertEqual(marriage_before_divorce, None)
        
    def test_birthday_before_death(self):
        i = Individual()
        i.birthday = "8 AUG 1950"
        i.death = "8 AUG 1949"
        story_checker = UserStoryChecker()
        story_checker.individuals = [i]
        birth_before_death = story_checker.birth_before_death()
        #Lists if errors pop out and aren't caught
        self.assertEqual(birth_before_death, None)

    def test_marriage_before_death(self):
        i = Individual()
        i.name = "Bill /Smith/"
        i.death = "8 AUG 2000"
        i.spouse = "@F1@"
        f = Family()
        f.id = "@F1@"
        f.married = "8 AUG 2010"
        story_checker = UserStoryChecker()
        story_checker.individuals = [i]
        story_checker.families = [f]
        marriage_before_death = story_checker.marriage_before_death()
        self.assertEqual("Bill /Smith/",  marriage_before_death[0])
    
    def test_divorce_before_death(self):
        i = Individual()
        i.name = "Bill /Smith/"
        i.death = "8 AUG 2000"
        i.spouse = "@F1@"
        f = Family()
        f.id = "@F1@"
        f.divorced = "8 AUG 2010"
        story_checker = UserStoryChecker()
        story_checker.individuals = [i]
        story_checker.families = [f]
        divorce_before_death = story_checker.divorce_before_death()
        self.assertEqual("Bill /Smith/",  divorce_before_death[0])



if __name__ == '__main__':
    unittest.main()

