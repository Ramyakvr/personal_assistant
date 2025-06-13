## Setup

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your API credentials:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_ACCESS_TOKEN=your_github_access_token
   ```

## Usage

1. Run identity service agent:
   ```bash
   python agents/identity_service_agent.py
   ```
2. Run github agent:
   ```bash
   python agents/github_agent.py  --pr 3843 --repo shopuptech/warehouse_mgmt_service
   ```

3. Run personal app:
   
   ```bash
   npx create-agent-ui@latest 

   ```bash
   python personal_app.py
   ```
