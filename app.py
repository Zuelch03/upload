from flask import Flask, request, render_template, redirect, url_for, send_file
import pandas as pd
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('process_csv'))

    return render_template('upload.html')

@app.route('/process') 
def process_csv():
    csv_file = request.files['file']
    df = pd.read_csv(csv_file)

    # Process CSV 
   
    csv_bytes = process_csv

    return send_file(csv_bytes)

def extract_qa(text):
   pattern = r'\[Q\d+\. (.*)\]\s+(.*)'
   return re.findall(pattern, text, re.DOTALL)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))