import re

def sqltoqbepython(params, cond):
    txt = params
    condition = cond

    Query = "SELECT "
    tablematched =[]
    Entities= re.split(",", txt)
    #print(Entities)


    ### code to handle UNQ. keyword
    for i in Entities:
        if(re.search(".UNQ", i)):
            Query = Query + "DISTINCT "
   
    ###loop for table matching with print
    for i in Entities:
        x=re.search("_[0-9]=P.",i)
        #print(x)
        if(re.search("_[0-9]=P.",i)):
            #print(i)
            tablematched.append(re.split("=",i)[0])
            #print(tablematched)
    ###take all the columns in tablematched
    if(tablematched):
        for i in tablematched:
            for j in Entities:
                #print(re.search(i+"\.",j))
                if(re.search(i+"\.",j)):
                    Query = Query + re.split("=",j)[0]+","
                    #Entities.remove(re.split("=",j)[0]+",")
    #print(Query)
    #print(Entities)
    #print(Entities_Copy)
    ###take columns other than tablematched
    for i in Entities:
        if re.search("=P.",i) and not (re.search("_[0-9]=P.", i)):
            #print(re.search("=P.",i))
            Query = Query + re.split("=",i)[0]+","
            #print(Query)
    ### Remove last comma in query
    Query = Query[:-1]
    #print(Query)
    ### Get table names
    Query = Query + " FROM "
    for i in Entities:
        if(re.search("_[0-9]=",i)):
            Query = Query + re.split("_[0-9]",i)[0] +" "+re.split("=",i)[0]+","
            #print(Query)
    #print(Query)
        
    ###Remove last comma in query
    Query = Query[:-1]
    #print(Query)
    ##if(re.search("=_[A-Za-z]",txt)):
    ##  Query = Query + " WHERE TRUE AND "
    #print(Query)


    ### Code to handle ascending and descending order cases
    for i in Entities:
        if (re.findall("AO",i) or re.findall("AO(1)", i)):
            if re.match("AO(2)", i)==None:
                Query = Query + " ORDER BY " + re.split("=",i)[0] + " ASC"
            else:
                break;
        if(re.match("AO(2)", i)):
            print("Hai")
            Query = "," + Query + re.split("=",i)[0] + " ASC"
    
    for i in Entities:
        if i.find("DO")!=-1:
            Query = Query + " ORDER BY " + re.split("=",i)[0] + " DESC"        
    
    #print(Query)
    joinlist = []
    ### handle joins
    join_condition = re.findall("_[A-Za-z]", txt)
    #print(join_condition)
    res = {}
  
    for keys in re.findall("_[A-Za-z]", txt) : 
        res[keys] = res.get(keys, 0) + 1
        #print(res.get(keys))
   

    #print(res)
    flag = ''
    for i,j in res.items():
        if(j==2 or j==3):
            Query = Query + " WHERE TRUE AND "
            flag=i
    #print(flag)
    #print(Entities)
    for i in Entities:
        #print(re.split("=", i)[1])
        #print(re.search(flag,re.split("=", i)[1]))
        if(re.search("_[A-Za-z]", i) and flag!= ""):
        ##if(re.search(flag,re.split("=", i)[1])):
            joinlist.append(re.split("=", i)[0])
    #joinlist.append("temp")
    #print(joinlist)
    #print(Query)
    i =0
    while i< len(joinlist)-1:
        Query = Query + joinlist[i]+ "=" + joinlist[i+1]
        #if(i%2 == 0):
        #Query = Query[:-1]
        if(i%2==0):
            Query = Query + " AND "
        i=i+1
        if(len(joinlist)%2 == 0):
            Query = Query[:-5]
    #print(Query)

    '''#### for condition box with _c
    if (re.search("P._C",txt) or re.search("_C",txt) ):
        if(re.search("WHERE TRUE AND ", Query)):
            Query = Query 
        else :
            Query = Query + " WHERE TRUE AND "
        for i in Entities:
            if re.search("=P._C",i) or re.search("=_C",i):
                #print(re.search("=P._C",i))
                Query = Query + re.split("=",i)[0]
        Query = Query + condition.split("_C")[1]   '''
    #print(Query)

    ## for number conditions directly in table
    for i in Entities:
        if (re.split("=",i)[1]).isnumeric():
            if(re.search("WHERE TRUE AND ", Query)):
                Query = Query + " AND "
            else :
                Query = Query + " WHERE TRUE AND "
            Query = Query + re.split("=",i)[0] + "=" + re.split("=",i)[1]
    #print(Query)

    ## for string condition directly in table
    for i in Entities:
        if(i.find("'")!=-1):
            if(re.search("WHERE TRUE AND ", Query)):
                Query = Query + " AND "
            else:
                Query = Query + " WHERE TRUE AND "
            Query = Query + re.split("=",i)[0] + "=" + re.split("=",i)[1]
    #print(Query)

    ## for conditions with _variable
    #condition_literals = []
    condition_column = []
    condition_literals = re.findall("_[A-Za-z]", condition)
    #print(condition_literals)
    a = 0
    for i in Entities:
        for j in condition_literals:
            if(re.search(j,i)):
                condition_column.append(re.split("=", i)[0])
                #print(condition_column)
                condition=re.sub(j, condition_column[a], condition)
                a = a+1

    if(re.search("WHERE TRUE AND ", Query) and condition!= ''):
        Query = Query + " AND "+condition
    elif (condition!= ''):
        Query = Query + " WHERE TRUE AND "+ condition  
    Query = Query+ ";"          
    return(Query)




            
        


        

