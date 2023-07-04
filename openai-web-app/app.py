from flask import Flask, render_template, request, jsonify
from flask_sockets import Sockets
from openai import ChatCompletion
from werkzeug.utils import secure_filename
import docx2txt
import PyPDF2

from azure.identity import DefaultAzureCredential
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



# Set up your OpenAI API key
openai.api_key = 'your_openai_api_key'


# Initialize Flask app and WebSocket support
app = Flask(__name__)
sockets = Sockets(app)

# Serve the HTML template for the web app
@app.route('/')
def index():
    return render_template('index.html')

# Handle messages via HTTP POST request
@app.route('/send-message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        response = process_message(message)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'No message provided'})

# Process the received message and generate a response using ChatGPT
def process_message(message):
    
    print(message)
    
    
    completion = openai.Completion.create(
             engine="text-davinci-003", # gpt-3.5-turbo, text-davinci-002
             prompt=message,
             temperature=0.5,
             max_tokens=1024,
             n = 1,
             stop=None
        )
    
    
    reply = completion.choices[0]['text'].strip()
    
    print(reply)
    
    return reply


# Handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # print(file_path + " was uploaded")
        summary = summarize_document(file_path)
        return jsonify({'summary': summary})

    return jsonify({'error': 'Invalid file type'})

# Summarize the uploaded document using the OpenAI API
def summarize_document(file_path):
    if "pdf" in file_path:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            document_text = ''
            for page_number in range(len(reader.pages)):
                page_obj = reader.pages[page_number]
                document_text += page_obj.extract_text()
            
    elif "docx" in file_path:
        document_text = docx2txt.process(file_path)
    
    
    # print(document_text)
    
    
    completion = openai.Completion.create(
            engine="text-davinci-003", # gpt-3.5-turbo, text-davinci-002
            prompt=(f"Please summarize the following text:\n{document_text}\n\nSummary:"),
            temperature=0.5,
            max_tokens=1024,
            n = 1,
            stop=None
        )
    
    
    summary = completion.choices[0]['text'].strip()
    
    print(summary)
    
    return summary

# Check if the file extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
