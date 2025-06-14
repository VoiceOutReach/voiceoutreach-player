
# 🗂️ STEP 1: Set GitHub Access

GITHUB_USERNAME = "your-github-username"
GITHUB_TOKEN = "ghp_yourRealGitHubToken"
REPO_NAME = "voiceoutreach-player"

repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

!git clone {repo_url}
%cd {REPO_NAME}



# 🎙️ STEP 2: Save a dummy voice note into public/voices/

import os
from datetime import datetime

output_dir = "public/voices"
os.makedirs(output_dir, exist_ok=True)

filename = f"voice_note_{datetime.now().strftime('%H%M%S')}.mp3"
file_path = os.path.join(output_dir, filename)

with open(file_path, "wb") as f:
    f.write(b"Fake audio content for testing!")

print(f"✅ Voice note saved at: {file_path}")



# 📤 STEP 3: Push to GitHub

!git config --global user.name "Your Name"
!git config --global user.email "your@email.com"

from datetime import datetime
commit_msg = f"🔊 Auto-push voice notes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

!git add -f public/voices/*.mp3
!git commit -m "{commit_msg}"
!git push origin main
