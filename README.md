### get code

```bash
git clone https://github.com/tsadimasteaching/flask-demo
```

### create virtual environment, activate and install dependencies
```bash
cd flask-demo
python3 -m venv flaskenv
source flaskenv/bin/activate
pip install -r requirements.txt
```

### create .env and fill the db params

```bash
cp .env.example .env
```
### run the app
```bash
 flask --app main run --host 0.0.0.0 --port 5000 --debug --reload
```

    

## Database creation
* go to https://render.com/
* create an account
* create a new database from https://dashboard.render.com/
* copy the connection string
* connect to database from the terminal
```bash
PGPASSWORD=<DB_PASSWORD> psql -h <DB_SERVER> -U <DB_USER> <DATABASE_NAME>
```

### create the table
```sql

CREATE TABLE if not exists users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    birth_year INT
);

CREATE TABLE if not exists jobs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(100),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id));


CREATE TABLE if not exists courses (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT);
                
                                                              
CREATE TABLE if not exists user_courses (
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, course_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE);
                                                              
                                                              
                                                              
                 

```