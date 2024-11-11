import pymysql

class Database:
  @staticmethod
  def connect():
    try:
      connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="hotel_rooms_management",
       
      )
      if connection.open:
        print("Database connection successful!")
      return connection
    except pymysql.MySQLError as err:
      print(f"Database connection failed: {err}")
      return None

  def close(self):
    if self.connection and self.connection.open:
        print("Closing database connection")
        self.connection.close()
        
