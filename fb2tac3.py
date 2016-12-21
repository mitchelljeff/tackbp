


tac2tac={   "org:top_member_employees":"org:top_members_employees",
            "org:members_of":"org:member_of",
            "per:country_of_residence":"per:countries_of_residence",
            "per:city_of_residence":"per:cities_of_residence",
            "org:subsidaries":"org:subsidiaries",
            "per:stateorprovince_of_residence":"per:statesorprovinces_of_residence"}

reverse={   "per:employee_or_member_of":"org:employees_or_members",
            "per:cities_of_residence":"gpe:residents_of_city",
            "org:city_of_headquarters":"gpe:headquarters_in_city",
            "per:city_of_birth":"gpe:births_in_city",
            "per:city_of_death":"gpe:deaths_in_city",
            "org:founded_by":"per:organizations_founded",
            "org:top_members_employees":"per:top_member_employee_of",
            "per:countries_of_residence":"gpe:residents_of_country"}

rlist=[]

with open("fb2tac.txt") as f:
    for line in f:
        fields=line.rstrip("\n").split(",")
        tacrel=fields[0]
        fbrel=fields[1]
        ent1=fields[2]
        ent2=fields[3]
        ent2=ent2[0:len(ent2)-1]
        tacrel2=tac2tac.get(tacrel,tacrel)
        print(tacrel2,fbrel,ent1,ent2,sep=",")
        if tacrel2 in reverse:
            tacrel3=reverse[tacrel2]
            print(tacrel3,fbrel,ent2,ent1+".",sep=",")




