import sqlite3


class ConnectDB:
    '''CONNECTION CLASS METHOD'''

    @staticmethod
    def create_user_table():
        '''create user tables'''
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS user ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'username TEXT, '
            'password TEXT, '
            'fullname TEXT, '
            'card_number TEXT, '
            'expiration_date TEXT, '
            'cvv TEXT)'
        )
        connection.commit()
        connection.close()
    
    @staticmethod
    def create_prediction_table():
        '''create prediction table'''
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        # username, transaction_time, amount, card_expiration_date, card_number,
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS prediction ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'username TEXT,'
            'transaction_time TEXT,'
            'amount TEXT,'
            'card_expiration_date TEXT,'
            'card_number TEXT,'
            'v4 REAL,'
            'v7 REAL,'
            'v9 REAL,'
            'v12 REAL,'
            'v18 REAL,'
            'v19 REAL,'
            'v20 REAL,'
            'v21 REAL,'
            'v22 REAL,'
            'v28 REAL,'
            'status TEXT'
            ')'
        )
        connection.commit()
        connection.close()

    @staticmethod
    def create_user(
        username,
        password,
        fullname,
        card_number,
        expiration_date,
        cvv
    ):
        '''create users func'''
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO user (username, password, fullname, card_number, \
                expiration_date, cvv) VALUES (?, ?, ?, ?, ?, ?)',
            (username, password, fullname, card_number, expiration_date, cvv)
        )
        connection.commit()
        connection.close()
    
    @staticmethod
    def create_prediction(
        username,
        transaction_time,
        amount,
        card_expiration_date,
        card_number,
        v4, v7, v9, v12, v18, v19, v20, v21, v22, v28,
        status
    ):
        '''create users func'''
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO prediction (username, transaction_time, amount, card_expiration_date, card_number, v4, v7, v9, v12, v18, v19, v20, v21, v22, v28, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (username, transaction_time, amount, card_expiration_date, card_number, v4, v7, v9, v12, v18, v19, v20, v21, v22, v28, status)
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
    def get_predictions(usr=None):
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM prediction')
        data = cursor.fetchall()
        connection.close()
        return data
    
    @staticmethod
    def get_user():
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username, fullname, card_number, \
                       expiration_date FROM user')
        data = cursor.fetchall()
        connection.close()
        return data
    
    @staticmethod
    def check_user_card(
        fullname,
        card_number,
        expiration_date,
        cvv
    ):
        """check card details"""
        # Connect to the database
        connection = sqlite3.connect('creditcard.db')
        cursor = connection.cursor()

        # Execute the SELECT query
        cursor.execute(
            'SELECT * FROM user WHERE fullname = ? AND card_number = ? AND expiration_date = ? AND cvv = ?',
            (fullname, card_number, expiration_date, cvv)
        )

        # Fetch the result
        result = cursor.fetchone()

        # Close the connection
        connection.close()

        # Return True if the result is not None, indicating the user exists
        return result is not None