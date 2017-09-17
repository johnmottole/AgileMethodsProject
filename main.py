#open file
file = open('My-Family-3-Sep-2017-593.ged', 'r')
#set constants
tag_types = ['INDI','NAME', 'SEX', 'BIRT','DEAT','FAMC','FAMS','FAM','MARR', 'HUSB', 'WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE']
tag_exceptions=['INDI','FAM']

#go through file line by line
for l in file:
    #get rid of unnecessary characters from file
    line = l.replace("\n", "")
    line = line.replace("\r","")

    #print the input
    print '--> ' + line

    #break up line into at most 3 sections
    parts = line.split(' ',2)

    #get output
    #start of with <-- symbol, then check for exception such as INDI and FAM tag or the 1 DATE and 2 NAME Exception
    #if 1 DATE or 2 NAME found then set valid with N
    output = "<-- "
    if len(parts) == 3 and parts[2] in tag_exceptions:
        output = '<-- ' + parts[0] + '|' + parts[2] + '|Y|' + parts[1]
    elif len(parts) == 3 and parts[0] == '1' and parts[1] == 'DATE':
        output = '<-- 1|DATE|N|' + parts[2]
    elif len(parts) == 3 and parts[0] == '2' and parts[1] == 'NAME':
        output = '<-- 2|NAME|N|' + parts[2]
    #if line has none of the exceptions, process normally
    else:
        #go through each section of the line and add it to input, with a | symbol between each
        for index, item in enumerate(parts):
            #if item is not the first on the line, start it with a |
            if index != 0:
                output +='|'

            #add item to output string
            output += item

            #check to see if the tag type is valid and add to output string
            if index == 1:
                if item in tag_types:
                    output += "|Y"
                else:
                    output += "|N"
    #print the output of the current line
    print output