# Local Setup & Installation

## Prerequisites
* Python 3.9+
* AWS CLI configured with active SSO credentials
* Access to the specific AWS account hosting the Bedrock Knowledge Base

## Installation Steps
1. **Clone the repository:**
```
git clone https://github.com/Chubbyy/Hub-MDA-Helpdesk-01.git
cd Hub-MDA-Helpdesk-01
```

2. **Create and activate a virtual environment:**
```
# Windows:
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
```

3. **Install dependencies:**
```
pip install -r requirements.txt
```

4. **Authenticate with AWS:**
Prior to running the application, login with AWS:
```
aws sso login
```

5. **Launch the application:**
```
streamlit run app.py
```