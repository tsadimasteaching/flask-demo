import os
import psycopg2
from dotenv import load_dotenv
from models import User, DBUser

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   print('DB_HOST is {}'.format(os.environ.get('DB_HOST')))
else:
   raise RuntimeError('Not found application configuration')


def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'])
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE if not exists users (id SERIAL PRIMARY KEY,'
                'first_name VARCHAR(100),'
                'last_name VARCHAR(100),'
                'email VARCHAR(100),'
                'birth_year INT);'
                )
    conn.commit()
    cur.close()
    conn.close()

def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    rows = cur.fetchall()
    users = [DBUser(id=row[0], firstname=row[1], lastname=row[2],email=row[3], birth_year=row[4] ) for row in rows]
    cur.close()
    conn.close()
    return users

def get_user(userid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s;', (userid,))
    row = cur.fetchone()
    print(row)
    if row is None:
        return None
    user=DBUser(id=row[0], firstname=row[1], lastname=row[2],email=row[3], birth_year=row[4])
    cur.close()
    conn.close()
    return user

def delete_user(userid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s;', (userid,))
    row = cur.fetchone()
    print(row)
    if row is None:
        cur.close()
        conn.close()
        return False
    cur.execute('DELETE FROM users WHERE id = %s;', (userid,))
    conn.commit()
    cur.close()
    conn.close()

def save_user(user):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (first_name, last_name, email, birth_year) VALUES (%s, %s, %s, %s);',
                (user.firstname, user.lastname, user.email, user.birth_year))
    conn.commit()
    cur.close()
    conn.close()