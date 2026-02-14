import os

from .is_badge import is_badge

if is_badge():
    apps = os.listdir("/apps")
    path = ""
    ASSET_PATH = "apps"

    if "pikesley_tildagon_countdown" in apps:
        ASSET_PATH = "/apps/pikesley_tildagon_countdown/"

    if "countdown" in apps:
        ASSET_PATH = "apps/countdown/"

else:
    ASSET_PATH = ""