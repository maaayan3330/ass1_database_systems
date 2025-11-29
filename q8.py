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

    #  i total Ferrari's points and Maserati's points directly inside one SELECT.
    # Then i subtract the two totals to get the final difference (diff).
    cursor.execute("""
       SELECT
            (SELECT SUM(PTS) 
            FROM teams_updated
            WHERE Car = 'Ferrari')
        -   (SELECT SUM(PTS)
            FROM teams_updated
            WHERE Car = 'Maserati')
        AS diff;
    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
