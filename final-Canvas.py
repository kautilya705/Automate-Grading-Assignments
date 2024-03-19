from canvasapi import Canvas
import concurrent.futures
from grades import grades_data # Assuming this is the format of grades.py
import time 


API_URL = "https://canvas.instructure.com"
API_KEY = "qMjGNOlFJsEQ2XeuertWk8NgpmFMlBXaGYSzDnACbG6FcbGyso6F5QL5DJDdmZLL"
COURSE_IDS = ['9017873', '9017881','9017883','9017887'] 

canvas = Canvas(API_URL, API_KEY)

def update_grade(grade_info):
    course_id = grade_info['course_id']
    assignment_id = grade_info['assignment_id']
    student_id = grade_info['student_id']
    grade = float(grade_info['grade'])
    try:
        course = canvas.get_course(course_id)
        assignment = course.get_assignment(assignment_id)
        submission = assignment.get_submission(student_id)
        updated_submission = submission.edit(submission={'posted_grade': grade})
        print(f"Updated {student_id} for assignment {assignment_id} in course {course_id} with grade {grade}")
        return updated_submission
    except Exception as e:
        print(f"Error updating grade for student {student_id} on assignment {assignment_id}: {e}")
        print(f"{assignment_id}, {grade},")
        return None

def submit_grades_concurrently(grades_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        # Submit all grade updates concurrently
        futures = [executor.submit(update_grade, grade_info) for grade_info in grades_data]
        
        # Optionally, process results as they become available
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            # Handle the result of each submission if needed



if __name__ == "__main__":
    start_time = time.time()
    submit_grades_concurrently(grades_data)
    end_time = time.time()
    difference = print(f"Time Difference is: {end_time-start_time}")

