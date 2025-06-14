# ✅ VoiceOutReach.ai - Clean Colab Template for LinkedIn Voice Outreach
# Version: MVP
# Author: Hassan

# 📦 STEP 0: Install Required Packages
!pip install --quiet openai

# 📂 STEP 1: Imports and Setup
import os
import io
import requests
import pandas as pd
from google.colab import files
from openai import OpenAI

# 📌 STEP 2: Configuration
# 🔐 Insert your actual keys below
OPENAI_API_KEY = "your-openai-api-key"
ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
VOICE_ID = "your-elevenlabs-voice-id"  # e.g., "1SM7GgM6IMuvQlz2BwM3"

USE_FULL_GPT = True     # Use GPT to generate full message
TEST_ONE_ROW = False     # True = only process 1 row for testing

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# 📁 STEP 3: Output folder
output_folder = "/content/voice_notes"
os.makedirs(output_folder, exist_ok=True)

# 📤 STEP 4: Upload CSV File
uploaded = files.upload()
filename = list(uploaded.keys())[0]
df = pd.read_csv(io.BytesIO(uploaded[filename]))

# 🛠️ STEP 5: Clean + Map Columns (adjust if needed)
df.columns = df.columns.str.strip()  # Remove spaces from column names
df['first_name'] = df['Full name'].str.split().str[0]
df['position'] = df['Position']
df['company'] = df['Company name']
df['job_description'] = df['Description']
df['hiring_for'] = df['Hiring for Job Title']

# 🔄 STEP 6: Process Each Lead
results = []
loop_data = df.head(1) if TEST_ONE_ROW else df

for index, row in loop_data.iterrows():
    vars = {
        "first_name": row['first_name'],
        "position": row['position'],
        "company": row['company'],
        "hiring_for": row['hiring_for'],
        "job_description": row['job_description']
    }

    # 🎯 GPT Prompt (Structure: Hook → Intro → Value → CTA)
    full_prompt = f"""
You're crafting a professional, voice-style LinkedIn message.

Structure:
1. Start with a friendly sentence showing you've read their job description
2. Introduce yourself: "I'm Hassan..."
3. Briefly explain how you can help (relevant to their job post)
4. End with: "Happy to hop on a quick call if you're open to it."

Keep it around 80–100 words.
Tone: warm, natural, and professional.

Info:
- First name: {vars['first_name']}
- Role: {vars['position']}
- Company: {vars['company']}
- Hiring for: {vars['hiring_for']}
- Job Description: {vars['job_description']}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if your API account has access
            messages=[{"role": "user", "content": full_prompt}]
        )
        message_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT error: {e}")
        message_text = f"Hi {vars['first_name']}, I noticed you're hiring and wanted to reach out personally. (GPT error)"

    print(f"\n🎤 Message for {vars['first_name']}\n{message_text}\n")

    # 🗣️ ElevenLabs Text-to-Speech
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": message_text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    response = requests.post(tts_url, headers=headers, json=payload)

    voice_filename = f"{vars['first_name'].strip()}_{vars['hiring_for'].strip()}.mp3"
    voice_path = os.path.join(output_folder, voice_filename)

    if response.status_code == 200:
        with open(voice_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved voice note: {voice_filename}")
    else:
        print(f"❌ ElevenLabs Error: {response.status_code}")

    results.append({
        "First Name": vars['first_name'],
        "Company": vars['company'],
        "Position": vars['position'],
        "Hiring For": vars['hiring_for'],
        "Message": message_text,
        "Voice File": voice_filename
    })

# 💾 STEP 7: Save Messages to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("generated_voice_messages.csv", index=False)
print("\n✅ Messages saved to generated_voice_messages.csv")

# 📦 STEP 8: Zip MP3s for Download
import shutil
shutil.make_archive(output_folder, 'zip', output_folder)
files.download(output_folder + ".zip")
print("✅ Voice notes zipped and ready to download")
