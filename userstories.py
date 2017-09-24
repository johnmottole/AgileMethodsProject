from datetime import datetime
from dateutil.relativedelta import relativedelta
import unittest

class UserStoryChecker:
    individuals = []
    families = []

    # This method is called once by main, call all stories in this method
    def check_all_stories(self, i, f):
        self.individuals = i
        self.families = f
        #User story 9
        self.birth_before_death_of_parent()
        #User Story 10
        self.marriage_after_14()
        self.marriage_to_descend()

    #can be used by family and individual because both have id property
    def find_by_id(self, object_list, id):
        for i in object_list:
            if i.id == id:
                return i
        return None

    #subtracts time between date2 and date1 (date2 - date1)
    def compare_dates(self, date1, date2):
        d1 = datetime.strptime(date1, '%d %b %Y')
        d2 = datetime.strptime(date2, '%d %b %Y')
        return (d2 - d1).days

    # User story 09, Birth before death of parents
    def birth_before_death_of_parent(self):
        for individual in self.individuals:
            bday = individual.birthday
            family = self.find_by_id(self.families,individual.child)
            if family != None:
                mother_id = family.wife_id
                father_id = family.husband_id
                mother = self.find_by_id(self.individuals,mother_id)
                father = self.find_by_id(self.individuals, father_id)
                mother_death = mother.death
                father_death = father.death
                if (mother_death != "NA"):
                    time_between = self.compare_dates(bday,mother_death)
                    if (time_between < 0):
                        print("Error US09: " + individual.name + " (" + individual.id + ") was born after the death of mother " + mother.name + " (" + mother.id + ")")
                if (father_death != "NA"):
                    b_day_obj = datetime.strptime(bday, '%d %b %Y')
                    dad_date = b_day_obj - relativedelta(months=9)
                    d2 = datetime.strptime(father_death, '%d %b %Y')
                    time_between = (d2-dad_date).days
                    if (time_between < 0):
                        print("Error US09: " + father.name + " (" + father.id + ") died at least 9 months before " + individual.name + " (" + individual.id + ") was born")


    #User story 10, marraige before 14
    def marriage_after_14(self):
        for f in self.families:
            wife = self.find_by_id(self.individuals,f.wife_id)
            husband = self.find_by_id(self.individuals, f.husband_id)
            spouses = [wife,husband]
            for spouse in spouses:
                if (spouse != None):
                    age = spouse.age
                    try:
                        num_age = float(age)
                        if (num_age < 14):
                            print("Anomaly US10:  " + spouse.name + " (" + spouse.id + ") is married but is less than 14 years old")
                    except:
                        pass
    
    def marriage_to_descend(self):
        for f in self.families:
            mother = self.find_by_id(self.individuals,f.wife_id)
            father= self.find_by_id(self.individuals, f.husband_id)
            ##print(mother)
            for child in f.children:
                myChild = self.find_by_id(self.individuals, child)
                childSpouse = self.find_by_id(self.individuals, myChild.spouse)
                if(childSpouse == mother):
                    print("Error US17:  " + mother.name + " (" + mother.id + ") is married to a descendant")
                    return True
                elif(childSpouse == father):
                    print("Error US17: " + father.name + " (" + father.id + ") is married to a descendant ")
                    return True
        return False













