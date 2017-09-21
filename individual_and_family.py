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
    child = "NA"
    spouse = "NA"

    #to string (used for testing)
    def to_string(self):
        res =  "id: " + self.id + " name: " + self.name + " gender: " + self.gender + " birthday: " + self.birthday + " age: " + self.age + " alive: " + self.alive + " death: " + self.death + " spouse: " + self.spouse + " child: " + ",".join(self.child)
        return res
