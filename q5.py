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

    # 1 - I used AVG to help me calculate , 2- I did JOIN with the KEY : CAR , 3 - now i can start use the conditions when it is less then 2 minutes
    # 4 - group by the team = CAR  with DEAC
    cursor.execute("""
        SELECT teams_updated.Car, AVG(teams_updated.PTS) AS avg_pts
        FROM teams_updated
        JOIN fastest_laps_updated ON teams_updated.Car = fastest_laps_updated.Car
        WHERE MINUTE(STR_TO_DATE(fastest_laps_updated.Time, '%i:%s.%f')) < 2
        GROUP BY teams_updated.Car
        ORDER BY avg_pts DESC;
    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
