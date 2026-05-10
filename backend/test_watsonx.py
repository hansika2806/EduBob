"""
Standalone test script for IBM watsonx.ai Granite integration
Tests authentication and model inference
"""
import os
import sys
import requests
import json
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Load environment variables
load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

print("=" * 80)
print("IBM watsonx.ai Granite Integration Test")
print("=" * 80)

# Step 1: Validate environment variables
print("\n[STEP 1] Validating Environment Variables")
print("-" * 80)
print(f"WATSONX_API_KEY: {'[OK] Set' if WATSONX_API_KEY else '[ERROR] Missing'}")
if WATSONX_API_KEY:
    print(f"  Length: {len(WATSONX_API_KEY)} characters")
    print(f"  Preview: {WATSONX_API_KEY[:10]}...{WATSONX_API_KEY[-10:]}")

print(f"WATSONX_PROJECT_ID: {'[OK] Set' if WATSONX_PROJECT_ID else '[ERROR] Missing'}")
if WATSONX_PROJECT_ID:
    print(f"  Value: {WATSONX_PROJECT_ID}")

print(f"WATSONX_URL: {WATSONX_URL}")

if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    print("\n[ERROR] Missing required environment variables!")
    exit(1)

# Step 2: Get IAM Access Token
print("\n[STEP 2] Getting IAM Access Token")
print("-" * 80)

iam_url = "https://iam.cloud.ibm.com/identity/token"
iam_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}
iam_data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": WATSONX_API_KEY
}

try:
    print(f"Requesting IAM token from: {iam_url}")
    iam_response = requests.post(iam_url, headers=iam_headers, data=iam_data, timeout=30)
    print(f"Response Status: {iam_response.status_code}")
    
    if iam_response.status_code == 200:
        iam_result = iam_response.json()
        access_token = iam_result.get("access_token")
        token_type = iam_result.get("token_type")
        expires_in = iam_result.get("expires_in")
        
        print(f"[SUCCESS] IAM Token obtained successfully!")
        print(f"  Token Type: {token_type}")
        print(f"  Expires In: {expires_in} seconds")
        print(f"  Token Preview: {access_token[:20]}...{access_token[-20:]}")
    else:
        print(f"[ERROR] Failed to get IAM token!")
        print(f"Response: {iam_response.text}")
        exit(1)
        
except Exception as e:
    print(f"[ERROR] Error getting IAM token: {str(e)}")
    exit(1)

# Step 3: Test watsonx.ai API with Granite model
print("\n[STEP 3] Testing watsonx.ai API with Granite Model")
print("-" * 80)

test_prompt = """Analyze these student programming errors:
- IndexError: list index out of range
- TypeError: unsupported operand type(s) for +: 'int' and 'str'

Provide:
1. Common errors (list 2 most frequent error types)
2. Struggling concepts (list 2 programming concepts)

Format:
Common Errors:
- error 1
- error 2

Struggling Concepts:
- concept 1
- concept 2"""

watsonx_url = f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29"
watsonx_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

watsonx_body = {
    "input": test_prompt,
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 0,
        "stop_sequences": [],
        "repetition_penalty": 1
    },
    "model_id": "ibm/granite-3-8b-instruct",
    "project_id": WATSONX_PROJECT_ID
}

try:
    print(f"Sending request to: {watsonx_url}")
    print(f"Model: ibm/granite-3-8b-instruct")
    print(f"Project ID: {WATSONX_PROJECT_ID}")
    print(f"Prompt length: {len(test_prompt)} characters")
    
    watsonx_response = requests.post(
        watsonx_url,
        headers=watsonx_headers,
        json=watsonx_body,
        timeout=60
    )
    
    print(f"\nResponse Status: {watsonx_response.status_code}")
    
    if watsonx_response.status_code == 200:
        result = watsonx_response.json()
        print(f"[SUCCESS] API call successful!")
        print(f"\nFull Response:")
        print(json.dumps(result, indent=2))
        
        generated_text = result.get("results", [{}])[0].get("generated_text", "")
        print(f"\n{'=' * 80}")
        print("Generated Text:")
        print(f"{'=' * 80}")
        print(generated_text)
        print(f"{'=' * 80}")
        
        print(f"\n[SUCCESS] IBM watsonx.ai Granite integration is working!")
        
    else:
        print(f"[ERROR] API call failed!")
        print(f"Response Headers: {dict(watsonx_response.headers)}")
        print(f"Response Body: {watsonx_response.text}")
        
        # Try to parse error details
        try:
            error_data = watsonx_response.json()
            print(f"\nError Details:")
            print(json.dumps(error_data, indent=2))
        except:
            pass
            
        exit(1)
        
except requests.exceptions.Timeout:
    print(f"[ERROR] Request timed out after 60 seconds")
    exit(1)
except Exception as e:
    print(f"[ERROR] Error calling watsonx.ai API: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 80)
print("Test completed successfully!")
print("=" * 80)

# Made with Bob
