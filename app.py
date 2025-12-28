from flask import Flask, render_template, request, send_file
from core.ingestor import parse_scan_data
from core.brain import analyze_vulnerability, generate_attack_path_summary # <-- IMPORT NEW FUNCTION
from core.reporter import generate_report
from core.analytics import create_severity_chart # <-- IMPORT NEW FUNCTION
import os

app = Flask(__name__)

# Force No-Cache (Keep this from before)
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Ingestion
        findings = parse_scan_data("data/input/sample.xml")
        client_context = request.form.get('context', 'Standard Corporate Network')

        # --- FEATURE 2: GENERATE CHART ---
        chart_path = create_severity_chart(findings)
        
        # --- FEATURE 5: ATTACK PATH SUMMARY ---
        # We generate this ONCE for the whole report
        holistic_summary = generate_attack_path_summary(findings, client_context)
        
        # 2. Individual Analysis
        analyses = []
        try:
            for finding in findings:
                analysis = analyze_vulnerability(finding, client_context)
                analyses.append(analysis)
        except:
            analyses = ["AI Offline: Analysis Failed"] * len(findings)
            
        # 3. Generation (Pass new data to reporter)
        report_path = generate_report(
            findings, 
            analyses, 
            chart_path=chart_path, 
            attack_path_summary=holistic_summary
        )
        
        return render_template('index.html', message="Report Generated Successfully!", pdf_link=report_path)

    return render_template('index.html')

# ... (Rest of your app.py routes) ...
# --- MISSING DOWNLOAD ROUTE ---
@app.route('/data/output/<filename>')
def download_file(filename):
    # This tells Flask exactly where to find the PDF on your computer
    file_path = os.path.join(os.getcwd(), 'data', 'output', filename)
    return send_file(file_path, as_attachment=True)
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)