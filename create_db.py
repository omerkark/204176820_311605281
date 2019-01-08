import sqlite3
import os
import sys

def intelizeTables():
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





def insertToClassRoom(parameters, cursor):
    id = int(parameters[1])
    location = parameters[2]
    cursor.execute("INSERT INTO classrooms VALUES(?,?)", (id, location))


def insertToStudents(parameters, cursor):
    grade = parameters[1]
    count = int(parameters[2])
    cursor.execute("INSERT INTO students VALUES(?,?)", (grade, count))

def insertToCourses(parameters, cursor):
    id = int(parameters[1])
    courseName = parameters[2]
    student = parameters[3]
    numOfStudents = int(parameters[4])
    class_id = int(parameters[5])
    courseLength = int(parameters[6])
    cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)", (id, courseName, student, numOfStudents, class_id, courseLength ))





def readFromFile(path):
    dbConnection = sqlite3.connect('schedule.db')
    with dbConnection:
        cursor = dbConnection.cursor()
        inputfilename = path
        with open(inputfilename) as inputfile:
            for line in inputfile:
                splitedData = line.split(", ")
                # INSERT TO TABLE CLASSROOM
                toTable = splitedData[0]
                if toTable == 'C':
                    insertToCourses(splitedData, cursor)
                elif toTable == 'S':
                    insertToStudents(splitedData, cursor)
                else:
                    insertToClassRoom(splitedData, cursor)

def main(args):
    intelizeTables()
    readFromFile(args[1])

if __name__ == '__main__':
    main(sys.argv)






