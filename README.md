# AutoCAD AI Assistant

This project integrates Google Gemini AI with AutoCAD to generate and execute AutoCAD commands based on user input. It automates drawing creation by interpreting natural language prompts and simulating keystrokes.

[![ZenCAD Demo](https://i.ytimg.com/an_webp/2WH_bQJRVdQ/mqdefault_6s.webp?du=3000&sqp=CLjZj78G&rs=AOn4CLBclYv0gsgSBfB3iiiCEKxQ22J_Iw)](https://www.youtube.com/watch?v=2WH_bQJRVdQ)

## Features

- Generates AutoCAD commands using Gemini AI.
- Automates command execution in AutoCAD via `pyautogui`.
- Supports text, speech, and image input for drawing commands.
- Opens AutoCAD and creates a new drawing automatically.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/AutoCAD-AI-Assistant.git
    cd AutoCAD-AI-Assistant
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

### Running the Streamlit Web Interface

1. Start the Streamlit web interface:
    ```sh
    poetry run streamlit run [webpage.py](http://_vscodecontentref_/1)
    ```

2. Open your web browser and navigate to the provided URL (usually `http://localhost:8501`).

3. Follow the steps in the web interface to enter the AutoCAD path, describe your drawing, and generate commands.

### Running Tests

1. Run the test script to execute commands from the test list:
    ```sh
    poetry run python [test.py](http://_vscodecontentref_/2)
    ```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
