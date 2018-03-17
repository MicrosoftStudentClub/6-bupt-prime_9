from flask import Flask, request
from fuzzywuzzy import process
import sqlite3 as sq3

vscode = ['vscode', 'vs code', 'visual studio code', 'code']

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    # print(request.form.to_dict())
    action = request.form.get('action', 'none')
    software = request.form.get('software', 'none')
    if software in vscode:
        software = vscode[0]
    else:
        res = '{"data":"' + 'The software is not in out list. Please try another name or give up.' + '"}'
        return res
    
    conn = sq3.connect('sheets.db')
    c = conn.cursor()
    table = list(c.execute('select action, key from vscode'))
    action = process.extractOne(action, table[:][0])[0]
    for row in table:
        if row[0] == action:
            res = row[1]
            break
    res = '{"data":"' + 'The key for action ' + action + ' is ' + res + '"}'
    return res

if __name__ == '__main__':
    app.run(debug=True)
