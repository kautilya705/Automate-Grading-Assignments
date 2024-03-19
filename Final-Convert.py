import concurrent.futures
import os
import time 
import json 


system_prompt = "Please provide a cumulative score out of 100 for this C++ program. Do NOT breakdown the score or say anything. Just a number out of 100. Thats it. Your response should be this in this format: 35/100.Please do what I say."
def rubric(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    
        content = content.replace('\n', '\\n')
        content = content.replace('""','')
        return content 
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None 

def processsing(cpp_file_path):
    try:
        with open(cpp_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        critera = rubric('criteria.txt')
        content = system_prompt + "Code: " + content + "Criteria: " + critera
        # Prepare the string: escape quotes, backslashes, and insert newline characters
        content = content.replace('\\', '').replace('"', '').replace('\n', ' ').replace("'","")
        obj = {'role': 'user', 'content': content}
        # Return a formatted string representation of the file's contents
        return json.dumps(obj)
    except Exception as e:
        print(f"Error processing {cpp_file_path}: {e}")
        return None



def convert(cpp_files_dir, output_py_file):
    cpp_files = [os.path.join(cpp_files_dir, file) for file in os.listdir(cpp_files_dir) if file.endswith('.cpp')]
    
    # Same logic as importing files, but this time .map is used. 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        file_strings = list(executor.map(processsing, cpp_files))
    
    
    #Combining all strings into 1 big one!!!
    combined_string = ",\n".join(file_strings)

    # Converting the combining string to a python file. 
    with open(output_py_file, 'w', encoding='utf-8') as py_file:
        py_file.write(f"cpp_files_content = [{combined_string}\n]")

# Example usage
if __name__ == "__main__":
    start_time = time.time()
    cpp_files_dir = "/Users/kautilya/Desktop/Trying/RepoFiles3"
    output_py_file = "/Users/kautilya/Desktop/Trying/Assignments.py"
    convert(cpp_files_dir, output_py_file)
    end_time = time.time()
    print(f"Time Taken `is: {end_time-start_time}")


