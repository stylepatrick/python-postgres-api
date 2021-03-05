#!/usr/bin/python
import flask
import psycopg2
from flask import request, jsonify
from config import config

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dbselector(select):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(select)
        res = cur.fetchall()
        cur.close()
        return jsonify(res)
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn is not None:
            conn.close()


def dbinsert(insert):
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
        return error
    finally:
        if conn is not None:
            conn.close()


@app.route('/', methods=['GET'])
def init():
    return "API works!"


@app.route('/user', methods=['GET'])
def getUser():
    select = "SELECT distinct(user_id) from money;"
    return dbselector(select)


@app.route('/money', methods=['GET'])
def getMoney():
    if 'user_id' in request.args:
        user_id = str(request.args['user_id'])
        select = "SELECT amount, note, created_at from money where user_id ='%s'" % user_id
        return dbselector(select)
    else:
        return "No User provided!"


@app.route('/money/create', methods=['GET'])
def insertMoney():
    if 'user_id' and 'amount' in request.args:
        user_id = str(request.args['user_id'])
        amount = float(request.args['amount'])
        insert = "INSERT INTO money (user_id, amount) VALUES ('%s', %f)" % (user_id, amount)
        return dbinsert(insert)
    else:
        return "No User and/or amount provided!"


app.run()
