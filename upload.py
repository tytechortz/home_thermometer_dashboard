def create_connection(home_temps.db):

    try:
        conn = sqlite3.connect(home_temps)
        return conn
    except Error as e:
        print(e)
    
    return None
