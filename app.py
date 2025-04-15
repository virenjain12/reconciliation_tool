import os
import traceback
import json
from flask import Flask, request, jsonify, send_file, render_template
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from extractor import extract_text_from_pdf
from gpt_parser import extract_data_with_gpt
from reconciler import save_to_excel

load_dotenv()
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/upload', methods=['POST'])
def upload_files():
    po_files = request.files.getlist("po_files")
    invoice_files = request.files.getlist("invoice_files")

    if not po_files and not invoice_files:
        return jsonify({"error": "No files uploaded"}), 400

    try:
        for file in po_files:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            parsed = json.loads(extract_data_with_gpt(text))
            save_to_excel(parsed)

        for file in invoice_files:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            parsed = json.loads(extract_data_with_gpt(text))
            save_to_excel(parsed)

        return send_file("output/reconciliation_report.xlsx", as_attachment=True)

    except Exception as e:
        print("ERROR:", str(e)) 
        return jsonify({"error": str(e)}), 500

@app.route('/download-report')
def download_report():
    return send_file("output/reconciliation_report.xlsx", as_attachment=True)

@app.route("/tool")
def tool():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
