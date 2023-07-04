# OpenAI

App was developed using Python's 3.9.11 version. Instructions to run the app:

1. Go to the directory named  `openai-web-app`.
2. Setup your python environment using `requirements.txt` file.
3. Please provide your own OpenAI api key in `app.py` file.
4. To start the app use `python app.py`  in the console opened from the project directory.
5. Go to `http://localhost:5000/` url, and you will see the web app is there. Default port for the Flask might be different on your machine, or `port 5000` can be used by other processes. Make sure that you use the port which is not occupied.
6. To chat, just type your question and press `Send`.
7. To summarize the text from a file, `Choose File` and then press `Upload`. Currently, `pdf` and `docx` files are supported only.
8. You can also consider looking at console output, sent and received messages are printed, generated summaries are also printed there.
