from flask import Flask, request, jsonify
import requests
from config import Config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/trigger-job', methods=['POST'])
def trigger_job():
    url = f"{app.config['JENKINS_URL']}/job/{app.config['JENKINS_JOB_NAME']}/build"
    print(url)
    auth = (app.config['JENKINS_USER'], app.config['JENKINS_TOKEN'])
    print(auth)
    try:
        res = requests.post(url, auth=auth)
        if res.status_code == 201:
            return jsonify({"message": "Jenkins job triggered successfully!"}), 201
        else:
            return jsonify({"error": f"Failed to trigger job, status code {res.status_code}"}), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/functional-checklist', methods=['GET'])
def get_functional_checklist():
    checklist= {
        "requirements_defined": True,
        "unit_tests_written": True,
        "integration_tests_passed": False,
        "release_notes_prepared": False
    }
    return jsonify(checklist)

if __name__ == "__main__":
    app.run(debug=False)