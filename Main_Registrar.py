from flask import Flask, request, jsonify, render_template
import os
from core.Registrar import Registrar

app = Flask(__name__, 
            template_folder='dashboard/templates', 
            static_folder='dashboard/static')

# তোমার সেই ১৬ বছরের সিক্রেট কি
MASTER_KEY = "Samrat_Omor_16_Year_Gift"
reg = Registrar()

@app.route('/')
def index():
    """ডোমেইন ম্যানেজমেন্ট ড্যাশবোর্ড"""
    return render_template('index.html')

@app.route('/api/v1/register', methods=['POST'])
def register_domain():
    """নতুন ডোমেইন রেজিস্ট্রি এবং মাস্টার ক্লাউডে সিঙ্ক করার এন্ডপয়েন্ট"""
    data = request.json
    incoming_key = request.headers.get('X-Smriti-Key')

    # ১. সিকিউরিটি চেক
    if incoming_key != MASTER_KEY:
        return jsonify({"status": "failed", "message": "Unauthorized"}), 401

    if not data or 'domain' not in data or 'target' not in data:
        return jsonify({"status": "failed", "message": "Invalid Data"}), 400

    domain = data.get('domain')
    target = data.get('target')

    # ২. Registrar-এর মাধ্যমে লোকাল এবং ক্লাউড সিঙ্ক করা
    success = reg.register(domain, target)

    if success:
        return jsonify({
            "status": "success",
            "message": f"Domain {domain} registered and synced to Master Cloud!",
            "domain": domain
        })
    else:
        return jsonify({"status": "failed", "message": "Sync failed"}), 500

@app.route('/api/v1/resolve', methods=['GET'])
def resolve():
    """ডোমেইন কানেকশন ভেরিফিকেশন"""
    host = request.host.lower()
    return jsonify({
        "status": "connected", 
        "resolved_host": host,
        "system": "SmritiName Engine"
    })

if __name__ == "__main__":
    # রেন্ডার অটোমেটিক পোর্ট ভেরিয়েবল দেয়, অন্যথায় ৮০৮০ ব্যবহার হবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)