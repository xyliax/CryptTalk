from pysqlcipher3 import dbapi2 as sqlite

def createtable(dbname,password) :
    conn = sqlite.connect(dbname)
    conn.execute(f"PRAGMA key='{password}'")
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT,
        email TEXT
    )
    '''
    conn.execute(create_table_query)
    return conn
def add_data(conn,username, password, email):
    insert_data_query = '''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
    '''
    data = [(username, password, email)]
    conn.executemany(insert_data_query, data)
    conn.commit()

def check_member_exists(conn,name):
    query = '''
    SELECT * FROM users WHERE username = ?
    '''
    result = conn.execute(query,(name,)).fetchone()
    return result is not None
def delete_table(conn):
    query = '''
    DROP TABLE users
    '''
    conn.execute(query)
    conn.commit()
def checkpassword(conn,username,password):
    query = '''
    SELECT password FROM users WHERE username = ?
    '''
    result = conn.execute(query,(username,)).fetchone()
    if result[0] == password:
        return True
    return False
def getemail(conn,username):
    query = '''
    SELECT email FROM users WHERE username = ?
    '''
    result = conn.execute(query,(username,)).fetchone()
    return result[0]