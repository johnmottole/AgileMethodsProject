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

    #RL -- test list printer returns
    def test_list_dead(self):
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_one.death = "6 APR 1999"

        story_checker = UserStoryChecker()
        story_checker.individuals = [child_one]
        individuals = [child_one]

        self.assertTrue(individuals == story_checker.list_dead())

    def test_list_living_married(self):
        child_one = Individual()
        child_one.id = "@I1@"
        child_one.name = "Ryan Little"
        child_one.birthday = "5 APR 1997"
        child_one.death = "NA"
        child_one.spouse = "@I99@"

        story_checker = UserStoryChecker()
        story_checker.individuals = [child_one]
        individuals = [child_one]

        self.assertTrue(individuals == story_checker.list_living_married())
    def test_marriage_to_descend(self):
        ind1 = Individual()
        ind1.name = "Husband1"
        ind1.id = "I01"
        ind1.gender = 'M'
       
        ind2 = Individual()
        ind2.name = "Husband2"
        ind2.id = "I02"
        ind2.gender = 'F'
        ind2.spouse = ind1.id
        ind3 = Individual()
        ind3.name = "Wife"
        ind3.id = "I03"
        ind3.gender = 'F'
        ind3.spouse = ind1.id
        ind1.spouse = ind3.id
        fam1 = Family()
        fam1.husband_name = ind1.name
        fam1.husband_id = ind1.id
        fam1.wife_name = ind3.name
        fam1.wife_id = ind3.id
        fam2 = Family()
        fam2.husband_name = ind1.name
        fam2.husband_id = ind1.id
        fam2.wife_name = ind2.name
        fam2.wife_id = ind2.id
        fam2.children = [ind3.id]

        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind1,ind2,ind3]
        storyChecker.families = [fam2, fam1]
        marriedtodesc = storyChecker.marriage_to_descend()
        self.assertEqual(marriedtodesc,ind1.id)
    def test_unique_spouses(self):
        fam1 = Family()
        fam2 = Family()
        fam1.id = "@F1@"
        fam2.id = "@F2@"
        fam1.husband_id = "@I1@"
        fam1.wife_id = "@I2@"
        fam1.married = "11/12/2017"
        fam2.husband_id = "@I1@"
        fam2.wife_id = "@I3@"
        fam2.married = "11/12/2017"
        story_checker = UserStoryChecker()
        story_checker.families = [fam1, fam2]
        myList = story_checker.unique_spouses()
        self.assertTrue("@F1@" in myList)
    def test_unique_names_gedcom(self):
        ind1 = Individual()
        ind1.name = "Husband1"
        ind1.id = "I01"
        ind1.gender = 'M'
       
        ind2 = Individual()
        ind2.name = "Husband1"
        ind2.id = "I02"
        ind2.gender = 'F'
        ind2.spouse = ind1.id
        ind3 = Individual()
        ind3.name = "Husband2"
        ind3.id = "I03"
        ind3.gender = 'F'
        story_checker = UserStoryChecker()
        story_checker.individuals = [ind1, ind2, ind3]
        myList = story_checker.unique_names_gedcom()
        self.assertTrue("Husband1" in myList)
    def test_aunts_uncles(self):
        story_checker = UserStoryChecker()
