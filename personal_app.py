#!/usr/bin/env python3
"""
Identity Service Postgres Agent Module

This module provides tools to interact with Identity Service PostgreSQL databases in both staging and production
environments using the Agno framework.
"""

from agents.identity_service_agent import get_identity_service_db_agent
from agents.memory_agent import get_memory_agent
from agno.playground import Playground, serve_playground_app

identity_service_db_agent = get_identity_service_db_agent()
memory_agent = get_memory_agent()
app = Playground(
    agents=[
        identity_service_db_agent,
        memory_agent
    ],
    app_id="personal-app",
    name="Personal App",
).get_app()

if __name__ == "__main__":
    serve_playground_app("personal_app:app", port=7777)


