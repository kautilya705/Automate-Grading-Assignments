from canvasapi import Canvas

API_URL = 'https://canvas.instructure.com'
API_KEY = 'qMjGNOlFJsEQ2XeuertWk8NgpmFMlBXaGYSzDnACbG6FcbGyso6F5QL5DJDdmZLL'
canvas = Canvas(API_URL, API_KEY)

user = canvas.get_current_user()
for course in user.get_courses(enrollment_state='active'):
    print(f"Course ID: {course.id}, Course Name: {course.name}")
    
    assignments = course.get_assignments()
    for assignment in assignments:
        print(f"\tAssignment ID: {assignment.id}, Assignment Name: {assignment.name}")

for course in user.get_courses(enrollment_state='active'):
    print(f"\nCourse ID: {course.id}, Course Name: {course.name}")
    enrollments = course.get_enrollments(type=['StudentEnrollment'])
    for enrollment in enrollments:
        print(f"\tStudent ID: {enrollment.user_id}, Display Name: {enrollment.user['sortable_name']}")

def check_assignment_grades(course):
    """
    Prints out each assignment's grading status for a given course.
    """
    print(f"\nCourse ID: {course.id}, Course Name: {course.name}")

    assignments = course.get_assignments()
    for assignment in assignments:
        submissions = assignment.get_submissions()
        graded_count = 0
        for submission in submissions:
            if submission.workflow_state == 'graded':
                graded_count += 1
        print(f"\tAssignment ID: {assignment.id}, Assignment Name: {assignment.name}")

def main():
    for course in user.get_courses(enrollment_state='active'):
        check_assignment_grades(course)

        # Optionally, print enrolled students. Comment out if not needed.
        print(f"\nCourse ID: {course.id}, Course Name: {course.name}")
        enrollments = course.get_enrollments(type=['StudentEnrollment'])
        for enrollment in enrollments:
            print(f"\tStudent ID: {enrollment.user_id}, Display Name: {enrollment.user['sortable_name']}")

if __name__ == "__main__":
    main()
