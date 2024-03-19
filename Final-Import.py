from github import Github
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Constants
GITHUB_TOKEN = "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"
REPO_NAME = "kautilya705/GradingAssignments"
BASE_DIRECTORY = "/Users/kautilya/Desktop/Trying/RepoFiles3"

gh = Github(GITHUB_TOKEN)  # GitHub Object
repo = gh.get_repo(REPO_NAME)

def download_and_delete_file(file_content):
    print(f"Downloading and scheduling deletion for {file_content.path}...")
    file_path = os.path.join(BASE_DIRECTORY, file_content.path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Converts from binary data to actual code.
    content = file_content.decoded_content
    with open(file_path, 'wb') as file:
        file.write(content)
    # Attempt to delete the file, retry once if SHA mismatch occurs
    delete_attempts = 20
    for attempt in range(delete_attempts):
        try:
            # Fetch the latest SHA in case it has changed
            latest_file_content = repo.get_contents(file_content.path)
            repo.delete_file(file_content.path, "Delete file via script", latest_file_content.sha, branch="main")
            print(f"Deleted {file_content.path}")
            break  # Exit the loop if deletion was successful
        except Exception as e:
            if attempt < delete_attempts - 1:  # Before the last attempt, just print the error
                print(f"Error deleting {file_content.path}, retrying...: {e}")
            else:  # On the last attempt, give up and print the error
                print(f"Error deleting {file_content.path}: {e}")


def get_files(repo, path=""):
    """List all files in the repository recursively."""
    file_contents = []
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == "dir":
            file_contents.extend(get_files(repo, content.path))
        else:
            file_contents.append(content)
    return file_contents


def main():
    start_time = time.time()

    # List all files in the repository
    file_contents = get_files(repo)

    # Download all files and schedule them for deletion using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=55) as executor:  # Adjusted max_workers to a more conservative number
        future_to_file = {executor.submit(download_and_delete_file, content): content for content in file_contents}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{file.path} generated an exception: {exc}')
    
    end_time = time.time()
    print(f"Time Taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
