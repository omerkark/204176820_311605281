import sqlite3
import os

databaseexisted = os.path.isfile('schedule.db')
dbConnection = sqlite3.connect('schedule.db')
cursor = dbConnection.cursor()


def classesTOFill(allOptionalCourseToClass):
    if (len(allOptionalCourseToClass) > 0):
        id = allOptionalCourseToClass[0][0]
        finalCourseToClass = []
        finalCourseToClass.append(allOptionalCourseToClass[0])
    for course in allOptionalCourseToClass:
        if (course[0] != id):
            id = course[0]
            finalCourseToClass.append(course)
    return finalCourseToClass


def fillClasses(finalCourseToClass, cursor, clock):
    for classroom in finalCourseToClass:
        # reduce students count from students table
        grade1 = classroom[6]
        cursor.execute("SELECT count FROM students WHERE grade LIKE '%s' " % grade1)
        count1 = cursor.fetchone()[0]
        count1 = count1 - classroom[7]
        cursor.execute("UPDATE students SET count= ? WHERE grade = ? ", (count1, grade1))
        dbConnection.commit()
        cursor.execute("SELECT * FROM students")

        # insert courses to classes
        course_id = classroom[4]
        time_left = classroom[9]
        cursor.execute("UPDATE classrooms SET current_course_id=?, current_course_time_left=? WHERE id =?",(course_id, time_left, classroom[0]))
        dbConnection.commit()
        cursor.execute("SELECT * FROM classrooms")

        text = "(%d) %s: %s is schedule to start" % (clock, classroom[1], classroom[5])
        print(text)


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def print_tables(cursor):
    cursor.execute("SELECT * FROM courses")
    print("courses")
    print_table(cursor.fetchall())
    cursor.execute("SELECT * FROM classrooms")
    print("classrooms")
    print_table(cursor.fetchall())
    cursor.execute("SELECT * FROM students")
    print("students")
    print_table(cursor.fetchall())

def fillClassesUpdateDataBase(clock):
    cursor.execute("SELECT * FROM classrooms as c JOIN courses ON c.id = courses.class_id WHERE current_course_time_left LIKE 0")
    # all classes free to be ocupied and courses for them.

    freeClassRooms = cursor.fetchall()
    if (len(freeClassRooms) != 0):
        finalCourseToClass = classesTOFill(freeClassRooms)
        fillClasses(finalCourseToClass, cursor, clock)

def process(cursor, clock):
    cursor.execute("SELECT * FROM classrooms")
    classroomsStat = cursor.fetchall()
    for classroom in classroomsStat:
        courseId = classroom[2]
        cursor.execute("SELECT current_course_time_left FROM classrooms WHERE current_course_id LIKE '%d'" % courseId)
        timeleft = cursor.fetchone()[0]
        cursor.execute("SELECT course_name FROM courses WHERE id LIKE '%d'" % courseId)
        coursenameTaple = cursor.fetchone()
        if(coursenameTaple is not None):
            coursename = coursenameTaple[0]
        if (courseId != 0 and clock != 0):
            if (timeleft == 1):
                text = "(%d) %s: %s is done" % (clock, classroom[1], coursename)
                print(text)
                cursor.execute("UPDATE classrooms SET current_course_id = (?) , current_course_time_left = (?) WHERE id = (?)", (0, 0, classroom[0]))

                cursor.execute("DELETE FROM courses WHERE id LIKE '%d'" % courseId)
                dbConnection.commit()
                fillClassesUpdateDataBase(clock)

            else:
                cursor.execute("SELECT current_course_time_left FROM classrooms WHERE current_course_id LIKE '%d'" % courseId)
                time_left = cursor.fetchone()[0]
                time_left = time_left - 1
                cursor.execute("""UPDATE classrooms SET current_course_time_left = ? WHERE current_course_id = ?""",
                               (time_left, courseId))
                dbConnection.commit()
                text = "(%d) %s: occupied by %s" % (clock, classroom[1], coursename)
                print(text)


def courses_table_size(cursor):
    cursor.execute("SELECT COUNT(id) FROM courses")
    i = cursor.fetchone()[0]
    return i


def main():
    clock = 0
    # take all the free classes and assgin them with courses
    fillClassesUpdateDataBase(clock)
    if (courses_table_size(cursor) != 0):
        while (courses_table_size(cursor) > 0):

            # all the logic of the program
            process(cursor, clock)

            # printing tables
            print_tables(cursor)

            clock = clock + 1
    else:
        print_tables(cursor)


if __name__ == '__main__':
    main()

dbConnection.close()