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
    #First we find the driver who completed the most total laps in 2000 by summing their laps.
    # Then we join that driver back to all their 2000 race entries to link them with their fastest-lap records.
    # Finally, we return that driver together with their minimum (fastest) lap time from the year 2000.

    cursor.execute("""
        SELECT  d.Winner, MIN(f.Time) AS min_time
        FROM
        (SELECT Winner, SUM(Laps) AS total_laps
        FROM winners
        WHERE YEAR(Date) = 2000
        GROUP BY Winner
        ORDER BY total_laps DESC
        LIMIT 1) AS d
        JOIN winners AS w ON w.Winner = d.Winner AND YEAR(w.Date) = 2000
        JOIN fastest_laps_updated AS f ON f.Code = w.`Name Code`
        WHERE f.year = 2000
        GROUP BY d.Winner;
    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
