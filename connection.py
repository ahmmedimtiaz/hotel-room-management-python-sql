import pymysql

# MySQL connection setup
connection = pymysql.connect(
    host='localhost',
    port=3306,  # Default MySQL port
    user='root',
    password='',  # Leave blank if no password is set for MySQL root user
    db='hotel_room_management'  # Database name
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()
        print("Connected to:", result)
finally:
    connection.close()
