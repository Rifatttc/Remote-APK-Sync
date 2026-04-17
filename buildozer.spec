[app]
title = SecureSync
package.name = securesync
package.domain = org.test.pro

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0

# Android config
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
android.build_tools_version = 33.0.0

# Permissions (safe)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# stability
log_level = 2
warn_on_root = 1

[p4a]
branch = master
