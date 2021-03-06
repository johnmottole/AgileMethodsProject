from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable
from operator import itemgetter, attrgetter

class UserStoryChecker:
    individuals = []
    families = []

    # This method is called once by main, call all stories in this method
    def check_all_stories(self, i, f):
        self.individuals = i
        self.families = f

        # US29 these are out of order bc they print tables
        self.list_dead()
        #US30
        self.list_living_married()
        #US31
        self.list_living_single()
        #US32
        self.list_multiple_births()
        #US01
        self.dates_before_today()
        #US02
        self.birth_before_marriage()
        #US03
        self.birth_before_death()
        #US04
        self.marriage_before_divorce()
        #US05
        self.marriage_before_death()
        #US06
        self.divorce_before_death()
        #US07
        self.younger_than_150()
        #US08
        self.birth_before_parents()
        #User story 9
        self.birth_before_death_of_parent()
        #User Story 10
        self.marriage_after_14()
        #User Story 11
        self.no_bigamy()
        #User Story 12
        self.parents_to_old()
        #User story 13
        self.sibling_spacing()
        # User story 14
        self.multuple_births()
        #User story 15
        self.fewer_15_siblings()
        #user story 16
        self.male_last_names()
        #US17
        self.marriage_to_descend()
        #US18
        self.marriage_to_sibling()
        #US25
        self.unique_first_names()
        #US26
        self.corresp_entries()
        #US19
        self.first_cousins()
        #US20
        self.aunts_uncles()
        #US27 and US28 defined in main.py, because they must
        #run whenever individuals and families are put together
        #US21
        self.gender_roles()
        #US22
        self.unique_ids_fam()
        self.unique_ids_ind()
        #US23
        self.unique_names_gedcom()
        #24
        self.unique_spouses()
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

    def compare_years(self, date1, date2):
        d1 = datetime.strptime(date1, '%d %b %Y')
        d2 = datetime.strptime(date2, '%d %b %Y')
        return (d2-d1).days/365.2425

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
                #print(child_bday)
                diff_mother = self.compare_dates(wife_bday, child_bday) / 365
                diff_father = self.compare_dates(husband_bday, child_bday) / 365
                if (diff_mother > 60):
                    print("Error US12: " + child.name + "(" + child.id + ") is more than 60 years younger than mother")
                    error_messages += ["Error US12: " + child.name + "(" + child.id + ") is more than 60 years younger than mother"]
                if (diff_father > 80):
                    print("Error US12: " + child.name + "(" + child.id + ") is more than 80 years younger than father")
                    error_messages += ["Error US12: " + child.name + "(" + child.id + ") is more than 80 years younger than father"]
        return error_messages

    #User story 13
    def sibling_spacing(self):
        matches = []
        for f in self.families:
            children_objs = []
            children_ids = f.children
            for id in children_ids:
                children_objs += [self.find_by_id(self.individuals,id)]
            for child in children_objs:
                for sibling in children_objs:
                    if child.id != sibling.id:
                        diff = self.compare_dates(child.birthday,sibling.birthday)
                        if diff < 30*8 and diff > 2:
                            matches += [[child,sibling]]
        for m in matches:
            print("Error US13: Siblings " + m[0].name + " (" + m[0].id + ") and " + m[1].name + " (" + m[1].id + ") are not spaced correctly")
        return matches

    #User story 14
    def multuple_births(self):
        error_families = []
        for f in self.families:
            children_objs = []
            children_ids = f.children
            for id in children_ids:
                children_objs += [self.find_by_id(self.individuals, id)]
            birth_dict = {}
            for child in children_objs:
                if child.birthday in birth_dict.keys():
                    birth_dict[child.birthday] += [child.id]
                else:
                    birth_dict[child.birthday] = [child.id]

            for key in birth_dict.keys():
                if len(birth_dict[key]) > 5:
                    print("Anomaly US14: Too many children born to family " + f.id + " on " + key + " (" + str(birth_dict[key]) +")")
                    error_families += [f]
        return error_families


    #user story 15, there should be less than 15 sblings
    def fewer_15_siblings(self):
        problem_families = []
        for f in self.families:
            if len(f.children) >= 15:
                print("Anomaly US15: There is 15 or more siblings in family " + f.id)
                problem_families += [f]
        return problem_families

    #user story 16, male last names
    def male_last_names(self):
        problem_families = []
        for f in self.families:
            split_husband_name = f.husband_name.split()
            if len(split_husband_name) > 1:
                family_name = split_husband_name[1]
                for child_id in f.children:
                    child = self.find_by_id(self.individuals,child_id)
                    if child.gender == 'M':
                        split_child_name = child.name.split()
                        if len(split_child_name) > 1:
                            if split_child_name[1] != family_name:
                                print("Anomaly US16: Male family names don't match in family " + f.id)
                                problem_families += [f]
                                break
        return problem_families


    #user story 17, parents should not marry descendants
    def marriage_to_descend(self):
        for i in self.individuals:
                for f in self.families:
                    if(i.id in f.children):
                        #print("ID IS " + i.id)
                        father = f.husband_id
                        mother = f.wife_id
                        for myFam in self.families:
                            if(i.id == myFam.husband_id):
                                if(mother == myFam.wife_id):
                                    print("Error US17:  "  + mother + " is married to a descendant")
                                    return mother
                            if(i.id == myFam.wife_id):
                                if(father == myFam.husband_id):
                                    print("Error US17:  "  + father + " is married to a descendant")
                                    return father

                    
    # US18 no marriage to siblings
    def marriage_to_sibling(self):
        for ind in self.individuals:
            if ind.spouse != 'NA':
                if ind.child == 'NA':
                    continue
                the_fam_s = self.find_by_id(self.families, ind.spouse)
                the_fam_c = self.find_by_id(self.families, ind.child)
                if(the_fam_c):
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
        error_list =[]

        for i in self.individuals:
            individual_birthday = i.birthday
            individual_death = i.death
            try:
                if self.compare_dates(current_date, individual_birthday) > 0:
                    print("Error US01: {} birthday is after today; are you a time traveler?".format(i.name))
                    error_list.append(i.birthday)
            except:
                pass
            if (individual_death != None):
                try:
                    if self.compare_dates(current_date, individual_death) > 0:
                        print("Error US01: {} date of death is after today; are you a time traveler?".format(i.name))
                        error_list.append(i.death)
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
                        error_list.append(f.divorced)
                except:
                    pass
                
            if married_date != None:
                try:
                    if self.compare_dates(current_date, married_date) > 0:
                        print("Error US01: {} and {}'s marriage date is after today; are you a time traveler?".format(f.husband_name, f.wife_name))
                        error_list.append(f.married)
                except:
                    pass
        return error_list
    #User story 2
    def birth_before_marriage(self):
        error_list = []
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
                            error_list.append(i.name)
                    except:
                        pass
        return error_list
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

    #User story 5
    def marriage_before_death(self):
        error_list = []
        for i in self.individuals:
            death = i.death
            family = self.find_by_id(self.families, i.spouse)
            if death != None and family != None:  
                marriage = family.married
                if marriage != None:
                    try:
                        if self.compare_dates(death, marriage) > 0:
                            print ("Error US05: {} married after they died.".format(i.name))
                            error_list.append(i.name)
                    except:
                        pass
        return error_list

    #User story 6
    def divorce_before_death(self):
        error_list = []
        for i in self.individuals:
            death = i.death
            family = self.find_by_id(self.families, i.spouse)
            if death != None and family != None:  
                divorce = family.divorced
                if divorce != None:
                    try:
                        if self.compare_dates(death, divorce) > 0:
                            print ("Error US06: {} divorced after they died.".format(i.name))
                            error_list.append(i.name)
                    except:
                        pass
        return error_list

    #User story 7
    def younger_than_150(self):
        current_date = date.today().strftime('%d %b %Y')
        errors = {}
        for i in self.individuals:
            name = i.name
            birthday = i.birthday
            if self.compare_years(birthday, current_date) >= 150:
                print("Anomaly US07: {} is older than 150 years old.".format(name))
                errors.update({'{}'.format(name): birthday})
        return errors

    # User story 8                
    def birth_before_parents(self):
        errors = {}
        for individual in self.individuals:
            name = individual.name
            bday = individual.birthday
            family = self.find_by_id(self.families,individual.child)
            if family != None:
                mother_id = family.wife_id
                father_id = family.husband_id
                mother = self.find_by_id(self.individuals,mother_id)
                father = self.find_by_id(self.individuals, father_id)
                mother_name = mother.name
                father_name = father.name
                mother_birthday = mother.birthday
                father_birthday = father.birthday
                if self.compare_dates(bday, mother_birthday) > 0 and self.compare_dates(bday, father_birthday) > 0 :
                    print("Error US08: {} is older than their mother {} and father {}.".format(name, mother_name, father_name))
                    errors.update({name: [mother_name, father_name]})
                elif self.compare_dates(bday, mother_birthday) > 0 and self.compare_dates(bday, father_birthday) < 0:
                    print("Error US08: {} is older than their mother {}.".format(name, mother_name))
                    errors.update({name: mother_name})
                elif self.compare_dates(bday, mother_birthday) < 0 and self.compare_dates(bday, father_birthday) > 0:
                    print("Error US08: {} is older than their father {}.".format(name, father_name))
                    errors.update({name: father_name})
        return errors
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
    #US23 unique names in entire GEDCOM
    def unique_names_gedcom(self):
        match_arr = 0
        not_unique = False
        repeat_indivs = []
        for indiv in self.individuals:
            myIndName = indiv.name
            for other_indiv in self.individuals:
                if(myIndName == other_indiv.name):
                    match_arr = match_arr + 1
                if(match_arr > 1):
                    not_unique = True
                    repeat_indivs.append(myIndName)
            match_arr = 0
        if(not_unique):
            repeat_indivs = set(repeat_indivs)
            for i in repeat_indivs:
                print("ERROR US23 " + i + " is not a unique name")
            not_unique = False
        return repeat_indivs

    #US24
    def unique_spouses(self):
        match_arr = 0
        not_unique = False
        repeat_fams = []
        for family in self.families:
            myHusb = family.husband_id
            myWife = family.wife_id
            marriageDate = family.married
            for other_fam in self. families:
                otherHusb = other_fam.husband_id
                otherWife = other_fam.wife_id
                otherMarriageDate = other_fam.married
                if(myHusb == otherHusb or myWife == otherWife and marriageDate == otherMarriageDate):
                    match_arr = match_arr + 1
                if(match_arr > 1):
                    not_unique = True
                    repeat_fams.append(family.id)
            match_arr = 0
        if(not_unique):
            repeat_fams = set(repeat_fams)
            for i in repeat_fams:
                print("ERROR US24 " + i + " is not a unique family by spouse")
        return repeat_fams
    
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

    #US29 list all deceased in GEDCOM
    def list_dead(self):
        ret = []
        for ind in self.individuals:
            if ind.death != "NA":
                ret.append(ind)
        tbl = PrettyTable()
        tbl.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        num_records = len(ret)
        ind = 0
        while (ind < num_records):
            tbl.add_row([ret[ind].id, ret[ind].name, ret[ind].gender, ret[ind].birthday, ret[ind].age, ret[ind].alive, ret[ind].death, ret[ind].child, ret[ind].spouse])
            ind+=1
        print("These are the deceased members of this family: ")
        print(tbl)
        return ret

    #US30 list all living married members
    def list_living_married(self):
        ret = []
        for ind in self.individuals:
            if ind.death == "NA" and ind.spouse != "NA":
                ret.append(ind)
        tbl = PrettyTable()
        tbl.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        num_records = len(ret)
        ind = 0
        while (ind < num_records):
            tbl.add_row([ret[ind].id, ret[ind].name, ret[ind].gender, ret[ind].birthday, ret[ind].age, ret[ind].alive, ret[ind].death, ret[ind].child, ret[ind].spouse])
            ind += 1
        print("These are the living, married members of this family: ")
        print(tbl)
        return ret
    #US31 list all living single members of the family
    def list_living_single(self):
        ret = []
        for ind in self.individuals:
            if ind.spouse == "NA" and ind.death == "NA":
                ret.append(ind);
            tbl = PrettyTable()
            tbl.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        num_records = len(ret)
        ind = 0
        while (ind < num_records):
            tbl.add_row([ret[ind].id, ret[ind].name, ret[ind].gender, ret[ind].birthday, ret[ind].age, ret[ind].alive, ret[ind].death, ret[ind].child, ret[ind].spouse])
            ind += 1
        print("These are the living, single members of this family: ")
        print(tbl)
        return ret

    #US32 list all multiple births in a gedcom file
    def list_multiple_births(self):
        indis = self.individuals
        temp = []
        ret = []
        for fam in self.families:
            if len(fam.children) > 1:
                #first_kid = self.find_by_id(indis, fam.children[0])
                same_dates = []
                for kid1 in fam.children:
                    temp = []
                    kidone = self.find_by_id(indis, kid1)
                    for kid2 in fam.children:
                        kidtwo = self.find_by_id(indis, kid2)
                        if kidone.birthday == kidtwo.birthday and kidone.birthday not in same_dates and kidone.id != kidtwo.id:
                            if kidone.id not in temp:
                                temp.append(kidone.id)
                            if kidtwo.id not in temp:
                                temp.append(kidtwo.id)
                    if len(temp) > 1:
                        same_dates.append(kidone.birthday)
                        ret.append(temp)
        print("These are all of the multiple births")
        for mult in ret:
            print(mult)
        return ret

    #US21, husband should be male, wife should be female
    def gender_roles(self):
        for fam in self.families:
            husband = self.find_by_id(self.individuals, fam.husband_id)
            wife = self.find_by_id(self.individuals, fam.wife_id)
            if(husband.gender != "M"):
                print("ERROR US21 " + husband.name + " is a female husband")
            if(wife.gender != "F"):
                print("ERROR US21 " + wife.name + " is a male wife")
    #US22, All IDS individual or family should be unique
    def unique_ids_fam(self):
        match_arr = 0
        not_unique = False
        repeat_fams = []
       
        for fam in self.families:
            myID = fam.id
            ##print(myID)
            for other_fam in self.families:
                if(myID == other_fam.id):
                    match_arr = match_arr + 1
            if(match_arr > 1):
                not_unique = True
                repeat_fams.append(myID)
            match_arr = 0
        if(not_unique):
            repeat_fams = set(repeat_fams)
            for f in repeat_fams:
                print("ERROR US22 " + f + " is not unique family")
            not_unique = False
        return repeat_fams

    def unique_ids_ind(self):
        match_arr = 0
        not_unique = False
        repeat_indivs = []
        for indiv in self.individuals:
            myIndID = indiv.id
            for other_indiv in self.individuals:
                if(myIndID == other_indiv.id):
                    match_arr = match_arr + 1
                if(match_arr > 1):
                    not_unique = True
                    repeat_indivs.append(myIndID)
            match_arr = 0
        if(not_unique):
            repeat_indivs = set(repeat_indivs)
            for i in repeat_indivs:
                print("ERROR US22 " + i + " is not a unique individual ID")
            not_unique = False
        return repeat_indivs


   

        



