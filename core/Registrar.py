import json
import os
import requests

class Registrar:
    def __init__(self, db_path="database/registry.json"):
        # ১. লোকাল ডেটাবেস পাথ সেটআপ
        self.db_path = db_path
        
        # ২. মাস্টার ক্লাউড কনফিগারেশন
        self.master_cloud_url = "https://root-d6v2.onrender.com/api/v1/sync-registry"
        self.auth_key = "Samrat_Omor_16_Year_Gift"

        # নিশ্চিত করা যে লোকাল ডিরেক্টরি এবং ফাইল আছে
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({}, f)

    def register(self, domain, target):
        """ডোমেইন রেজিস্ট্রি করা এবং মাস্টার ক্লাউডে সিঙ্ক করা"""
        try:
            # ৩. লোকাল ফাইলে ডেটা সেভ করা
            with open(self.db_path, 'r+') as f:
                data = json.load(f)
                data[domain] = {
                    "target": target, 
                    "status": "active",
                    "timestamp": "2026-03-14"
                }
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

            # ৪. মাস্টার ক্লাউডে ডেটা অমর (Immortalize) করা
            self.sync_to_master(data)
            
            return True
        except Exception as e:
            print(f"Error in Registrar: {str(e)}")
            return False

    def sync_to_master(self, registry_data):
        """মাস্টার ক্লাউডে জেসন পাঠানোর লজিক"""
        headers = {
            "X-Smriti-Key": self.auth_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                self.master_cloud_url, 
                json=registry_data, 
                headers=headers, 
                timeout=10
            )
            if response.status_code == 200:
                print("✅ Successfully Synced with Master Cloud!")
            else:
                print(f"⚠️ Master Cloud Sync Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection Error with Master Cloud: {str(e)}")