#        self.assertTrue(story_checker.aunts_uncles())
    def test_first_cousins(self):
        story_checker = UserStoryChecker()
        #self.assertTrue(story_checker.first_cousins())
    def test_unique_ids_fam(self):
        fam1 = Family()
        fam2 = Family()
        fam1.id = "@F1@"
        fam2.id = "@F1@"
        story_checker = UserStoryChecker()
        story_checker.families = [fam1, fam2]
        self.assertTrue({"@F1@"}, story_checker.unique_ids_fam())
    def test_unique_ids_ind(self):
        ind1 = Individual()
        ind2 = Individual()
        ind1.id = "@I1@"
        ind2.id = "@I1@"
        story_checker = UserStoryChecker()
        story_checker.individuals = [ind1, ind2]
        self.assertEqual({"@I1@"}, story_checker.unique_ids_ind())
    def test_gender_roles(self):
        story_checker = UserStoryChecker()
        #self.assertTrue(story_checker.gender_roles())

        #self.assertTrue(story_checker.first_cousins())


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

    def test_younger_than_150(self):
        i = Individual()
        i.name = "John /Doe/"
        i.birthday = "8 AUG 1800"
        story_checker = UserStoryChecker()
        story_checker.individuals = [i]
        younger = story_checker.younger_than_150()
        self.assertTrue(younger.get(i.name) == "8 AUG 1800")

    def test_birth_before_parents(self):
        ind1 = Individual()
        ind2 = Individual()
        ind3 = Individual()
        ind1.name = "John /Doe"
        ind2.name = "Mom /Doe/"
        ind3.name = "Dad /Doe/"
        ind1.child = "@F1@"
        ind1.id = "@I1@"
        ind3.id = "@I3@"
        ind2.id = "@I2@"
        ind2.spouse = "@F1@"
        ind3.spouse = "@F1@"
        ind1.birthday = "8 AUG 1900"
        ind2.birthday = "8 AUG 1950"
        ind3.birthday = "8 AUG 1960"
        fam1 = Family()
        fam1.id = "@F1@"
        fam1.husband_id = "@I3@"
        fam1.wife_id = "@I2@"
        fam1.children = ["@I1@"]
        story_checker = UserStoryChecker()
        story_checker.individuals = [ind1, ind2, ind3]
        story_checker.families = [fam1]
        older = story_checker.birth_before_parents()

        self.assertEqual(older.get(ind1.name), [ind2.name, ind3.name])

    def test_sibling_spacing(self):
        ind1 = Individual()
        ind1.name = "Sibling1"
        ind1.id = "I01"
        ind1.birthday = "7 JUN 1950"
        ind2 = Individual()
        ind2.name = "Sibling2"
        ind2.id = "I02"
        ind2.birthday = "22 JUN 1950"
        fam1 = Family()
        fam1.children = [ind1.id, ind2.id]
        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind1, ind2]
        storyChecker.families = [fam1]
        sibling_pairs = storyChecker.sibling_spacing()
        self.assertEquals(len(sibling_pairs),1)
        self.assertIn(ind1,sibling_pairs[0])
        self.assertIn(ind2,sibling_pairs[0])
    def test_multiple_births(self):
        ind1 = Individual()
        ind1.name = "Sibling1"
        ind1.id = "I01"
        ind1.birthday = "7 JUN 1950"
        ind2 = Individual()
        ind2.name = "Sibling2"
        ind2.id = "I02"
        ind2.birthday = "7 JUN 1950"
        ind3 = Individual()
        ind3.name = "Sibling3"
        ind3.id = "I03"
        ind3.birthday = "7 JUN 1950"
        ind4 = Individual()
        ind4.name = "Sibling4"
        ind4.id = "I04"
        ind4.birthday = "7 JUN 1950"
        ind5 = Individual()
        ind5.name = "Sibling5"
        ind5.id = "I05"
        ind5.birthday = "7 JUN 1950"
        ind6 = Individual()
        ind6.name = "Sibling6"
        ind6.id = "I06"
        ind6.birthday = "7 JUN 1950"
        fam1 = Family()
        fam1.children = [ind1.id, ind2.id,ind3.id, ind4.id,ind5.id, ind6.id]
        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind1, ind2, ind3,ind4,ind5,ind6]
        storyChecker.families = [fam1]
        families_returned = storyChecker.multuple_births()
        self.assertEquals(len(families_returned),1)
        self.assertIn(fam1,families_returned)
    def test_fewer_15_children(self):
        ind1 = Individual()
        ind1.name = "Sibling1"
        ind1.id = "I01"
        ind1.birthday = "7 JUN 1950"
        ind2 = Individual()
        ind2.name = "Sibling2"
        ind2.id = "I02"
        ind2.birthday = "7 JUN 1950"
        ind3 = Individual()
        ind3.name = "Sibling3"
        ind3.id = "I03"
        ind3.birthday = "7 JUN 1950"
        ind4 = Individual()
        ind4.name = "Sibling4"
        ind4.id = "I04"
        ind4.birthday = "7 JUN 1950"
        ind5 = Individual()
        ind5.name = "Sibling5"
        ind5.id = "I05"
        ind5.birthday = "7 JUN 1950"
        ind6 = Individual()
        ind6.name = "Sibling6"
        ind6.id = "I06"
        ind6.birthday = "7 JUN 1950"
        ind7 = Individual()
        ind7.name = "Sibling7"
        ind7.id = "I07"
        ind7.birthday = "7 JUN 1950"
        ind8 = Individual()
        ind8.name = "Sibling2"
        ind8.id = "I02"
        ind8.birthday = "7 JUN 1950"
        ind9 = Individual()
        ind9.name = "Sibling3"
        ind9.id = "I03"
        ind9.birthday = "7 JUN 1950"
        ind10 = Individual()
        ind10.name = "Sibling4"
        ind10.id = "I04"
        ind10.birthday = "7 JUN 1950"
        ind11 = Individual()
        ind11.name = "Sibling5"
        ind11.id = "I05"
        ind11.birthday = "7 JUN 1950"
        ind12 = Individual()
        ind12.name = "Sibling6"
        ind12.id = "I06"
        ind12.birthday = "7 JUN 1950"
        ind13 = Individual()
        ind13.name = "Sibling4"
        ind13.id = "I04"
        ind13.birthday = "7 JUN 1950"
        ind14 = Individual()
        ind14.name = "Sibling5"
        ind14.id = "I05"
        ind14.birthday = "7 JUN 1950"
        ind15 = Individual()
        ind15.name = "Sibling6"
        ind15.id = "I06"
        ind15.birthday = "7 JUN 1950"
        fam1 = Family()
        fam1.children = [ind1.id, ind2.id, ind3.id, ind4.id, ind5.id, ind6.id,ind7.id,ind8.id, ind9.id, ind10.id, ind11.id, ind12.id, ind13.id,ind14.id,ind15.id]
        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind1, ind2, ind3, ind4, ind5, ind6]
        storyChecker.families = [fam1]
        families_returned = storyChecker.fewer_15_siblings()
        self.assertEquals(len(families_returned), 1)
        self.assertIn(fam1, families_returned)
    def test_male_last_names(self):
        ind2 = Individual()
        ind2.name = "Son LastName"
        ind2.id = "I02"
        ind2.gender = "M"
        ind3 = Individual()
        ind3.name = "Son DiffLast"
        ind3.id = "I03"
        ind3.gender = "M"
        fam1 = Family()
        fam1.children = [ind2.id]
        fam1.husband_name = "father LastName"
        fam2 = Family()
        fam2.husband_name = "father LastName"
        fam2.children = [ind3.id]
        storyChecker = UserStoryChecker()
        storyChecker.individuals = [ind2,ind3]
        storyChecker.families = [fam1,fam2]
        families_returned = storyChecker.male_last_names()
        self.assertEquals(len(families_returned), 1)
        self.assertIn(fam2, families_returned)






if __name__ == '__main__':
    unittest.main()

