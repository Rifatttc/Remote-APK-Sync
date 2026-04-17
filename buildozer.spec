[app]
title = SecureSync
package.name = securesync
package.domain = org.test.pro

# source files
source.dir = .
source.include_exts = py,png,jpg,kv

# version
version = 1.0

# requirements (clean & stable)
requirements = python3,kivy,requests

# app settings
orientation = portrait
fullscreen = 0

# =========================
# ANDROID CONFIG (IMPORTANT FIXED)
# =========================
android.api = 33
android.minapi = 21
android.ndk = 25b

# IMPORTANT: new correct format
android.archs = arm64-v8a

android.build_tools_version = 33.0.0

# permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# =========================
# BUILD SETTINGS
# =========================
log_level = 2
warn_on_root = 1

# =========================
# P4A (important for stability)
# =========================
p4a.branch = master
