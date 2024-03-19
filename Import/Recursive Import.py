from github import Github
from github import Auth
import os
import time 

start_time = time.time() 
auth = Auth.Token("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")
file = Github(auth = auth) #Github object. 


repo = file.get_repo("kautilya705/GradingAssignments") #Repo Name folled by the Grading LLM. 
contents = repo.get_contents("")
base_directory = "/Users/kautilya/Desktop/Trying/RepoFiles"

#Recursively Downloading Files from 1 repository 
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        # If the content is a directory, extend the contents list with the contents of that directory
        contents.extend(repo.get_contents(file_content.path))
    else:
        print(f"Downloading {file_content.path}...")

        # Construct the full local file path
        file_path = os.path.join(base_directory, file_content.path)

        # Create the local directory structure if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Download and write the file content
        with open(file_path, 'wb') as file:
            file.write(file_content.decoded_content)

end_time = time.time()


total_time = end_time - start_time
print(f"Total Time Taken: {total_time}")
