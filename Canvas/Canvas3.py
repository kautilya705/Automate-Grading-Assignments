import random
from canvasapi import Canvas

# Canvas API URL and Key
API_URL = 'https://canvas.instructure.com'
API_KEY = 'qMjGNOlFJsEQ2XeuertWk8NgpmFMlBXaGYSzDnACbG6FcbGyso6F5QL5DJDdmZLL'  # Replace with your actual API key
canvas = Canvas(API_URL, API_KEY)

# Function to create assignments and collect their IDs
def create_assignments(course_ids, number_of_assignments=100):
    assignment_ids = []

    for course_id in course_ids:
        course = canvas.get_course(course_id)

        for _ in range(number_of_assignments):
            assignment = course.create_assignment({
                'name': 'Test Assignment',
                'points_possible': 100,
                'grading_type': 'points',
                'published': True
            })
            print(f"Created assignment {assignment.id} in course {course_id}")
            assignment_ids.append({'course_id': course_id, 'assignment_id': str(assignment.id)})

    return assignment_ids


def generate_grades_file(assignment_ids, file_name='gradesss.py'):
    with open(file_name, 'w') as file:
        file.write('grades = [\n')
        
        for entry in assignment_ids:
            for student_num in range(1, 6):  # Assuming 5 students per assignment for testing
                grade = random.randint(0, 100)
                line = (f"    {{'course_id': '{entry['course_id']}', "
                        f"'assignment_id': '{entry['assignment_id']}', "
                        f"'student_id': 'test_student_{student_num}', "
                        f"'grade': '{grade}'}},\n")
                file.write(line)
        
        file.write(']\n')

# Example usage
if __name__ == '__main__':
    # List your course IDs here
    course_ids = ['8666310', '8907172','8907185','8907192','8907199']
    
    # Create assignments in each course and collect their IDs
    assignment_ids = create_assignments(course_ids)
    
    # Generate grades.py file with random grades for the created assignments
    generate_grades_file(assignment_ids)
