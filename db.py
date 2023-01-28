import sqlite3

conn = sqlite3.connect('mngr.dat', check_same_thread=False)
cur = conn.cursor()

def initialize_db(): 
    cur.execute('''
    CREATE TABLE IF NOT EXISTS mypass(id integer primary key autoincrement, service text, handle text, password text)
    ''')

def close_db():
    conn.close()

def create_pass(service, handle, password):
    try: 
        cur.execute('''
            INSERT INTO mypass(service, handle, password)
            VALUES(?, ?, ?)
            ''', (service, handle, password))
        conn.commit()
        return 0
    except:
        return 1

def change_pass(id, password):
    try:
        cur.execute('''
        UPDATE mypass SET password = ? 
        WHERE id = ?;
        ''', (password, id))
        conn.commit()
        return 0
    except Exception as e:
        print(e)

     
def delete_pass(id):
    try:
        cur.execute('''
        DELETE FROM mypass
        WHERE id = ?;
        '''), (id)
        conn.commit()
        return 0
    except:
        return 1


def get_all():
    cur.execute('''SELECT * FROM mypass''')
    return cur.fetchall()

def get_by_service(service):
    service = "%" + service + "%"
    cur.execute(
        '''
        SELECT * FROM mypass
        WHERE service LIKE ?
        ''',
    (service,)
    )
    return cur.fetchall()

def get_by_handle(handle):
    handle = "%" + handle + "%"
    cur.execute(
        '''
        SELECT * FROM mypass
        WHERE handle LIKE ?
        ''', (handle,)
    )
    return cur.fetchall()

def get_by_id(id):
    cur.execute(
        '''
        SELECT * FROM mypass
        WHERE id = ?
        ''', (str(id),)
        )
    return cur.fetchone()