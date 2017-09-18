from pprint import pprint
from datetime import date

#Defines family object
class Family:
    id = "NA"
    married = "NA"
    divorced = "NA"
    husband_id = "NA"
    husband_name = "NA"
    wife_id = "NA"
    wife_name = "NA"
    children = []
    #to string (used for testing)
    def to_string(self):
        return "id: " + self.id + " married: " + self.married + " divorced: " + self.divorced + " hus_id: " + self.husband_id + " hus_name: " + self.husband_name + " wife_id: " + self.wife_id + " wife_name: " + self.wife_name + " children: " + ','.join(self.children)
#Defines individual object
class Individual:
    id = "NA"
    name = "NA"
    gender = "NA"
    birthday = "NA"
    age = "NA"
    alive = 'True'
    death = "NA"
    child = []
    spouse = "NA"

    #to string (used for testing)
    def to_string(self):
        res =  "id: " + self.id + " name: " + self.name + " gender: " + self.gender + " birthday: " + self.birthday + " age: " + self.age + " alive: " + self.alive + " death: " + self.death + " spouse: " + self.spouse + " child: " + ",".join(self.child)
        return res

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


def find_indivual_by_id(indiv_list,id):
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

        # create new indiviual or family object if parts[2] is a 'INDI' or 'FAM"
        if len(parts) == 3 and parts[2] in tag_exceptions:
            if (parts[2] == 'INDI'):
                current_indiv = Individual()
                current_indiv.id = parts[1]
            else:
                current_fam = Family()
                current_fam.id = parts[1]
        #Ignoring these
        elif len(parts) == 3 and parts[0] == '1' and parts[1] == 'DATE':
            print("cant process")
        elif len(parts) == 3 and parts[0] == '2' and parts[1] == 'NAME':
            print("cant process")
        # if line has none of the exceptions, and is a '1' then its a property of current object
        elif len(parts) == 3 and parts[0] == '1':
            # if current_indiv is not None, then it is being defined so this line is defining one of its properties
            if current_indiv != None:
                if parts[1] == 'NAME':
                    current_indiv.name = parts[2]
                elif parts[1] == 'SEX':
                    current_indiv.gender = parts[2]
                elif parts[1] == 'CHIL':
                    current_indiv.child += parts[2]
                #RL -- death in our file is a Y/N? no dates available
                elif parts[1] == 'DEAT':
                    current_indiv.death = 'Y'
                    current_indiv.alive = 'False'
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
                current_indiv.birthday = birthday_adder(part_list, index)
                current_indiv.age = age_adder(current_indiv.birthday)
        
        

    #Return individual list and family list
    return (individuals, families)

#goes through each family and gets names of husband and wives
def link_indiv_fam(individuals, familes):
    for f in familes:
        husband = find_indivual_by_id(individuals,f.husband_id)
        if (husband != None):
            f.husband_name = husband.name
            husband.child = f.children
            husband.spouse = f.wife_id

        wife = find_indivual_by_id(individuals, f.wife_id)
        if (wife != None):
            wife.child = f.children
            f.wife_name = wife.name
            wife.spouse = f.husband_id

#RL -- adds birthday to the individual
def birthday_adder(part_list, index):
    return part_list[index + 1][2];

#RL -- calculates age 
def age_adder(birth):
    months = {'JAN' : 1, 'FEB' : 2, 'MAR' : 3,
              'APR' : 4, 'MAY' : 5, 'JUN' : 6,
              'JUL' : 7, 'AUG' : 8, 'SEP' : 9,
              'OCT' : 10, 'NOV' : 11, 'DEC' : 12 }
    birth_list = birth.split(' ');
    b_date = date(int(birth_list[2]), months[birth_list[1]], int(birth_list[0]) )
    c_date = date.today()
    return str(c_date.year - b_date.year -((c_date.month, c_date.day) < (b_date.month, b_date.day)))



def main():
    #get list of broken up lines from file
    parts = readFile()

    #get list of individual objects and family objects from broken up lines
    results = create_indiv_objects(parts)

    individuals = results[0]

    #go through fam list and print each fam
    families = results[1]
    link_indiv_fam(individuals, families)



    print("INDIVIDUALS: ")
    for i in individuals:
        print(i.to_string())

    print("FAMILIES: ")
    for f in families:
       print(f.to_string())

if __name__=="__main__":
	main()
