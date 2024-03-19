import concurrent.futures
import os

# Define the prompt that should precede each code snippet in the string format
system_prompt = "Please provide a cumulative score out of 100 for this C++ program. Do NOT breakdown the score or say anything. Just a number out of 100. That's it. Your response should be this in this format: 35/100.Please do what I say."

def process_file(file_path, criteria):
    """
    Reads the content of a given file, removes new lines, backslashes, single quotes,
    and internal double quotes, then formats it with the system prompt and criteria into a single line string.
    """
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace new lines with a space, remove backslashes, single quotes, and internal double quotes
        content_cleaned = content.replace('\n', ' ').replace('\\', '').replace('\'', '').replace('"', '')

        # Format the full content with system prompt and criteria
        full_content = f"{system_prompt} {content_cleaned} {criteria}"

        return full_content
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def convert_to_single_string(cpp_files_dir, criteria_text, output_file):
    # List all C++ files in the directory
    cpp_files = [os.path.join(cpp_files_dir, f) for f in os.listdir(cpp_files_dir) if f.endswith('.cpp')]

    # Process files concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Define a partial function application to include criteria for each file processing
        formatted_strings = list(executor.map(lambda f: process_file(f, criteria_text), cpp_files))

    # Combine all formatted strings into one, remove internal double quotes, and enclose in double quotes
    combined_string = ", ".join(filter(None, formatted_strings))  # Filter out any failed processing attempts
    final_output = f'"{combined_string}"'

    # Write the final output to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_output)

# Example usage
if __name__ == "__main__":
    cpp_files_dir = "/Users/kautilya/Desktop/Trying/Testingg"
    criteria_file = "/Users/kautilya/Desktop/Trying/criteria.txt"
    output_file = "/Users/kautilya/Desktop/Trying/Assignments.py"
    # Convert and write to file
    convert_to_single_string(cpp_files_dir, criteria_file, output_file)

