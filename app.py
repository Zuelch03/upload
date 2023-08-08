from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import re
import os

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
            result_file_path = 'result.csv'
            qna_df = pd.DataFrame(df['Q_and_A'].explode().tolist(), columns=[
                                  'Question', 'Response'])
            qna_df.to_csv(result_file_path, index=False)
            message = 'File processed successfully.'
        except KeyError:
            message = "The column 'add_text' was not found in the provided CSV file."

        return render_template('upload.html', message=message)

    return render_template('upload.html')

@app.route('/download')
def download_file():
    return send_from_directory(directory=os.getcwd(), filename="result.csv", as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
