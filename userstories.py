from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class UserStoryChecker:
    individuals = []
    families = []

    # This method is called once by main, call all stories in this method
    def check_all_stories(self, i, f):
        self.individuals = i
        self.families = f
        #US01
        self.dates_before_today()
        #US02
        self.birth_before_marriage()
        #User story 9
        self.birth_before_death_of_parent()
        #User Story 10
        self.marriage_after_14()
        #US17
        self.marriage_to_descend()
        #US18
        self.marriage_to_sibling()
        #US25
        self.unique_first_names()
        #US26
        self.corresp_entries()


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
            marr_day = f.married
            spouses = [wife,husband]
            for spouse in spouses:
                if (spouse != None):
                    bday = spouse.birthday
                    try:
                        num_age = float(spouse.age)
                        if (self.compare_dates(bday,marr_day) < 14*365):
                            print("Anomaly US10:  " + spouse.name + " (" + spouse.id + ") was less than 14 years old at time of marriage")
                    except:
                        pass
    #user story 17, parents should not marry descendants
    def marriage_to_descend(self):
        for f in self.families:
            mother = f.wife_id
            father= f.husband_id
            for child in f.children:
                #RL-- edited because was checking fam tags against indi tags
                #now actually checks for marriage to children
                myChild = self.find_by_id(self.individuals, child)
                if myChild.spouse == 'NA':
                    continue
                their_fam = self.find_by_id(self.families, myChild.spouse)
                if myChild.gender == 'M':
                    childSpouse = their_fam.wife_id
                if myChild.gender == 'F':
                    childSpouse = their_fam.husband_id
                if(childSpouse == mother):
                    mom = self.find_by_id(self.individuals, mother)
                    print("Error US17:  " + mom.name + " (" + mom.id + ") is married to a descendant")
                if(childSpouse == father):
                    dad = self.find_by_id(self.individuals, father)
                    print("Error US17: " + dad.name + " (" + dad.id + ") is married to a descendant ")
                    
    # US18 no marriage to siblings
    def marriage_to_sibling(self):
        for ind in self.individuals:
            if ind.spouse != 'NA':
                if ind.child == 'NA':
                    continue
                the_fam_s = self.find_by_id(self.families, ind.spouse)
                the_fam_c = self.find_by_id(self.families, ind.child)
                if ind.gender == 'M':
                    if the_fam_s.wife_id in the_fam_c.children:
                        print("Error US18: " + ind.name + " " + ind.id + " is married to a sibling.")
                if ind.gender == 'F':
                    if the_fam_s.husband_id in the_fam_c.children:
                        print("Error US18: " + ind.name + " " + ind.id + " is married to a sibling.")
        
##        for f in self.families:
##            for child in f.children:
##                myChild = self.find_by_id(self.individuals, child)
##                childSpouse = self.find_by_id(self.individuals, myChild.spouse)
##                for sib in f.children:
##                    if(childSpouse == sib):
##                        print("Error US18: " + myChild.name + "is married to a sibling")
##                        break
                    
    #User story 1, dates not after current date                
    def dates_before_today(self):
        current_date = date.today().strftime('%d %b %Y')

        for i in self.individuals:
            individual_birthday = i.birthday
            individual_death = i.death
            try:
                if self.compare_dates(current_date, individual_birthday) > 0:
                    print("Error US01: {} birthday is after today; are you a time traveler?".format(i.name))
            except:
                pass
            if (individual_death != None):
                try:
                    if self.compare_dates(current_date, individual_death) > 0:
                        print("Error US01: {} date of death is after today; are you a time traveler?".format(i.name))
                except:
                    pass
        #Need to check for existence of dates first before try except        
        for f in self.families:
            divorce_date = f.divorced
            married_date = f.married
            if (divorce_date != None):
                try:
                    if self.compare_dates(current_date, divorce_date) > 0:
                        print("Error US01: {} and {}'s- divorce date is after today; are you a time traveler?".format(f.husband_name, f.wife_name))
                except:
                    pass
                
            if married_date != None:
                try:
                    if self.compare_dates(current_date, married_date) > 0:
                        print("Error US01: {} and {}'s marriage date is after today; are you a time traveler?".format(f.husband_name, f.wife_name))
                except:
                    pass

    #User story 2
    def birth_before_marriage(self):
        
        for i in self.individuals:
            birthday = i.birthday
            #Need to create new object to hold family class to sort by values
            family = self.find_by_id(self.families, i.spouse)
            if family != None:
                marriage_date = family.married
                if marriage_date != None:
                    try:
                        if self.compare_dates(birthday, marriage_date) < 0:
                            print("Error US02: {} married before they were born.".format(i.name))
                    except:
                        pass

    #User story 25
    #no more than one child with same name and birth date in fam
    #returns list of lists of duplicates
    def unique_first_names(self):
        errors = []
        for fam in self.families:
            if len(fam.children) > 1:
                for index, kiddo in enumerate(fam.children):
                    kid = self.find_by_id(self.individuals, kiddo)
                    for kiddo_comp in fam.children[index:]:
                        kid_comp = self.find_by_id(self.individuals, kiddo_comp)
                        if kid.name == kid_comp.name and kid.birthday == kid_comp.birthday and kid.id != kid_comp.id:
                            print("Error US25: Child " + kid.name + " ("+ kid.id+")" +
                              " and Child " + kid_comp.name + " ("+ kid_comp.id +") have same Name and Birthday.")
                            errors.append([kid.id, kid_comp.id])
        return errors
    
    #US26
    #Keep Individual and Family lists consistent
    #Returns: list of error strings
    def corresp_entries(self):
        errors= []
        #build dicts - faster lookup -> own func later
        indiDict = {}
        famDict = {}
        for x in self.individuals:
            indiDict[x.id] = x
        for y in self.families:
            famDict[y.id] = y
        #check fams for kids and spouses
        for fam in self.families:
            for kid in fam.children:
                #kids
                if indiDict[kid].child != fam.id:
                    errStr = "Anomaly US26: " + indiDict[kid].name + " is missing their family tag."
                    errors.append(errStr);
                    print(errStr)
            #spouses
            if indiDict[fam.husband_id].spouse != fam.id:
                errStr = "Anomaly US26: " + indiDict[fam.husband_id].name + " is missing his spouse tag."
                errors.append(errStr);
                print(errStr)
            if indiDict[fam.wife_id].spouse != fam.id:
                errStr = "Anomaly US26: " + indiDict[fam.wife_id].name + " is missing her spouse tag."
                errors.append(errStr);
                print(errStr)
        #check indi for inclusion in their family's data
        for indi in self.individuals:
            #spouse
            if indi.spouse != 'NA':
                if (indi.id != famDict[indi.spouse].husband_id and indi.id != famDict[indi.spouse].wife_id):
                    errStr = "Anomaly US26: " + indi.name + " is missing from their family's spouse data."
                    errors.append(errStr);
                    print(errStr)
            #child
            if indi.child != 'NA':
                if indi.id not in famDict[indi.child].children:
                    errStr = "Anomaly US26: " + indi.name + " is missing from their family's children data."
                    errors.append(errStr);
                    print(errStr)  
        return errors






