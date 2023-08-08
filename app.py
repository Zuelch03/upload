from flask import Flask, request, send_file
import pandas as pd
import re

app = Flask(__name__)

@app.route('/process', methods=['POST'])  
def process_csv():

  file = request.files['file']
  
  df = pd.read_csv(file)

  # Extract questions and responses
  df['Q&A'] = df['add_text'].apply(extract_qa)
  
  # Explode list to rows
  qa_df = df['Q&A'].explode().apply(pd.Series) 
  qa_df.columns = ['Question', 'Response']

  # Convert DataFrame to CSV bytes
  csv_bytes = qa_df.to_csv().encode()
  
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