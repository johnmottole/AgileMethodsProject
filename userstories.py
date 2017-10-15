from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from operator import itemgetter, attrgetter

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
        #US03
        self.birth_before_death()
        #US04
        self.marriage_before_divorce()
        #User story 9
        self.birth_before_death_of_parent()
        #User Story 10
        self.marriage_after_14()
        #User Story 11
        self.no_bigamy()
        #User Story 12
        self.parents_to_old()
        #US17
        self.marriage_to_descend()
        #US18
        self.marriage_to_sibling()
        #US25
        self.unique_first_names()
        #US26
        self.corresp_entries()
        #US19
        ##self.first_cousins()
        #US20
        self.aunts_uncles()
        #US27 and US28 defined in main.py, because they must
        #run whenever individuals and families are put together
        print("US27 and US28 can be seen in individual and family summaries.")


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
    #User Story 11
    def no_bigamy(self):
        indiv_with_bigamy = []
        for indiv in self.individuals:
            current_spouses = []
            indiv_id = indiv.id
            for f in self.families:
                if f.wife_id == indiv_id and self.marr_ended(f) == False:
                    current_spouses += [f.husband_name + " (" + f.husband_id + ")"]
                elif f.husband_id == indiv_id and self.marr_ended(f):
                    current_spouses += [f.wife_name + " (" + f.wife_id + ")"]
            if len(current_spouses) > 1:
                spouses = ""
                for i in range(0,len(current_spouses)):
                    if i == len(current_spouses)-1:
                        spouses += " and " + current_spouses[i]
                    else:
                        spouses += current_spouses[i] + ","
                print("Anomaly US11: " + indiv.name + "(" + indiv_id + ") is married to " + spouses)
                indiv_with_bigamy += [indiv.id]
        return indiv_with_bigamy

    #helper method for US11
    def marr_ended(self,fam):
        if fam.divorced != "NA":
            return True
        husband = self.find_by_id(self.individuals, fam.husband_id)
        wife = self.find_by_id(self.individuals, fam.wife_id)
        if wife.alive == 'False' or husband.alive == 'False':
            return True
        return False

    #User Story 12
    def parents_to_old(self):
        error_messages = []
        for f in self.families:
            wife = self.find_by_id(self.individuals, f.wife_id)
            husband = self.find_by_id(self.individuals, f.husband_id)
            wife_bday = wife.birthday
            husband_bday = husband.birthday
            for child in f.children:
                child = self.find_by_id(self.individuals,child)
                child_bday = child.birthday
                print(child_bday)
                diff_mother = self.compare_dates(wife_bday, child_bday) / 365
                diff_father = self.compare_dates(husband_bday, child_bday) / 365
                if (diff_mother > 60):
                    print("Error US12: " + child.name + "(" + child.id + ") is more than 60 years younger than mother")
                    error_messages += ["Error US12: " + child.name + "(" + child.id + ") is more than 60 years younger than mother"]
                if (diff_father > 80):
                    print("Error US12: " + child.name + "(" + child.id + ") is more than 80 years younger than father")
                    error_messages += ["Error US12: " + child.name + "(" + child.id + ") is more than 80 years younger than father"]
        return error_messages


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
    
    #US19 First Cousins should not marry
    def first_cousins(self):
        for ind in self.individuals:
            if ind.spouse != 'NA':
                continue
            cousins_list = self.get_relatives(ind, "cousin")
            if(not cousins_list):
                continue
            ##print("COUSINS ARE: ")
            ##print(cousins_list)
            for f in self.families:
                husb = f.husband_id
                wife = f.wife_id
                if(ind.gender == 'M'):
                    if(ind.id == husb):
                        for person in cousins_list:
                            if(wife == person):
                                print("Error US19: " + ind.name + " " + ind.id + " is married to a first cousin")
                                return True 
                if(ind.gender == 'F'):
                    if(ind.id == wife):
                        for person in cousins_list:
                            if(husb == person):
                                print("Error US19: " + ind.name + " " + ind.id + " is married to a first cousin")
                                return True
                    

    def aunts_uncles(self):
        for ind in self.individuals:
            if(ind.spouse != 'NA'):
                continue
            aunts_and_uncles = self.get_relatives(ind, "aunt")
            if(not aunts_and_uncles):
                continue
            ##print("AUNTS AND UNCLES ARE: ")
            ##print(aunts_and_uncles)
            for f in self.families:
                husb = f.husband_id
                wife = f.wife_id
                if(ind.gender == 'M'):
                    if(ind.id == husb):
                        for person in aunts_and_uncles:
                            if(wife == person):
                                print("Error US20: " + ind.name + " " + ind.id + " is married to a niece")
                                return True
                if(ind.gender == 'F'):
                    if(ind.id == wife):
                        for person in aunts_and_uncles:
                            if(husb == person):
                                print("Error US20: " + ind.name + " " + ind.id + " is married to a nephew")
                                return True

    ##gets different levels of relatives
    ##pass parameter "cousin" to get first cousins
    ##otherwise get aunts and uncles
    def get_relatives(self, ind, level):
        #print(" ID IS : " + ind.id)
        mom = ""
        dad = ""
        ##aunts_uncles = []
        cousins_list = []
        mom_sibs = []
        dad_sibs = []
        ##mom_cousins = []
        ##dad_cousins = []
        for f in self.families:
            for c in f.children:
                if(c == ind.id):
                    mom = f.wife_id
                    dad = f.husband_id
        for f in self.families:
            for c in f.children:
                if(c == mom):
                    mom_sibs = f.children
                    mom_sibs.remove(c)
        for f in self.families:
            for c in f.children:
                if(c == dad):
                    dad_sibs = f.children
                    dad_sibs.remove(c)
        if(level == "cousin"):
            for f in self.families:
                for person in dad_sibs:
                    if(f.husband_id == person or f.wife_id == person):
                        cousins_list = cousins_list + f.children
            for f in self.families:
                for person in mom_sibs:
                    if(f.husband_id == person or f.wife_id == person):
                        cousins_list = cousins_list + f.children
        else:
            ##print("MOM SIBS: " + str(mom_sibs))
            ##print("DAD SIBS: " + str(dad_sibs))
            if(mom_sibs):
                cousins_list = cousins_list + mom_sibs
            if(dad_sibs):
                cousins_list = cousins_list + dad_sibs
        ##print("IND IS: " + ind.id)
        ##print("IND SPOUSE IS: " + ind.spouse)
        #print(cousins_list)

        return cousins_list
            
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

    #User story 3
    def birth_before_death(self):
        for i in self.individuals:
            birthday = i.birthday
            death = i.death
            if death != None:
                try:
                    if self.compare_dates(death, birthday) > 0:
                        print("Error US03: {} died before they were born.".format(i.name))
                except:
                    pass
    #User story 4
    def marriage_before_divorce(self):
        for f in self.families:
            marriage = f.married
            divorced = f.divorced
            if divorced != None and marriage != None:
                try:
                    if self.compare_dates(divorced, marriage) > 0:
                        print ("Error US04: {} and {} divorced before they were married.".format(f.husband_name, f.wife_name))
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

    #US27
    def age_adder(self, indiv):
        birth = indiv.birthday
        months = {'JAN': 1, 'FEB': 2, 'MAR': 3,
                  'APR': 4, 'MAY': 5, 'JUN': 6,
                  'JUL': 7, 'AUG': 8, 'SEP': 9,
                  'OCT': 10, 'NOV': 11, 'DEC': 12}
        if (indiv.death == "NA"):
            birth_list = birth.split(' ')
            b_date = date(int(birth_list[2]), months[birth_list[1]], int(birth_list[0]))
            c_date = date.today()
            return str(c_date.year - b_date.year - ((c_date.month, c_date.day) < (b_date.month, b_date.day)))
        if (indiv.death != "NA"):
            birth_list = birth.split(' ')
            death_list = indiv.death.split(' ')
            b_date = date(int(birth_list[2]), months[birth_list[1]], int(birth_list[0]))
            c_date = date(int(death_list[2]), months[death_list[1]], int(death_list[0]))
            return str(c_date.year - b_date.year - ((c_date.month, c_date.day) < (b_date.month, b_date.day)))
    #US28
    # US28 -- order siblings by age when listing families
    def order_sibs(self, fam, indivs):
        ret_lst = []
        if (len(fam.children) > 1):
            tmp = []
            for chil in fam.children:
                tmp.append(self.find_by_id(indivs, chil))
            tmp.sort(key=lambda x: x.age, reverse=True)
            for child in tmp:
                ret_lst.append(child.id)
            #print(ret_lst)
            return ret_lst
        else:
            return fam.children


   

        



