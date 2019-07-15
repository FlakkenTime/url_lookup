#!/usr/bin/python3
"""
This is the web app for url_lookup.
It can be used for checking if a URL is allowed
and updating the database.
See README for setup and usage instructions
"""

import MySQLdb
from configparser import ConfigParser
from flask import Flask, Response, request

# setup config for db
config = ConfigParser()
config.read('resources/db.ini')


app = Flask(__name__)


def db_connect():
    """
    Helper function that connects and returns a db connection
    """
    db = MySQLdb.connect(config['Database']['Connect'],
                         config['Database']['User'],
                         config['Database']['Password'],
                         config['Database']['Database_Name'])
    return db


def check_helper(test):
    """
    Helper function that connects to the database and checks if this is safe
    :param test: String. The url to test
    :return: String. True / False
    """
    db = db_connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM url_table WHERE url = %s LIMIT 1", [test])
    result = cursor.fetchone()
    db.close()

    if result is None:
        # Allow this request
        return 'True'
    else:
        # block
        return 'False'


@app.route("/urlinfo/1/<path:test>", methods=['GET'])
def url_lookup(test):
    """
    This pulls everything in the url after /urlinfo/1/ and
    puts it in the variable test. This is the part we're checking
    on.
    Note it drops parameters after ? which shouldn't be needed.
    :param test: String. The url we're checking for safety
    :returns: String. True / False
    """
    result = check_helper(test)
    return Response(result), 200


def update_helper(urls):
    """
    Pushes url updates to DB
    :param urls: String. Comma separated urls.
    :return: (Boolean, String) (True / False, None / Error)
    """
    db = db_connect()
    try:
        db = db_connect()
        cursor = db.cursor()

        # Generate our query escaping the URLs. From my reading much faster
        # than using execute many and having it prepare the query.
        query = 'INSERT INTO url_table (url) VALUES '
        url_split = urls.split(',')
        for url in url_split:
            # note need to conver the byte string
            query += "('%s')," % db.escape_string(url).decode("utf-8")

        # drop trailing ,
        query = query[:-1]

        result = cursor.execute(query)
        db.commit()
        db.close()

        # Extra check that the number of updates matches the number we received
        if result == len(url_split):
            return (True, None)
        else:
            return (False, "Incorrect number of updates to db")

    except Exception as e:
        # Catch the generalized exception
        db.close()
        return (False, "Error hit. Check logs")


@app.route("/urlupdate/1/", methods=['POST'])
def url_update():
    """
    Used for pushing new urls to the database
    """
    # Pull the json and verify input
    json = request.get_json()
    if json is None:
       return "False no parameters provided", 200

    elif json.get('PASS', None) is None:
        return "False no pass provided", 200

    elif json.get('urls', None) is None:
        return "False no urls provided", 200

    elif json['PASS'] != config['Database']['Update_Pass']:
        # don't tell them bad pass
        return "False", 200

    # add the URL
    result = update_helper(json['urls'])
    if result[0] is True:
        return "True", 200
    else:
        return result[1], 200


if __name__ == "__main__":
    app.run(debug=True)
