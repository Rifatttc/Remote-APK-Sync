[app]
title = SecureSync
package.name = securesync
package.domain = org.test.pro

# source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# version
version = 1.0

# requirements (clean & stable)
requirements = python3,kivy==2.3.0,requests

# UI
orientation = portrait
fullscreen = 0

# Android settings (IMPORTANT FIXED)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a

# build tools (must match GitHub Actions)
android.build_tools_version = 33.0.0

# permissions (SAFE VERSION)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# build config
log_level = 2
warn_on_root = 1

# optional stability fixes
p4a.branch = master
