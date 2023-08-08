from flask import Flask, request, render_template, send_file
import pandas as pd 
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html') 

@app.route('/process', methods=['POST'])
def process_csv():

    csv_file = request.files['file']
    df = pd.read_csv(csv_file)

    # Extract questions and answers
    df['Q&A'] = df['add_text'].apply(extract_qa)

    # Explode to rows
    qa_df = df['Q&A'].explode().apply(pd.Series)
    qa_df.columns = ['Question', 'Answer']

    # Convert to CSV
    csv_bytes = qa_df.to_csv().encode()

    # Return CSV file
    return send_file(
        io.BytesIO(csv_bytes), 
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename='processed.csv'
    )

def extract_qa(text):
    pattern = r'\[Q\d+\. (.*)\]\s+(.*)'
    return re.findall(pattern, text, re.DOTALL)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))