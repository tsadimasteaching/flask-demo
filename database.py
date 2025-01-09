import os
import psycopg2
from dotenv import load_dotenv
from models import User, DBUser, DBJob, DBJobUser, Course, DBCourse

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

    cur.execute('CREATE TABLE if not exists jobs (id SERIAL PRIMARY KEY,'
                 'name VARCHAR(100),'
                 'description VARCHAR(100),'
                 'user_id INT,'
                 'FOREIGN KEY (user_id) REFERENCES users(id));'
                 )

    cur.execute('CREATE TABLE if not exists courses (id SERIAL PRIMARY KEY,'
    'course_name VARCHAR(100) NOT NULL UNIQUE,'
    'description TEXT);'
                )

    cur.execute('CREATE TABLE if not exists user_courses (user_id INT NOT NULL,'
    'course_id INT NOT NULL,'
    'enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'PRIMARY KEY (user_id, course_id),'
    'CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,'
    'CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE);'
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

def get_courses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM courses;')
    rows = cur.fetchall()
    users = [DBCourse(id=row[0], name=row[1], description=row[2]) for row in rows]
    cur.close()
    conn.close()
    return users

def get_jobs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'select jobs.name, jobs.description, jobs.user_id, users.first_name, users.last_name FROM jobs inner join users on jobs.user_id = users.id;',
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    jobs = [DBJobUser(name=row[0],description=row[1], user_id=row[2],firstname=row[3], lastname=row[4]) for row in rows]
    cur.close()
    conn.close()
    return jobs


def get_user_jobs(userid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'select jobs.name, jobs.description, jobs.user_id, users.first_name, users.last_name FROM jobs inner join users on jobs.user_id = users.id WHERE jobs.user_id = %s;',
        (userid,)
    )
    rows = cur.fetchall()
    jobs = [DBJobUser(name=row[0], description=row[1], user_id=row[2], firstname=row[3], lastname=row[4]) for row in rows]
    cur.close()
    conn.close()
    return jobs

def get_user(userid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    # cur.execute('select jobs.name, jobs.description, jobs.user_id, users.first_name, users.last_name FROM jobs inner join users on jobs.user_id = users.id;', (userid,))
    cur.execute('select * from users where id = %s;', (userid,))
    row = cur.fetchone()
    print(row)
    if row is None:
        return None
    user=DBUser(id=row[0], firstname=row[1], lastname=row[2],email=row[3], birth_year=row[4])
    cur.close()
    conn.close()
    return user

def get_course(course_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from courses where id = %s;', (course_id,))
    row = cur.fetchone()
    print(row)
    if row is None:
        return None
    course=DBCourse(id=row[0], name=row[1], description=row[2])
    cur.close()
    conn.close()
    return course

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
    return True

def save_user(user):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (first_name, last_name, email, birth_year) VALUES (%s, %s, %s, %s);',
                (user.firstname, user.lastname, user.email, user.birth_year))
    conn.commit()
    cur.close()
    conn.close()

def save_course(course):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO courses (course_name, description) VALUES (%s, %s);',
                (course.name, course.description))
    conn.commit()
    cur.close()
    conn.close()

def edit_user(user,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE users SET first_name = %s, last_name = %s, email = %s, birth_year = %s WHERE id = %s;',
        (user.firstname, user.lastname, user.email, user.birth_year, id)
    )
    print('query')
    conn.commit()
    cur.close()
    conn.close()

def save_job_user(job, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO jobs (name, description, user_id) VALUES (%s, %s, %s);',
                (job.name, job.description, user_id))
    conn.commit()
    cur.close()
    conn.close()


def enroll_users_to_course(user_id, course_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s);',
                (user_id, course_id))
    conn.commit()
    cur.close()
    conn.close()

def get_user_courses(course_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users JOIN user_courses ON users.id = user_courses.user_id JOIN courses ON user_courses.course_id = courses.id WHERE courses.id = %s;', (course_id,))
    rows = cur.fetchall()
    users = [DBUser(id=row[0], firstname=row[1], lastname=row[2], email=row[3], birth_year=row[4]) for row in rows]
    cur.close()
    conn.close()
    return users