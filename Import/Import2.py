from github import Github 
import os 
import trio 
from github import Auth
import time 

auth = Auth.Token("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")
file = Github(auth = auth) #Github object. 
repo = file.get_repo("kautilya705/GradingAssignments") #Repo Name folled by the Grading LLM. 
base_directory = "/Users/kautilya/Desktop/Trying/RepoFiles2"

#Getting Files and directories 
def get_files(contents):
    files = []
    dirs = [] 
    for file_content in contents:
        if file_content.type == "dir":
            dirs.append(file_content)
        else:
            files.append(file_content)
    return files, dirs 




async def download_file(semaphore, file_content):
    async with semaphore:
        print(f"Downloading {file_content.path}...")
        file_path = os.path.join(base_directory, file_content.path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with await trio.open_file(file_path, 'wb') as file:
            await file.write(file_content.decoded_content)



#async def download_repo_files(repo, start_path="", semaphore=None):
    #contents = repo.get_contents(start_path)
    #async with trio.open_nursery() as nursery:
     #   for file_content in contents:
      #      if file_content.type == "dir":
       #         nursery.start_soon(download_repo_files, repo, file_content.path, semaphore)
        #    else:
         #       nursery.start_soon(download_file, nursery, semaphore, file_content)



async def download_repo_files(repo, start_path="", semaphore=None):
    contents = repo.get_contents(start_path)
    files, dirs = get_files(contents)
    
    async with trio.open_nursery() as nursery:
        for file_content in files:
            nursery.start_soon(download_file, semaphore, file_content)
        for dir_content in dirs:
            # Note: We ensure that the recursive calls are properly managed by awaiting them
            await download_repo_files(repo, dir_content.path, semaphore)



#Main Function 
async def main():
    start_time = time.time()
    Semaphore = trio.Semaphore(20)
    await download_repo_files(repo, semaphore=Semaphore)
    end_time = time.time()
    print(f"Time Taken: {end_time - start_time} seconds")

#Running with Trio 
trio.run(main)