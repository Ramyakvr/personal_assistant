# Personal Assistant

A collection of AI agents and teams built with the Agno framework to assist with various tasks.

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
   # OpenAI API Key
   OPENAI_API_KEY=<your_openai_api_key>

   # PostgreSQL SSL Configuration
   TELEPORT_SSL_MODE=verify-full
   TELEPORT_STAGING_POSTGRES_SSL_CERT=<your_staging_postgres_ssl_cert>
   TELEPORT_PROD_POSTGRES_SSL_CERT=<your_prod_postgres_ssl_cert>
   TELEPORT_SSL_KEY=<your_ssl_key>
   TELEPORT_SSL_ROOT_CERT=<your_ssl_root_cert>

   # GitHub Access Token
   GITHUB_ACCESS_TOKEN=<your_github_access_token>

   # Jira
   JIRA_SERVER_URL=https://shopup.atlassian.net
   JIRA_USERNAME=<your_jira_username>
   JIRA_TOKEN=<your_jira_token>
   ```

## Usage

### Individual Agents

1. Run identity service agent:
   ```bash
   python agents/identity_service_agent.py "How many users are mapped with Supply Manager role in staging db"
   ```

2. Run GitHub agent:
   ```bash
   python agents/github_agent.py "Give latest PR details of warehouse_mgmt_service repo"
   ```

3. Run Jira agent:
   ```bash
   python agents/jira_agent.py "Get details of ticket UDH-5076"
   ```

4. Run Test case summary team:
   ```bash
   python test_case_summary_team.py "Prepare the test case summary of warehouse_mgmt_service PR 3887 and add comment in the associated jira ticket"
   ```

### Personal App

#### Run playground server

Start the playground server on port 7777:
```bash
python personal_app.py
```

#### Run Local Agent UI

1. Clone the Agent UI:
   ```bash
   npx create-agent-ui@latest
   ```

2. Start the development server:
   ```bash
   cd agent-ui && npm run dev
   ```

3. Open http://localhost:3000 to view the Agent UI

#### Alternative: Connect to Agno Playground UI

1. Set up the connection:
   ```bash
   ag setup
   ```

2. Open the link provided or navigate to http://app.agno.com/playground (login required)

3. Add/Select the localhost:7777 endpoint and start chatting with your agents!
