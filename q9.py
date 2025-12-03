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

    # First we calculate the average points for each nationality from the drivers table.
    # Then we find the fastest recorded lap time for each nationality by matching drivers to their lap results.
    # Finally, we get the most recent win date for each nationality and combine everything into one result.

    cursor.execute("""
        WITH avg_points AS (
        SELECT Nationality, AVG(PTS) AS avg_pts
        FROM drivers_updated
        GROUP BY Nationality
        ),
        min_fastest AS(
        SELECT drivers_updated.Nationality, MIN(fastest_laps_updated.Time) AS min_time
        FROM drivers_updated, fastest_laps_updated
        WHERE drivers_updated.Driver = fastest_laps_updated.Driver
        GROUP BY drivers_updated.Nationality
        ),
        latest_win AS(
        SELECT drivers_updated.Nationality, MAX(winners.Date) AS latest
        FROM drivers_updated, winners
        WHERE drivers_updated.Driver = winners.Winner
        GROUP BY drivers_updated.Nationality
        )
        SELECT avg_points.Nationality, avg_points.avg_pts, min_fastest.min_time, latest_win.latest
        FROM avg_points
        LEFT JOIN min_fastest USING (Nationality)
        LEFT JOIN latest_win USING (Nationality)
    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
