import sqlite3

_HISTORY_TABLE_NAME = "history"
conn = sqlite3.connect('test.db')

classes = {'safe': 1, 'unsafe': 2}


def add_history(file_name, label):
    print(label)
    conn.execute("INSERT INTO {} VALUES ('{}', '{}', 0)".format(_HISTORY_TABLE_NAME, file_name, classes[label]))


def get_reviewed_files():
    data = []
    rows = conn.execute("SELECT * FROM {} WHERE reviewed=1".format(_HISTORY_TABLE_NAME))
    for row in rows:
        data.append(row)
    return data


def get_reviewable_files():
    return conn.execute("SELECT * FROM {} WHERE reviewed=0".format(_HISTORY_TABLE_NAME))


if __name__ == '__main__':
    get_reviewed_files()
