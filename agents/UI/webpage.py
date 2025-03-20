import streamlit as st
from agents import react

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
    
    # Option to choose between text and speech input
    input_method = st.radio("Choose input method:", ("Text", "Speech"))
    
    user_command = ""
    if input_method == "Text":
        user_command = st.text_input("Enter your drawing request:")
    else:
        if st.button("Listening"):
            user_command = react.get_speech_input()
            st.text(f"Recognized speech: {user_command}")
            st.session_state["user_command"] = user_command
    if st.button("Generate and Execute"):
        if not st.session_state["AUTOCAD_PATH"]:
            st.error("AutoCAD path is required!")
        else:
            with st.spinner("Generating commands and checking AutoCAD..."):
                comment_to_type = react.get_response_from_gemini(st.session_state["user_command"])
                if not comment_to_type:
                    st.error("Failed to retrieve a response from Gemini.")
                else:
                    st.success("Commands generated successfully!")
                    st.write("**Generated Commands:**", comment_to_type)
                    
                    if react.is_autocad_running():
                        react.switch_to_autocad()
                    else:
                        react.open_autocad()
                    
                    react.type_comment_in_autocad(comment_to_type)
                    st.success("Operation complete.")
