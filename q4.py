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

    # first i do the first SELECT for find how mach races where won in 2001 but i miss the info
    # of who is the currect CAR so i did another SELECT that return a CAR and then the
    # first SELECT can answer the Q 
    cursor.execute("""
        SELECT COUNT(*) AS wins_2001
        FROM winners
        WHERE YEAR(Date) = 2001
        AND Car = (
                SELECT Car
                FROM winners
                WHERE YEAR(Date) = 1999
                GROUP BY Car
                ORDER BY COUNT(*) DESC
                LIMIT 1
    );

    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
