from flask import Flask, request, render_template
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
            message = 'File processed successfully. Download from '+result_file_path
        except KeyError:
            message = "The column 'add_text' was not found in the provided CSV file."

        return render_template('upload.html', message=message)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
