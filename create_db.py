import sqlite3
import os
import sys

def main():
    databaseexisted = os.path.isfile('schedule.db')

    dbConnection = sqlite3.connect('schedule.db')
    with dbConnection:
        cursor = dbConnection.cursor()
        if not databaseexisted:
            cursor.execute("""CREATE TABLE courses(
                        id INTEGER PRIMARY KEY, 
                        course_name TEXT NOT NULL,
                        student TEXT NOT NULL,
                        number_of_students INTEGER NOT NULL,
                        class_id INTEGER REFERENCES classrooms(id),
                        course_length INTEGER NOT NULL)""")

            cursor.execute("""CREATE TABLE students(
                        grade TEXT PRIMARY KEY,
                        count INTEGER NOT NULL )""")

            cursor.execute("""CREATE TABLE classrooms(id INTEGER PRIMARY KEY,
                            location TEXT NOT NULL,
                            current_course_id INTEGER NOT NULL,
                            current_course_time_left INTEGER NOT NULL )""")
    return




if __name__ == '__main__':
    main(sys.argv)
