import mysql.connector

if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="f1_data",
        port="3307",
    )

    cursor = mydb.cursor()

    # # We pull Ferrari winners and all ARG drivers from two tables and just combine them
    # with UNION. This gives us one clean list with no duplicates and sorted names.
    cursor.execute("""
        (
            SELECT DISTINCT Winner AS driver
            FROM winners
            WHERE Car = 'Ferrari'
        )
        UNION
        (
            SELECT DISTINCT Driver AS driver
            FROM drivers_updated
            WHERE Nationality = 'ARG'
        )
        ORDER BY driver;
    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
