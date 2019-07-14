"""
todo:
1. logging
2. shut down
3. comments
4. config file
"""

import MySQLdb
from flask import Flask, Response


app = Flask(__name__)

def check_helper(test):
    db = MySQLdb.connect('localhost', 'fakeName', 'fakePass', 'fakeDB')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM testing WHERE url = '%s' LIMIT 1" % test)

    if cursor.fetchone() is None:
        # Allow this request
        return 'True'
    else:
        # block
        return 'False'

@app.route("/urlinfo/1/<path:test>")
def url_lookup(test):
    result = check_helper(test)
    return Response(result), 200

if __name__ == "__main__":
    app.run(debug=False)
