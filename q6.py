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

    # This query performs a self-join on the winners table to identify all distinct Grand Prix pairs
    # sharing the same lap count (Laps ≥ 80), enforcing pair uniqueness through a lexicographic GP1 < GP2 constraint.
    cursor.execute("""
        SELECT w1.`Grand Prix` AS GP1, w2.`Grand Prix` AS GP2, w1.Laps
        FROM winners AS w1
        JOIN winners AS w2 ON w1.Laps = w2.Laps
        AND w1.`Grand Prix` < w2.`Grand Prix`
        WHERE w1.Laps >= 80
        GROUP BY w1.`Grand Prix`, w2.`Grand Prix`, w1.Laps;
    """)

    print(', '.join(str(row) for row in cursor.fetchall()))

    cursor.close()
    mydb.close()
