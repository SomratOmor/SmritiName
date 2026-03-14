import os
import json
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from core.Registrar import Registrar

app = Flask(__name__, 
            template_folder="dashboard/templates", 
            static_folder="dashboard/static")

# বাইরের এপিআই কল সাপোর্ট করার জন্য CORS
CORS(app)

registrar = Registrar()

# মাস্টার কী (নিরাপত্তার জন্য)
MASTER_KEY = os.getenv("MASTER_API_KEY", "Samrat_Omor_16_Year_Gift")

# --- ১৬ বছরের স্বপ্নের ডোমেইন ইঞ্জিন লজিক ---
@app.before_request
def dns_routing_engine():
    """
    এটিই তোমার ইঞ্জিনের আসল 'মস্তিষ্ক'। 
    ব্রাউজারে যে ডোমেইনই লেখা হোক, এই ফাংশন সেটাকে ক্যাচ করবে।
    """
    host = request.host.lower().replace('www.', '')
    
    # তোমার মেইন ইঞ্জিন ইউআরএল (যাতে লুপ না হয়)
    engine_url = "https://root-d6v2.onrender.com"
    
    # যদি রিকোয়েস্টটি ডোমেইন নাম দিয়ে আসে (যেমন smriti.cloud)
    if host != engine_url and not host.startswith('localhost'):
        all_domains = registrar.get_all_domains()
        
        if host in all_domains:
            target_link = all_domains[host]["target"]
            # সরাসরি রিডাইরেক্ট - এটাই হলো রেজোলিউশন
            return redirect(target_link, code=301)

# --- ড্যাশবোর্ড রুট ---
@app.route('/')
def home():
    return render_template('index.html')

# --- রেজোলিউশন এপিআই (GET) ---
@app.route('/api/v1/resolve', methods=['GET'])
def resolve():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"status": "error", "message": "Missing domain"}), 400
    
    all_data = registrar.get_all_domains()
    if domain in all_data:
        return jsonify({
            "status": "success", 
            "domain": domain, 
            "target": all_data[domain]["target"]
        }), 200
    return jsonify({"status": "error", "message": "Domain not registered"}), 404

# --- রেজিস্ট্রেশন এপিআই (POST) ---
@app.route('/api/v1/register', methods=['POST'])
def register():
    api_key = request.headers.get("X-Smriti-Key")
    if api_key != MASTER_KEY:
        return jsonify({"status": "error", "message": "Unauthorized Access"}), 401

    try:
        data = request.get_json()
        domain = data.get("domain").lower().replace('www.', '')
        target = data.get("target")

        if registrar.register(domain, target):
            return jsonify({
                "status": "success", 
                "message": f"'{domain}' is now live on your engine!"
            }), 200
        return jsonify({"status": "error", "message": "Storage error"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- হেলথ চেক (গ্লোবাল গেটওয়ের জন্য) ---
@app.route('/healthz')
def health():
    return "Smriti Engine Online", 200

if __name__ == '__main__':
    # রেন্ডারের পোর্টে রান করা
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)