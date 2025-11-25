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

    cursor.execute("""
      SELECT 
    d.Winner,
    MIN(f.Time) AS min_time
FROM
    (SELECT Winner, SUM(Laps) AS total_laps
     FROM winners
     WHERE YEAR(Date) = 2000
     GROUP BY Winner
     ORDER BY total_laps DESC
     LIMIT 1) AS d
JOIN winners AS w
    ON w.Winner = d.Winner AND YEAR(w.Date) = 2000
JOIN fastest_laps_updated AS f
    ON f.Code = w.`Name Code`    -- ← זה המפתח האמיתי!
WHERE f.year = 2000
GROUP BY d.Winner;



    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
