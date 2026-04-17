[app]
title = SecureSync
package.name = securesync
package.domain = org.test.pro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.entrypoint = main.py
requirements = python3, kivy==2.3.0, requests, certifi, idna, urllib3, chardet
orientation = portrait
fullscreen = 0
[buildozer]
log_level = 2
warn_on_root = 1
