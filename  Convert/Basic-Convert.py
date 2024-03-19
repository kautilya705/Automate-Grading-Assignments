import json
#Each object is defined with course Id and student Id 
#Object: {" "}, This is the problem.
#Rubric: {""}, extracted from a file. 
#System Prompt Prompt: {""}
#formatted input: System Prompt + Object + Rubric

system_prompt = "You are a grader responsible for grading programming projects based on a particular rubric. Grade the following programming assignment based on the rubric given. For each rubric, maximum points are given. Only provide the points awarded for each criteria along with the total, which is out of 100. Do not provide written feedback."
#File Path 
cpp = 'A1 copy 30.cpp'
json_file_path = 'grades.jsonl'

#Reading 
with open(cpp, 'r') as cpp_file:
    cpp_content = cpp_file.read()

full_content = system_prompt + "\n" + cpp_content

json_object = {"Solution by student": full_content}
json_str = json.dumps(json_object)
json_line = json_str + "\n"

#Writing a json object 
with open(json_file_path, 'w') as jsonl_file:
    jsonl_file.write(json_line)


print("Conversion Done. Check")