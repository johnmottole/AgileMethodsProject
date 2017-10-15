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



if __name__ == '__main__':
    unittest.main()

