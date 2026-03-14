import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # ব্রাউজার কানেকশনের জন্য
from core.Registrar import Registrar

app = Flask(__name__, 
            template_folder="dashboard/templates", 
            static_folder="dashboard/static")

# এটি যোগ করলে ব্রাউজার থেকে বাটন টিপলে আর ব্লক করবে না
CORS(app)

registrar = Registrar()

# রেন্ডারের এনভায়রনমেন্ট ভেরিয়েবল থেকে কী রিড করবে
MASTER_KEY = os.getenv("MASTER_API_KEY", "Samrat_Omor_16_Year_Gift")

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/v1/register', methods=['POST'])
def register():
    # অথেন্টিকেশন চেক
    api_key = request.headers.get("X-Smriti-Key")
    if api_key != MASTER_KEY:
        return jsonify({"status": "error", "message": "Unauthorized Access"}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        domain = data.get("domain")
        target = data.get("target")

        if not domain or not target:
            return jsonify({"status": "error", "message": "Domain and Target are required"}), 400

        # ডোমেইন রেজিস্ট্রেশন শুরু
        success = registrar.register(domain, target)
        
        if success:
            return jsonify({
                "status": "success", 
                "message": f"Domain '{domain}' has been immortalized!",
                "sync": "Master Cloud Updated"
            }), 200
        else:
            return jsonify({"status": "error", "message": "Database write failed"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # রেন্ডার সাধারণত ৮0৮0 বা তার বেশি পোর্ট ব্যবহার করে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)