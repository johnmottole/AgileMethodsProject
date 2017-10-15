from datetime import date
from prettytable import PrettyTable
from individual_and_family import *
from userstories import *
from operator import itemgetter, attrgetter

def readFile():
    #open file
    file = open('My-Family-3-Sep-2017-593.ged', 'r')

    partList = []

    #go through file line by line
    for l in file:
        #get rid of unnecessary characters from file
        line = l.strip()

        #break up line into at most 3 sections
        parts = line.split(' ',2)

        #add broken up input line to list of broken up lines
        partList.append(parts)

    return partList


def find_individual_by_id(indiv_list,id):
    for i in indiv_list:
        if i.id == id:
            return i
    return None

#process each line
def create_indiv_objects(part_list):
    #lists of objects to be sent back
    individuals = []
    families = []

    # set constants
    tag_types = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV','DATE', 'HEAD', 'TRLR', 'NOTE']
    tag_exceptions = ['INDI', 'FAM']

    #current object being added to
    current_indiv = None
    current_fam = None

    #go through each broken up line
    for index, parts in enumerate(part_list):
        #if first part of line is a 0, then something new is being created, so append current indiv or fam to appriate list and set current_indiv or current_fam to empty
        if (len(parts) > 0 and parts[0] == '0'):
            if current_indiv != None:
                #RL -- right before 
                individuals.append(current_indiv)
                current_indiv = None
            elif current_fam != None:
                families.append(current_fam)
                current_fam = None

        exeption1 = (len(parts) == 3 and parts[0] == '1' and parts[1] == 'DATE')
        exception2 = (len(parts) == 3 and parts[0] == '2' and parts[1] == 'NAME')
        # create new indiviual or family object if parts[2] is a 'INDI' or 'FAM"
        if len(parts) == 3 and parts[2] in tag_exceptions:
            if (parts[2] == 'INDI'):
                current_indiv = Individual()
                current_indiv.id = parts[1]
            else:
                current_fam = Family()
                current_fam.id = parts[1]
        # if line has none of the exceptions, and is a '1' then its a property of current object
        elif len(parts) == 3 and parts[0] == '1' and exeption1 is False and exception2 is False:
            # if current_indiv is not None, then it is being defined so this line is defining one of its properties
            if current_indiv != None:
                if parts[1] == 'NAME':
                    current_indiv.name = parts[2]
                elif parts[1] == 'SEX':
                    current_indiv.gender = parts[2]
                elif parts[1] == 'FAMC':
                    current_indiv.child = parts[2]
                elif parts[1] == 'FAMS':
                    current_indiv.spouse = parts[2]
                #RL -- death in our file is a Y/N? no dates available
                elif parts[1] == 'DEAT':
                    current_indiv.alive = 'False'
                    current_indiv.death = day_adder(part_list, index)
            # if current_fam is not None, then it is being defined so this line is defining one of its properties
            elif current_fam != None :
                if parts[1] == 'HUSB':
                    current_fam.husband_id = parts[2]
                elif parts[1] == 'WIFE':
                    current_fam.wife_id = parts[2]
                elif parts[1] == 'CHIL':
                    current_fam.children = current_fam.children + [parts[2]]


        #RL --  calling birthday adder and age adder
        if (len(parts) == 2):
            if(parts[1] == 'BIRT'):
                current_indiv.birthday = day_adder(part_list, index)
                #current_indiv.age = age_adder(current_indiv)
            if (parts[1] == 'MARR'):
                current_fam.married = day_adder(part_list,index)
            if (parts[1] == 'DIV'):
                current_fam.divorced = day_adder(part_list,index)
    #calls to US27 and 28
    #doing this here to account for the fact that people shouldn't
    #"age" after they have died
    for indi in individuals:
        indi.age = age_adder(indi)
    for famy in families:
        famy.children = order_sibs(famy, individuals)

    #Return individual list and family list
    return (individuals, families)

#goes through each family and gets names of husband and wives
#RL commenting some of this out to allow errors through for US26
def link_indiv_fam(individuals, familes):
    for f in familes:
        husband = find_individual_by_id(individuals,f.husband_id)
        if (husband != None):
            f.husband_name = husband.name
            #husband.spouse = f.id

        wife = find_individual_by_id(individuals, f.wife_id)
        if (wife != None):
            f.wife_name = wife.name
            #wife.spouse = f.id

##        for child in f.children:
##            child_obj = find_individual_by_id(individuals, child)
##            if (child_obj != None):
##                child_obj.child = f.id

#RL -- adds birthday to the individual
def day_adder(part_list, index):
    return part_list[index + 1][2];

#RL -- calculates age
#US27 -- Include person's current age when listing individuals
def age_adder(indiv):
    birth = indiv.birthday
    months = {'JAN' : 1, 'FEB' : 2, 'MAR' : 3,
              'APR' : 4, 'MAY' : 5, 'JUN' : 6,
              'JUL' : 7, 'AUG' : 8, 'SEP' : 9,
              'OCT' : 10, 'NOV' : 11, 'DEC' : 12 }
    if(indiv.death == "NA"):
        birth_list = birth.split(' ')
        b_date = date(int(birth_list[2]), months[birth_list[1]], int(birth_list[0]) )
        c_date = date.today()
        return str(c_date.year - b_date.year -((c_date.month, c_date.day) < (b_date.month, b_date.day)))
    if(indiv.death != "NA"):
        birth_list = birth.split(' ')
        death_list = indiv.death.split(' ')
        b_date = date(int(birth_list[2]), months[birth_list[1]], int(birth_list[0]))
        c_date = date(int(death_list[2]), months[death_list[1]], int(death_list[0]))
        return str(c_date.year - b_date.year - ((c_date.month, c_date.day) < (b_date.month, b_date.day)))

#US28 -- order siblings by age when listing families
def order_sibs(fam, indivs):
    ret_lst = []
    if (len(fam.children) > 1):
        tmp = []
        for chil in fam.children:
            tmp.append(find_individual_by_id(indivs, chil))
        tmp.sort(key=lambda x: x.age, reverse=True)
        for child in tmp:
            ret_lst.append(child.id)
        print(ret_lst)
        return ret_lst
    else:
        return fam.children


def main():
    #get list of broken up lines from file
    parts = readFile()

    #get list of individual objects and family objects from broken up lines
    results = create_indiv_objects(parts)

    individuals = results[0]
    families = results[1]
    link_indiv_fam(individuals, families)

    #At this point the data has been completed processed
    x = PrettyTable()
    x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    individual_num = len(individuals)
    i = 0
    while (i < individual_num):
        x.add_row([individuals[i].id, individuals[i].name, individuals[i].gender, individuals[i].birthday, individuals[i].age, individuals[i].alive, individuals[i].death, individuals[i].child, individuals[i].spouse])
        i += 1
    print(x)

    y = PrettyTable()
    y.field_names = ["ID", "Married", "Divorced", "Husband Name", "Husband ID", "Wife Name", "Wife ID", "Children"]
    fam_num = len(families)
    k = 0
    while (k < fam_num):
        y.add_row([families[k].id, families[k].married, families[k].divorced, families[k].husband_name, families[k].husband_id, families[k].wife_name, families[k].wife_id, families[k].children])
        k += 1
    print(y)

    
    #Have User story checker perform all checks on data
    checker = UserStoryChecker()
    checker.check_all_stories(individuals,families)
    
if __name__=="__main__":
	main()
