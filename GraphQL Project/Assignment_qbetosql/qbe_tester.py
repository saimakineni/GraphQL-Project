import sys
import graphene
import mysql.connector
import re
import sample

class Authenticate(graphene.ObjectType):
    table_names = graphene.String()

class Skeleton(graphene.ObjectType):
    colname = graphene.String()
    coltype = graphene.String()

class Qbetomysql(graphene.ObjectType):
    qbetosqlquery = graphene.String()
    resultquery = graphene.List(graphene.String)
    queryParams = graphene.String()
    queryCondParams = graphene.String()



class Queries(graphene.ObjectType):
    authen = graphene.List(Authenticate,uname = graphene.String(),upass = graphene.String(),database_name = graphene.String())
    tables = graphene.List(Skeleton, uname = graphene.String(), upass = graphene.String(), database_name= graphene.String(), table_name = graphene.String())
    qbetomysql = graphene.List(Qbetomysql, uname = graphene.String(), upass = graphene.String(), database_name = graphene.String(),queryParams=graphene.String(), queryCondParams=graphene.String())
    
    def resolve_authen(self,info,uname,upass,database_name):
        mydb = mysql.connector.connect(
            host="localhost",
            user=uname,
            password=upass,
            auth_plugin='mysql_native_password',
            database=database_name
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '"+database_name+"'")
        d = [str(x[0]) for x in mycursor]
        mycursor.close()
        mydb.close()

        res = []
        for t in d:
            res.append(Authenticate(table_names=t))
        print(d,res)
        return res


    def resolve_tables(self,info,uname,upass,database_name,table_name):
        db = mysql.connector.connect(
            host="localhost",
            user=uname,
            password=upass,
            auth_plugin='mysql_native_password',
            database=database_name
        )
        query = " SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+table_name+"' and TABLE_SCHEMA = '"+database_name+"'"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        columns = []
        for record in records:
            columns.append(Skeleton(colname=record[0], coltype=record[1]))
        return columns


    def resolve_qbetomysql(self,info,uname,upass,database_name,queryParams,queryCondParams):
        
        sqlQuery = sample.sqltoqbepython(queryParams,queryCondParams)
        
        mydb = mysql.connector.connect(
            host="localhost",
            user=uname,
            password=upass,
            auth_plugin='mysql_native_password',
            database=database_name
        )
        mycursor = mydb.cursor()
        query = sqlQuery
        print(query)
        mycursor.execute(query)
        records = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        result = []
        for record in records:
            result.append(Qbetomysql(qbetosqlquery = query, resultquery = record))
        return result

    
schema = graphene.Schema(query=Queries)