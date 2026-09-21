#!/usr/bin/env python
# coding: utf-8

# # INFO 5940 — Environment Check
# 
# Run each cell below in order. If all four checks print a ✅, your Codespace is ready.
# 
# If a cell fails, the message tells you what to fix — see **Step 2: Set your OpenAI API key** in the README.

# In[ ]:


# 1. Package versions
import importlib.metadata as md

for pkg in ["openai", "langchain", "langchain-openai", "streamlit", "pandas", "pydantic", "tiktoken"]:
    try:
        print(f"  {pkg:20s} {md.version(pkg)}")
    except md.PackageNotFoundError:
        print(f"  {pkg:20s} NOT INSTALLED  <-- rerun: pip install -r requirements.txt")

print("\n✅ Packages loaded.")


# In[ ]:


# 2. Credentials — checked WITHOUT printing the key itself
import os
from dotenv import load_dotenv

# Where the key comes from:
#   In Codespaces  -> a Codespaces secret, already in the environment.
#   Running locally -> a .env file you create (see .env.example).
#
# load_dotenv() does NOT overwrite variables that are already set, so the
# Codespaces secret always wins and .env is only a fallback.
load_dotenv()

key = os.environ.get("OPENAI_API_KEY")
base = os.environ.get("OPENAI_BASE_URL")

if not key:
    raise SystemExit(
        "❌ OPENAI_API_KEY is not set.\n"
        "   In Codespaces:  add it as a Codespaces secret, then rebuild the Codespace.\n"
        "   Running locally: copy .env.example to .env and fill in your key.\n"
        "   Full instructions are in the README under 'Step 2: Set your OpenAI API key'."
    )

print(f"  OPENAI_API_KEY   set ({len(key)} characters, starts with {key[:3]}...)")

if not base:
    print("  OPENAI_BASE_URL  NOT SET — requests would go to OpenAI directly,")
    print("                   not Cornell's endpoint. Set it in .env if running locally.")
else:
    print(f"  OPENAI_BASE_URL  {base}")

print("\n✅ Credentials present.")


# In[ ]:


# 3. Create the client
from openai import OpenAI

client = OpenAI()   # reads OPENAI_API_KEY and OPENAI_BASE_URL from the environment
print("✅ Client created.")


# In[ ]:


# 4. One small live API call
MODEL = "openai.gpt-4o"

# temperature controls randomness: 0.0 is (near-)deterministic, higher values
# give more varied replies. 0 is right for a verification test — you want the
# same answer every run. Raise it in your own assignment code to experiment.
TEMPERATURE = 0.0

try:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", 
             "content": "Reply with exactly: hello INFO 5940"}
            ],
        temperature=TEMPERATURE,
        max_tokens=20,
    )
    print("  Model reply:", resp.choices[0].message.content.strip())
    print("\n✅ Your environment is fully working.")

except Exception as e:
    name = type(e).__name__
    print(f"❌ The API call failed ({name}).\n")
    if "Authentication" in name or "401" in str(e):
        print("   Your key was rejected. Check that the Codespaces secret holds")
        print("   your full Cornell AI key, then rebuild the Codespace.")
    elif "NotFound" in name or "404" in str(e):
        print(f"   The model '{MODEL}' was not found at {os.environ.get('OPENAI_BASE_URL')}.")
        print("   Confirm the model name with your instructor.")
    elif "Connection" in name or "APITimeout" in name:
        print("   Could not reach the API. Check your network and OPENAI_BASE_URL.")
    else:
        print(f"   {e}")
    print("\n   Still stuck? Post the error name above (not your key) on the class forum.")

