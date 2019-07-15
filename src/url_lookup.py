"""
todo:
1. logging
2. shut down
3. comments
4. config file
"""

import MySQLdb
from configparser import ConfigParser
from flask import Flask, Response

# setup config for db
config = ConfigParser()
config.read('resources/db.ini')


app = Flask(__name__)

def check_helper(test):
    """
    Helper function that connects to the database and checks if this is safe
    :param test: String. The url to test
    :return: String. True / False
    """
    db = MySQLdb.connect(config['Database']['Connect'],
                         config['Database']['User'],
                         config['Database']['Password'],
                         config['Database']['Database_Name'])
    cursor = db.cursor()
    cursor.execute("SELECT * FROM testing WHERE url = %s LIMIT 1", [test])

    if cursor.fetchone() is None:
        # Allow this request
        return 'True'
    else:
        # block
        return 'False'

@app.route("/urlinfo/1/<path:test>")
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

if __name__ == "__main__":
    app.run(debug=False)
