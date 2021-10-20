
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import mysql.connector as mysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webforms/', methods=['POST'])
def insert_data():
    sql1 = "INSERT INTO interests values ( '" + request.json['sid'] + "', '" + request.json['sname'] + "', '" + request.json['degree'] + "' )" 
    database = mysql.connect(
        host = "localhost",
        database = raj
        user = raj
        passwd = r123
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
        result = {"ok": False, "msg": 'Data Inserstion into interests table Failed' "exception":'e'}
        return jsonify(result)
    for k in request.json['pls']
        pls = "INSERT INTO pls values ('" +request.json['sid']+ "','" +k+ "')"
        try:
            cursor.execute(pls)
            result = {"ok": True, "msg": 'seperate data insertion Success'}
        except Exception as e:
            database.rollback()
            cursor.close()
            database.close()
        result = {"ok": False, "msg": 'Data Inserstion into pls table Failed' "exception":'e''}
        return jsonify(result)
    database.commit()
    cursor.close()
    database.close()
    return jsonify(result)