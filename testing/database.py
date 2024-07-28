import psycopg2

hostname = 'localhost'
database = 'demo'
username = 'postgres'
pwd = 'mamlesh'
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )

    conn.autocommit = True

    cur = conn.cursor()

    create_script = '''CREATE TABLE IF NOT EXISTS employee (
                        id INT PRIMARY KEY,
                        name VARCHAR(40) NOT NULL,
                        salary INT,
                        dept_id VARCHAR(20))'''
    cur.execute(create_script)

    insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
    insert_values = [
        (1, 'Alice', 70000, 'D001'),
        (2, 'Bob', 80000, 'D002'),
        (3, 'Charlie', 75000, 'D001'),
        (4, 'James', 12000, 'D1')
    ]

    for record in insert_values:
        cur.execute(insert_script, record)

    conn.commit()

    cur.execute('SELECT * FROM employee')
    rows = cur.fetchall()
    for row in rows:
        print(row)

    print("Table created and values inserted successfully")

except Exception as error:
    print("Error while executing SQL:", error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
