# Bonnyrigg Pizza Blog +

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
