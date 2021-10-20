import sys
import json

def generate_html(db):
    cs  = db['caption']
    s1 ='''
        <html>
            <header>
                <title>'''+cs+'''</title>
                <script src="'''+db['name']+'''.js"></script>
            </header>
            <body>
                <h3>'''+cs+'''</h3><br/>
        '''   
    elements = db['elements']
    for x in elements:
         etype = x['etype']
         if etype=='textbox':
             s1=s1+'''
                <label>'''+x['caption']+'''</label>
                <input name= "'''+x['ename']+'''" size= "'''+x['size']+'''" maxlength="'''+x['maxlength']
             if x['datatype'] =='integer':
                s1=s1+'''" type = "number" />
                <br/><br/>'''
             elif x['datatype'] =='string':
                s1=s1+'''" type = "text" />
                <br/><br/>'''
         
         elif etype=='checkbox':
             s1=s1+'''
                
                <label>'''+x['caption']+'''</label><br/>'''
             for k in x['group']:
                 s1=s1+'''
                <input type="checkbox" value="'''+k['value']+'''" name="'''+x['ename']
                 if 'checked' in k:
                     s1=s1+'''"  checked>'''+k['caption']+'''</input><br/>'''
                 else:
                     s1=s1+'''">'''+k['caption']+'''</input><br/>'''

         elif etype=='selectlist':
             s1=s1+'''
                <br/>

                <label>'''+x['caption']+'''</label><br/>
                <select name="'''+x['ename']+'''">'''
             for k in x['group']:
                 s1=s1+'''
                    <option value="'''+k['value']+'''">'''+k['caption']+'''</option>'''
             s1+='''
                </select><br/>'''
         elif etype=='radiobutton':
             s1=s1+'''
                <br/>

                <label>'''+x['caption']+'''</label><br/>'''
             for k in x['group']:
                 s1=s1+'''
                <input type="radio" value="'''+k['value']+'''" name="'''+x['ename']+'''" >'''+k['caption']+'''</input><br/>'''
         elif etype=='submit':
             s1+='''
                <br/>

                <button onclick="myFunction()" name="'''+x['ename']+'''">'''+x['caption']+'''</button>'''
         elif etype=='reset':
             s1+=''' 
                <button onclick="reload()" name="'''+x['ename']+'''">'''+x['caption']+'''</button>'''
         elif etype=='multiselectlist':
             s1=s1+'''
                <br/>

                <label>'''+x['caption']+'''</label><br/>
                <select name="'''+x['ename']+'''" size="'''+x['size']+'''" multiple>'''
             for k in x['group']:
                 s1=s1+'''
                    <option value="'''+k['value']+'''">'''+k['caption']+'''</option>'''
             s1+='''
                </select><br/>'''
    s1+='''
            </body>
        </html>'''

    print(s1)  
    f = open(db['name']+".html", "w+")
    f.write(s1)
    f.close()


def generate_js(db):
    cs=db['elements']
    s2='''function myFunction(){
    
    var data={};'''
    elements = db['elements']

    
    for x in elements:
        etype = x['etype']
        if etype=='textbox':
            s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0].value;
    data["'''+x['ename']+'''"] = '''+x['ename']

        elif etype=='checkbox':
            s2+='''
    var '''+x['ename']+'''Selected = [];
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''");
    for(i=0; i<'''+x['ename']+'''.length; i++){
        if('''+x['ename']+'''[i].checked == true){
            '''+x['ename']+'''Selected.push('''+x['ename']+'''[i].value)
        }
    }
    data["'''+x['ename']+'''"] = '''+x['ename']+'''Selected;'''

        elif etype=='selectlist':
            s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0];
    var '''+x['ename']+'''Selected = '''+x['ename']+'''.options['''+x['ename']+'''.selectedIndex].value;
    data["'''+x['ename']+'''"] = '''+x['ename']+'''Selected;'''

        elif etype=='radiobutton':
            s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''");
    for(i=0; i<'''+x['ename']+'''.length; i++){
        if('''+x['ename']+'''[i].checked == true){
            data["'''+x['ename']+'''"] = '''+x['ename']+'''[i].value;
        }
    }'''
        elif etype=="multiselectlist":
            s2+=''' 
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0];
    var '''+x['ename']+'''Selected = [];
    for(var i=0; i<'''+x['ename']+'''.length; i++){
        if('''+x['ename']+'''.options[i].selected){
            '''+x['ename']+'''Selected.push('''+x['ename']+'''.options[i].value);
        }  
    }
    data["'''+x['ename']+'''"] = '''+x['ename']+'''Selected;'''

    s2+='''
    console.log(data);

    var url = '''+db['backendURL']+'''
    $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
        if (response.ok) {
            alert("Insert Sucessful")
        },
        error: function(error) {
            alert("ERROR");
            console.log(error);
        }
    });
}

function reload(){
    window.location.reload();
}'''
    print(s2)
    f = open(db['name']+".js", "w+")
    f.write(s2)
    f.close()
    







def generate_py(db):
    s3='''
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import mysql.connector as mysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webforms/', methods=['POST'])
def insert_data():'''

    mainTable=[]
    seperateTable=[]
    key = ''
    for x in db['elements']:
        etype = x['etype']
        if etype == "textbox" or etype=='selectlist' or etype=='radiobutton':
            mainTable.append(x['ename'])
        elif etype == "checkbox" or etype=='multiselect' :
            seperateTable.append(x['ename'])
        
        if 'key' in x:
            key = x['ename']
    
    s3+='''
    sql1 = "INSERT INTO '''+db['name']+''' values ('''
    for x in mainTable:
        s3+=''' '" + request.json[\''''+x+'''\'] + "','''
    
    s3=s3[:-1]+''' )" '''

    s3+='''
    database = mysql.connect(
        host = "localhost",
        database = '''+db['mysqlDB']+'''
        user = '''+db['mysqlUserID']+'''
        passwd = '''+db['mysqlPWD']+'''
        auth_plugin = 'mysql_native_password'
    )
    cursor = database.cursor()
    try:
        cursor.execute(sql1)
        database.commit()
        result = {"ok": True, "msg": 'Main table data insertion Success'}
    except Exception as e:
        database.rollback()
        cursor.close()
        database.close()
        result = {"ok": False, "msg": 'Data Inserstion into '''+db['name']+''' table Failed' "exception":'e'}
        return jsonify(result)'''


    for y in seperateTable:
        s3+='''
    for k in request.json[\''''+y+'''\']
        '''+y+''' = "INSERT INTO '''+y+''' values ('" +request.json[\''''+key+'''\']+ "','" +k+ "')"
        try:
            cursor.execute('''+y+''')
            result = {"ok": True, "msg": 'seperate data insertion Success'}
        except Exception as e:
            database.rollback()
            cursor.close()
            database.close()
        result = {"ok": False, "msg": 'Data Inserstion into '''+y+''' table Failed' "exception":'e''}
        return jsonify(result)'''

    s3+='''
    database.commit()
    cursor.close()
    database.close()
    return jsonify(result)'''

    print(s3)
    f = open(db['name']+".py", "w+")
    f.write(s3)
    f.close()




def main():
  with open(sys.argv[1],'r') as fp:
    db = json.load(fp)
    generate_html(db) # This function will generate html file
    #generate_js(db) # this function will generate javascript file
    #generate_py(db) #This function will generate python file

main()
