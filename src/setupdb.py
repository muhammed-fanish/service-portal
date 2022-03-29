import sqlite3

# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('users.sqlite3')

# cursor object
cursor_obj = connection_obj.cursor()

# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS GEEK")

# Creating table
table = """ CREATE TABLE USERS (
            id INT,
			Email CHAR(255) NOT NULL,
            wso2UserId CHAR(25),
			userName CHAR(25) NOT NULL,
			providerName CHAR(25),
            apiKey CHAR(25),
            phoneNumber CHAR(25),
			active INT
		); """

cursor_obj.execute(table)

print("Table is Ready")

# Close the connection
connection_obj.close()
