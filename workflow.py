import subprocess
import time 
import shutil
import os 


def run_script(script_path):
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Output of {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error in {script_path}:\n{e.stderr}")
        raise


def delete_everything(files, directory):
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted {file}")
        except OSError as e:
            print(f"Error deleting {file}: {e.strerror}")
    
    # Delete directory and all its contents
    try:
        shutil.rmtree(directory)
        print(f"Deleted directory {directory}")
    except OSError as e:
        print(f"Error deleting directory {directory}: {e.strerror}")



if __name__ == "__main__":
    start_time = time.time()
    print("Starting workflow...")
    
    # Step 1: Run Final-Import.py
    print("Importing files.... ")
    run_script('/Users/kautilya/Desktop/Trying/Final-Import.py')
    
    print("Creating Assignments......")
    # Step 2: Run Final-Convert.py (which creates Assignment.py)
    run_script('/Users/kautilya/Desktop/Trying/Final-Convert.py')
    
    print("Sending Stuff to LLM........")
    # Step 3: Run Final-LLM.py (which uses Assignment.py and creates grades.py)
    run_script('/Users/kautilya/Desktop/Trying/Final-LLM.py')
    print("Grades file has been created!")

    print("Sending Grades to Canvas.......")
    # Step 4: Run final-Canvas.py (which uses grades.py)
    run_script('/Users/kautilya/Desktop/Trying/final-Canvas.py')
    
    print("Workflow completed.")
    end_time = time.time()
    print(f"Time taken is: {end_time - start_time}")

    files_to_delete = ['/Users/kautilya/Desktop/Trying/grades.py', '/Users/kautilya/Desktop/Trying/Assignments.py']
    directory_to_delete = '/Users/kautilya/Desktop/Trying/RepoFiles3'
    delete_everything(files_to_delete, directory_to_delete)