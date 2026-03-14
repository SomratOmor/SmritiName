import json
import os
import requests
from datetime import datetime

class Registrar:
    def __init__(self, db_path="database/registry.json"):
        # ১. লোকাল ডেটাবেস পাথ সেটআপ
        self.db_path = db_path
        
        # ২. মাস্টার ক্লাউড কনফিগারেশন
        # নিশ্চিত করো তোমার মাস্টার ক্লাউডের এই এন্ডপয়েন্টটি কাজ করছে
        self.master_cloud_url = "https://root-d6v2.onrender.com/api/v1/sync-registry"
        self.auth_key = os.getenv("MASTER_API_KEY", "Samrat_Omor_16_Year_Gift")

        # ফোল্ডার এবং ফাইল তৈরি নিশ্চিত করা
        dir_name = os.path.dirname(self.db_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({}, f)

    def register(self, domain, target):
        """ডোমেইন রেজিস্ট্রি করা এবং মাস্টার ক্লাউডে সিঙ্ক করা"""
        try:
            # ৩. ডাটা রিড করা
            data = {}
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}

            # নতুন ডোমেইন ডাটা যোগ করা
            data[domain] = {
                "target": target, 
                "status": "active",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # লোকাল ফাইলে সেভ করা
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=4)

            # ৪. মাস্টার ক্লাউডে ডাটা অমর (Immortalize) করা
            # আমরা আলাদা থ্রেড বা সরাসরি পাঠাতে পারি
            self.sync_to_master(data)
            
            return True
        except Exception as e:
            print(f"❌ Error in Registrar: {str(e)}")
            return False

    def sync_to_master(self, registry_data):
        """মাস্টার ক্লাউডে জেসন পাঠানোর লজিক"""
        headers = {
            "X-Smriti-Key": self.auth_key,
            "Content-Type": "application/json"
        }
        try:
            # এখানে registry_data সরাসরি পাঠানো হচ্ছে
            response = requests.post(
                self.master_cloud_url, 
                json=registry_data, 
                headers=headers, 
                timeout=10
            )
            if response.status_code == 200:
                print("✅ Successfully Synced with Master Cloud!")
            else:
                print(f"⚠️ Master Cloud Sync Failed Status: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Connection Error with Master Cloud: {str(e)}")

    def get_all_domains(self):
        """ড্যাশবোর্ডে দেখানোর জন্য সব ডোমেইন ডাটা রিড করা"""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}