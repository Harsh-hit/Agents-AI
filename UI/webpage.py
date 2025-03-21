import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
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
    
    uploaded_image = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg"])

    st.header("Or Draw Your Image")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        update_streamlit=True,
        height=300,
        width=300,
        drawing_mode="freedraw",
        key="canvas",
    )

    user_command = ""
    if input_method == "Text":
        st.session_state["user_command"] = st.text_input("Enter your drawing request:")
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
                if uploaded_image:
                    comment_to_type = react.image_response_from_gemini(st.session_state["user_command"], uploaded_image)
                elif canvas_result.image_data is not None:
                    # Save the drawn image to a temporary file
                    image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                    temp_image_path = "temp_drawn_image.png"
                    image.save(temp_image_path)
                    comment_to_type = react.image_response_from_gemini(st.session_state["user_command"], temp_image_path)
                else:
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
