# Bonnyrigg Pizza Blog - Login Flow Fixed

This version fixes the login flow so users can sign in normally unless they have chosen to enable 2FA in their profile.

## New behavior
- If 2FA is NOT enabled:
  - user logs in immediately with email + password
- If 2FA IS enabled:
  - user must enter a 6 digit code
- Password reset:
  - authenticator is used only if enabled
  - otherwise it falls back to Gmail/email verification

## Run
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
