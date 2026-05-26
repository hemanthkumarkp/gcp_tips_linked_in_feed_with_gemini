import os
import sys
import requests
from google import genai

# 1. Initialize the Gemini Client
# The SDK automatically looks for the GEMINI_API_KEY environment variable.
if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

client = genai.Client()

# 2. Generate the GCP Tip
prompt = """
Write a short, engaging LinkedIn post sharing a highly practical Google Cloud Platform (GCP) tip, trick, or best practice. 
Include:
- A catchy hook.
- The core tip explained simply.
- 2-3 relevant hashtags (e.g., #GCP, #GoogleCloud, #CloudArchitecture).
Keep it under 150 words and do not use markdown bolding (like **) in the output prose.
"""

print("Generating GCP tip from Gemini...")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
)
gcp_tip = response.text
print(f"Generated Content:\n{gcp_tip}\n")

# 3. Post to LinkedIn
linkedin_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
linkedin_author = os.environ.get("LINKEDIN_AUTHOR_URN")  # format: urn:li:person:YOUR_ID

if not linkedin_token or not linkedin_author:
    print("Error: LinkedIn credentials missing.")
    sys.exit(1)

url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {linkedin_token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

payload = {
    "author": linkedin_author,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": gcp_tip
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

print("Posting to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)

if res.status_code in [200, 201]:
    print("Successfully posted to LinkedIn!")
else:
    print(f"Failed to post. Status code: {res.status_code}")
    print(res.text)
    sys.exit(1)
