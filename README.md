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

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    birth_year INT
);

```