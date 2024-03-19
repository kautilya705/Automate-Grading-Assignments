from Assignments import cpp_files_content
import concurrent.futures
import time
import json
import ollama

def sending(prompt):
    try:
        # Correctly format the messages argument as expected by the Ollama API
        response = ollama.chat(model='mistral', messages=[prompt])
        # Assuming the response structure fits this pattern
        return response['message']['content']
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
                results.append({'prompt': prompt, 'response': result})
            except Exception as e:
                print(f"Error processing prompt {prompt['content']}: {e}")
            time.sleep(sleep_time)  # Respect the rate limit

    # Write the results to a Python file
    with open('grades.py', 'w') as f:
        f.write(f"grades_data = {json.dumps(results, indent=4)}")

if __name__ == "__main__":
    start_time = time.time()
    # Ensure cpp_files_content is a list of dictionaries formatted as required by the Ollama API
    concurrency(cpp_files_content, max_workers=50)  # Adjust max_workers as needed
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
