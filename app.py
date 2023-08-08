from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import re
import os
import tempfile

app = Flask(__name__)

def extract_qa(text):
    pattern = r'\[Q\d+\. (.*?)\]\s(.*?)(?=\s\[Q\d| $)'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)

        try:
            df['Q_and_A'] = df['add_text'].apply(extract_qa)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                qna_df = pd.DataFrame(df['Q_and_A'].explode().tolist(), columns=['Question', 'Response'])
                qna_df.to_csv(temp_file.name, index=False)
                temp_file_path = temp_file.name

            message = f'File processed successfully. <a href="/download?filename={os.path.basename(temp_file_path)}">Download result.csv</a>'
        except KeyError:
            message = "The column 'add_text' was not found in the provided CSV file."

        return render_template('upload.html', message=message)

    return render_template('upload.html')

@app.route('/download')
def download_file():
    filename = request.args.get('filename', '')
    if filename:
        try:
            return send_from_directory(directory=tempfile.gettempdir(), filename=filename, as_attachment=True, download_name="result.csv")
        except FileNotFoundError:
            return "File not found."
    else:
        return "Invalid request."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)