from datetime import datetime, date
from dateutil.relativedelta import relativedelta

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
        #US17
        self.marriage_to_descend()
        #US18
        
        #US01
        self.dates_before_today()

        self.marriage_to_sibling()

        #US02
        self.birth_before_marriage()
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
    #user story 1, parents should not marry descendants
    def marriage_to_descend(self):
        for f in self.families:
            mother = self.find_by_id(self.individuals,f.wife_id)
            father= self.find_by_id(self.individuals, f.husband_id)
            for child in f.children:
                myChild = self.find_by_id(self.individuals, child)
                childSpouse = self.find_by_id(self.individuals, myChild.spouse)
                if(childSpouse == mother):
                    print("Error US17:  " + mother.name + " (" + mother.id + ") is married to a descendant")
                elif(childSpouse == father):
                    print("Error US17: " + father.name + " (" + father.id + ") is married to a descendant ")
    def marriage_to_sibling(self):
        for f in self.families:
            for child in f.children:
                myChild = self.find_by_id(self.individuals, child)
                childSpouse = self.find_by_id(self.individuals, myChild.spouse)
                ##print(childSpouse)
                for sib in f.children:
                    ##print(sib)
                    if(childSpouse == sib):
                        print("Error US18: " + myChild.name + "is married to a sibling")
                        break
                    
    #User story 1, dates not after current date                
    def dates_before_today(self):
        current_date = date.today()
        for i in self.individuals:
            individual_birthday = self.find_by_id(self.individuals, i.birthday)
            individual_death = self.find_by_id(self.individuals, i.death)
            try:
                if self.compare_dates(individual_birthday, current_date) > 0:
                    print("Error US01: {} birthday is after today; are you a time traveler?".format(i.name))
            except:
                pass
            if individual_death != None:
                try:
                    if self.compare_dates(individual_death, current_date) > 0:
                        print("Error US01: {} date of death is after today; are you a time traveler?".format(i.name))
                except:
                    pass
        #Need to check for existence of dates first before try except        
        for f in self.families:
            divorce_date = self.find_by_id(self.individuals, f.divorced)
            married_date = self.find_by_id(self.individuals, f.married)
            if (divorce_date != None):
                try:
                    if self.compare_dates(divorce_date > current_date) > 0:
                        print("Error US01: {} divorce date is after today; are you a time traveler?".format(f.name))
                except:
                    pass
                
            if (married_date != None):
                try:
                    if self.compare_dates(married_date > current_date) > 0:
                        print("Error US01: {}'s marriage date is after today; are you a time traveler?".format(f.name))
                except:
                    pass

    #User story 2
    def birth_before_marriage(self):
##        #dictionaries for easies
##        indiDict = {}
##        famDict = {}
##        for x in self.individuals:
##            indiDict[x.id] = x
##        for y in self.families:
##            famDict[y.id] = y
##        for i in self.individuals:
##            if i.spouse != 'NA':
##                marr_date = famDict[i.spouse].married
##                bir_date = i.birthday
##                if self.compare_dates(marr_date, bir_date) > 0:
##                    print("Error US02: " + i.name + " married before born.")
        
        for i in self.individuals:
            birthday = i.birthday
            #Need to create new object to hold family class to sort by values
            family = self.find_by_id(self.families, i.spouse)
            if family != None:
                marriage_date = family.married
                if marriage_date != None:
                    try:
                        if compare_dates(birthday, marriage_date) > 0:
                            print("Error US02: {} is married is before they were born.".format(i.name))
                    except:
                        pass

    #User story 25
    #no more than one child with same name and birth date in fam
    #returns list of lists of duplicates
    def unique_first_names(self):
        error = ''
        all_indivs = self.individuals
        #this holds all dupe kids
        error_kids_all = []
        for fam in self.families:
            #this is a temp container for kids in each family
            kid_holder = []
            kids = fam.children
            for kid in kids:
                kid_holder.append(self.find_by_id(all_indivs, kid))
            if len(kid_holder) < 0:
                continue
            for each in kid_holder:
                if error == each.id:
                        continue
                for other in kid_holder:
                    if (each.name == other.name and each.birthday == other.birthday and each.id != other.id):
                        print("Error US25: Child " + other.name + " ("+ other.id+")" +
                              " and Child " + each.name + " ("+ each.id +") have same Name and Birthday.")
                        error_kids = [other.id, each.id]
                        error = other.id
                        error_kids_all.append(error_kids)
                        break
        return error_kids_all


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






