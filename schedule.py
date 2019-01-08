import sqlite3
import os


databaseexisted = os.path.isfile('schedule.db')

dbConnection = sqlite3.connect('schedule.db')
cursor = dbConnection.cursor()

clock = 0;

cursor.execute("SELECT * FROM courses")
x = cursor.fetchall();

# while(len(x) > 0):
cursor.execute("SELECT * FROM classrooms as c JOIN courses ON c.id = courses.class_id WHERE current_course_time_left LIKE 0")
freeClassRooms = cursor.fetchall()
for i in freeClassRooms:
    print(i)




