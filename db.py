import sqlite3


class ConnectDB:
    '''CONNECTION CLASS METHOD'''

    @staticmethod
    def create_user_table():
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS user (username TEXT, password TEXT)'
        )
        connection.commit()
        connection.close()

    @staticmethod
    def create_user(username, password):
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, password)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def login_user(username, password):
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM user WHERE username = ? AND password = ? ',
            (username, password)
        )
        # Fetch the user data if a match is found
        user_data = cursor.fetchone()
        connection.commit()
        connection.close()
        
        return user_data

    @staticmethod
    def get_user():
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM user')
        data = cursor.fetchall()
        connection.close()
        return data