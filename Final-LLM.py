import re
from Assignments import cpp_files_content
import concurrent.futures
import time
import json
import ollama

def extract_ids_and_grade(prompt, response):
    # Adjust regular expressions to correctly match the provided prompt format
    course_id_match = re.search(r"//courseid:(\d+)", prompt['content'])
    assignment_id_match = re.search(r"//assignmentid:(\d+)", prompt['content'])
    student_id_match = re.search(r"//studentid:(\d+)", prompt['content'])
    grade_match = re.search(r"(\d+)/100", response)

    # Extract matched values, or default to an empty string if not found
    course_id = course_id_match.group(1) if course_id_match else ""
    assignment_id = assignment_id_match.group(1) if assignment_id_match else ""
    student_id = student_id_match.group(1) if student_id_match else ""
    grade = grade_match.group(1) if grade_match else ""

    return {
        "course_id": course_id,
        "assignment_id": assignment_id,
        "student_id": student_id,
        "grade": grade
    }

def sending(prompt):
    try:
        # Send the prompt to the Ollama API and receive the response
        response = ollama.chat(model='mistral', messages=[prompt])
        # Process the response to extract the desired information
        processed_info = extract_ids_and_grade(prompt, response['message']['content'])
        return processed_info
    except Exception as e:
        print(f"Error sending prompt: {e}")
        return None

def concurrency(prompts, max_workers=50, sleep_time=1.00):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_prompt = {executor.submit(sending, prompt): prompt for prompt in prompts}
        for future in concurrent.futures.as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error processing prompt {prompt['content']}: {e}")
            time.sleep(sleep_time)  # Respect the rate limit

    # Write the results to a Python file
    with open('grades.py', 'w') as f:
        f.write(f"grades_data = {json.dumps(results, indent=4)}")

if __name__ == "__main__":
    start_time = time.time()
    concurrency(cpp_files_content, max_workers=50)  # Adjust max_workers as needed
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
