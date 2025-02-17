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


def get_response_from_gemini(prompt: str) -> list:
    prompt = "Give AutoCAD commands to create " + prompt + """ Make sure to give only commands and nothing else. Format the comments in form of a list. \
        For example, if you have to draw a line starting at (0,0) and ending at (1,1), your list of commands should be: ['line', '0,0', '4,4', 'ESC']. \
        After that add this default list ['ZOOM', 'C', '0,0', '100'] do not miss any element in the default list. So your end output must be ['line', '0,0', '4,4','ESC', 'ZOOM', 'C', '0,0', '100']"""
    
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
    pyautogui.hotkey("alt", "tab", interval=0.2)
    time.sleep(3)  # Wait for AutoCAD to be in focus


def open_autocad():
    """
    Launches AutoCAD and waits until it is fully loaded.
    """
    print("Opening AutoCAD...")
    subprocess.Popen([AUTOCAD_PATH])
    time.sleep(15)
    print("AutoCAD should now be open.")
    new_button_image = '../agents/media/new_button.png' 
    print("Searching for the 'New' button on screen...")

    button_location = None
    for _ in range(10):
        button_location = pyautogui.locateOnScreen(new_button_image)
        if button_location is not None:
            break
        time.sleep(1)
    
    if button_location is None:
        print("Error: 'New' button not found. Please ensure the image is correct and visible on the screen.")
        return
    
    print(f"'New' button located at: {button_location}. Clicking it...")
    pyautogui.click(button_location)


def type_comment_in_autocad(comments: list):
    """
    Types the provided commands in AutoCAD.

    Args:
        comments (list): List of AutoCAD commands to type.
    """    

    time.sleep(3)
    print("Typing commands in AutoCAD...")
    for comment in comments:
        if comment.lower() == "esc":
            pyautogui.press('esc')
        else:
            pyautogui.write(comment, interval=0.7)
            print(comment)
            pyautogui.press('enter')



