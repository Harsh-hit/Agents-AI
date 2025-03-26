import subprocess
import os
import time
import pyautogui
import psutil
import google.generativeai as genai
import ast
import speech_recognition as sr 
import PIL.Image
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
    prompt = f"""
    **Description:**
    Generate a sequence of AutoCAD commands to create a specified object. The response should only
    include AutoCAD commands without any additional text or explanations. The commands should be,
    formatted as a list, with a specific structure and A default list of commands `['ZOOM', 'C', '0,0', '100']` 
    must always be appended at the end of the 
    generated command sequence.
    
    **Question:**
    draw a line from `(0,0)` to `(1,1)` and then a line from `(1,1)` to `(2,2)`
    
    **Reasoning:**
    1. First 'line' command is used, then starting point is specified '0,0' and ending point is specified '1,1'.
    2. Next endpoint is '2,2', it is at distance 1 from x and 1 from y of the previous endpoint. So the final endpoint is '1,1'.
    3. The command 'ESC' is used to exit the line drawing mode.
    4. A default list of commands `['ZOOM', 'C', '0,0', '100']` must always be appended at the end of the 
    generated command sequence.
    5. The expected output should be:
       ```
       ['line', '0,0', '1,1', '1,1', 'ESC', 'ZOOM', 'C', '0,0', '100']
       ```
    
    **Output:**
    A Python list containing the AutoCAD commands, strictly formatted as described.

    Now, generate AutoCAD commands for: {prompt}
    """
    
    response = model.generate_content(prompt)
    result = parse_string_to_list(response.text)
    print(result)
    return result

def image_response_from_gemini(prompt: str, image_path:str) -> list:
    prompt = f"""
    **Description:**
    Use the image as a reference and Generate a sequence of AutoCAD commands to create a specified object. The response should only
    include AutoCAD commands without any additional text or explanations. The commands should be,
    formatted as a list, with a specific structure and A default list of commands `['ZOOM', 'C', '0,0', '100']` 
    must always be appended at the end of the 
    generated command sequence.
    
    **Question:**
    draw a line from `(0,0)` to `(1,1)` and then a line from `(1,1)` to `(2,2)`
    
    **Reasoning:**
    1. First 'line' command is used, then starting point is specified '0,0' and ending point is specified '1,1'.
    2. Next endpoint is '2,2', it is at distance 1 from x and 1 from y of the previous endpoint. So the final endpoint is '1,1'.
    3. The command 'ESC' is used to exit the line drawing mode.
    4. A default list of commands `['ZOOM', 'C', '0,0', '100']` must always be appended at the end of the 
    generated command sequence.
    5. The expected output should be:
       ```
       ['line', '0,0', '1,1', '1,1', 'ESC', 'ZOOM', 'C', '0,0', '100']
       ```
    
    **Output:**
    A Python list containing the AutoCAD commands, strictly formatted as described.

    Now, generate AutoCAD commands for: {prompt}
    """
    image = PIL.Image.open(image_path)
    response = model.generate_content(contents=[prompt, image])
    result = parse_string_to_list(response.text)
    print(result)
    return result

def get_speech_input() -> str:
    """
    Captures speech input from the user and converts it to text.

    Returns:
        str: The recognized speech as text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""


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
    time.sleep(1)
    pyautogui.hotkey("alt", "tab", interval=0.2)
    time.sleep(3)  # Wait for AutoCAD to be in focus


def open_autocad():
    """
    Launches AutoCAD and waits until it is fully loaded.
    """
    print("Opening AutoCAD...")
    subprocess.Popen([AUTOCAD_PATH])
    time.sleep(20)
    print("AutoCAD should now be open.")
    new_button_image = './media/new_button.png' 
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


def type_comment_in_autocad(comments: list[str]):
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
            pyautogui.write(comment, interval=0.5)
            print(comment)
            pyautogui.press('enter')



def test_type_comment_in_autocad(comments: list[str]):
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
    
    time.sleep(1)
    pyautogui.hotkey("ctrl", "n")
    time.sleep(1)
    pyautogui.hotkey('enter')