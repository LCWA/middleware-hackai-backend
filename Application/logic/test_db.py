from click import command
import psycopg2

conn_string = "postgres://missionautomate:Parola1234%23@postgre-db-server.postgres.database.azure.com:5432/postgres"

def get_gallery(id):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    command = """
            SELECT imgLink
            FROM gallery
            WHERE googleId = 
    """
    command += str(id)
    cursor.execute(command)
    return(cursor.fetchall)

def add_user(data):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()   
    command = "INSERT INTO users (user_id, user_fname, user_lname, user_email)VALUES (%s, %s, %s, %s)"
    cursor.execute(command, (data[0], data[1], data[2], data[3]))
    cursor.close()
    conn.commit()

# print the connection string we will use to connect
# print ("Connecting to database\n	->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
# conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
# cursor = conn.cursor()
# command = """
#         CREATE TABLE gallery (
#             google_id SERIAL PRIMARY KEY,
#             imgLink VARCHAR(255) NOT NULL
#         )
#         """
# command = "INSERT INTO users (user_id, user_fname, user_lname, user_email)VALUES (%s, %s, %s, %s)"
# print ("Connected!\n")

# cursor.execute(command, (23213, 'David', 'Copoeru', 'copoerudavid25@gmail.com'))
# command = """
#             SELECT user_lname
#             FROM users
#             WHERE user_id = %s
#     """
# command = """
#         SELECT * FROM users """
# cursor.execute(command, [23213])
# cursor.execute(command)
# result = cursor.fetchone
# print(result)
# cursor.close()
# conn.commit()