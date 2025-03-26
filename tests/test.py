from agents import react
import re

with open("./tests/test_list.txt", "r") as f:
    test_list = f.read()
    
lines = test_list.split("\n")
cleaned_lines = [re.sub(r"^\d+\.\s*", "", line) for line in lines]
for user_command in cleaned_lines:
    comment_to_type = react.get_response_from_gemini(user_command)
    print("running for command ", user_command)
    if react.is_autocad_running():
        react.test_type_comment_in_autocad(comment_to_type)
    else:
        react.open_autocad()
        react.test_type_comment_in_autocad(comment_to_type)

