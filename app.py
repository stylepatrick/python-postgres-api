#!/usr/bin/python
import psycopg2
from flask import request, jsonify, Flask
from psycopg2.extras import RealDictCursor

from config import config

app = Flask(__name__)
app.config["DEBUG"] = True


def db_selector(select):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(select)
        res = cur.fetchall()
        cur.close()
        return jsonify(res)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'Internal Server Error check Server logs.'
    finally:
        if conn is not None:
            conn.close()


def db_insert(insert):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(insert)
        cur.close()
        conn.commit()
        return 'Done!'
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'Internal Server Error check Server logs.'
    finally:
        if conn is not None:
            conn.close()


@app.route('/', methods=['GET'])
def init():
    return "API works!"


@app.route('/user', methods=['GET'])
def get_user():
    select = "SELECT distinct(user_id) from money;"
    return db_selector(select)


@app.route('/money', methods=['GET'])
def get_money():
    if 'user_id' in request.args:
        user_id = str(request.args['user_id'])
        select = "SELECT amount, note, created_at from money where user_id ='%s'" % user_id
        return db_selector(select)
    else:
        return "No User provided!"


@app.route('/money/create', methods=['GET'])
def insert_money():
    if 'user_id' and 'amount' in request.args:
        user_id = str(request.args['user_id'])
        amount = float(request.args['amount'])
        insert = "INSERT INTO money (user_id, amount) VALUES ('%s', %f)" % (user_id, amount)
        return db_insert(insert)
    else:
        return "No User and/or amount provided!"


if __name__ == "__main__":
    app.run()
