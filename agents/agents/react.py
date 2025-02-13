import subprocess
import streamlit as st
import os
import time
import pyautogui
import psutil
import google.generativeai as genai
import ast
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

AUTOCAD_PATH = r"C:/Program Files/Autodesk/AutoCAD 2025/acad.exe"


def parse_string_to_list(input_str):
    try:
        input_str = input_str.strip("`\n")
        parsed_list = ast.literal_eval(input_str)
        return parsed_list
    except (SyntaxError, ValueError):
        return []


def get_response_from_gemini(model: genai.GenerativeModel, prompt: str) -> list:
    prompt = "Give AutoCAD commands to create " + prompt + """ Make sure to give only commands and nothing else. Format the comments in form of a list. \
        For example, if you have to draw a line starting at (0,0) and ending at (1,1), your list of commands should be: ['line', '0,0', '4,4', 'ENTER']. \
        After that add this default list ['ZOOM', 'C', '0,0', '100'] do not miss any element in the default list. So your end output must be ['line', '0,0', '4,4', 'ENTER', 'ZOOM', 'C', '0,0', '100']"""
    
    response = model.generate_content(prompt)
    result = parse_string_to_list(response.text)
    print(result)
    return result


def is_autocad_running():
    """
    Checks if an AutoCAD process is currently running.
    
    Returns:
        bool: True if AutoCAD is running, False otherwise.
    """
    for process in psutil.process_iter(attrs=['name']):
        if "acad.exe" in process.info['name'].lower():
            return True
    return False


def switch_to_autocad():
    """
    Brings the active AutoCAD window to the foreground.
    """
    print("Bringing AutoCAD to the front...")
    pyautogui.hotkey("alt", "tab")
    time.sleep(3)  # Wait for AutoCAD to be in focus


def open_autocad():
    """
    Launches AutoCAD and waits until it is fully loaded.
    """
    print("Opening AutoCAD...")
    subprocess.Popen([AUTOCAD_PATH])
    time.sleep(20)
    print("AutoCAD should now be open.")


def type_comment_in_autocad(comments: list):
    """
    Types the provided commands in AutoCAD.

    Args:
        comments (list): List of AutoCAD commands to type.
    """

    print("Typing commands in AutoCAD...")
    for comment in comments:
        if comment.lower() == "enter":
            pyautogui.press('enter')
        else:
            pyautogui.write(comment, interval=0.7)
            print(comment)
            pyautogui.press('enter')


def main():
    user_command = input("Enter your command for the AI agent: ")

    comment_to_type = get_response_from_gemini(model, user_command)
    if not comment_to_type:
        print("Failed to retrieve a response from Gemini. Exiting.")
        return

    print("Gemini response:", comment_to_type)

    if is_autocad_running():
        print("AutoCAD is already open. Switching to the window...")
        switch_to_autocad()
    else:
        open_autocad()

    type_comment_in_autocad(comment_to_type)
    print("Operation complete.")


st.title("AI-Powered AutoCAD Drawing Assistant")

if "AUTOCAD_PATH" not in st.session_state:
    st.session_state["AUTOCAD_PATH"] = ""

if "step" not in st.session_state:
    st.session_state["step"] = "autocad_path"

if st.session_state["step"] == "autocad_path":
    st.header("Step 1: Enter AutoCAD Path")
    autocad_path = st.text_input("Enter the full path to AutoCAD executable:", 
                                 value=st.session_state["AUTOCAD_PATH"])
    if st.button("Next"):
        st.session_state["AUTOCAD_PATH"] = autocad_path
        st.session_state["step"] = "drawing_command"
        st.rerun()

elif st.session_state["step"] == "drawing_command":
    st.header("Step 2: Describe What You Want to Draw")
    user_command = st.text_input("Enter your drawing request:")
    if st.button("Generate and Execute"):
        if not st.session_state["AUTOCAD_PATH"]:
            st.error("AutoCAD path is required!")
        else:
            with st.spinner("Generating commands and checking AutoCAD..."):
                comment_to_type = get_response_from_gemini(model, user_command)
                if not comment_to_type:
                    st.error("Failed to retrieve a response from Gemini.")
                else:
                    st.success("Commands generated successfully!")
                    st.write("**Generated Commands:**", comment_to_type)
                    
                    if is_autocad_running():
                        switch_to_autocad()
                    else:
                        open_autocad()
                    
                    type_comment_in_autocad(comment_to_type)
                    st.success("Operation complete.")
