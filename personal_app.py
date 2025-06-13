#!/usr/bin/env python3
"""
Personal Assistant Application

This module provides a playground with various agents for GitHub, Jira, database operations,
memory management, and PR test summary generation.
"""

from agents.identity_service_agent import get_identity_service_db_agent
from agents.github_agent import get_github_agent
from agents.jira_agent import get_jira_agent
from agents.memory_agent import get_memory_agent
from test_case_summary_team import get_test_case_summary_team
from agno.playground import Playground, serve_playground_app

identity_service_db_agent = get_identity_service_db_agent()
github_agent = get_github_agent()
jira_agent = get_jira_agent()
memory_agent = get_memory_agent()
test_case_summary_team = get_test_case_summary_team()

app = Playground(
    agents=[
        github_agent,
        jira_agent,
        identity_service_db_agent,
        memory_agent,
    ],
    teams=[
        test_case_summary_team,
    ],
    app_id="personal-app",
    name="Personal App",
).get_app()

if __name__ == "__main__":
    serve_playground_app("personal_app:app", port=7777)


