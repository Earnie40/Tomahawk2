# Ring Integration Setup

## Method 1: Using ring-client-api
pip install ring-client-api

## Method 2: Using ring-doorbell
pip install ring-doorbell

## To get your Ring credentials:
1. Use your Ring account email and password
2. You'll receive a 2FA code on your phone
3. Enter the code when prompted

## Test Ring connection:
python -c "
from tomahawk2_ring import tool_ring_auth
import json
print(json.dumps(tool_ring_auth(email='your@email.com', password='your_password'), indent=2))
"
