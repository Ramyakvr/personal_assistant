#!/usr/bin/env python3
"""
Identity Service Postgres Agent Module

This module provides tools to interact with Identity Service PostgreSQL databases in both staging and production
environments using the Agno framework.
"""

import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.postgres import PostgresTools
from agno.models.openai import OpenAIChat
from agno.tools import tool

# Load environment variables from .env file
load_dotenv()

# Define database configurations
DB_CONFIGS = {
    "staging": {
        "agent_name": "StagingIdentityServiceAgent",
        "user": "teleport_view",
        "password": "",
        "host": "plteleport.shopup.center",
        "port": 443,
        "db_name": "auth_stage_vacc",
        "ssl_config": {
            "mode": os.getenv("TELEPORT_SSL_MODE"),
            "cert": os.getenv("TELEPORT_STAGING_POSTGRES_SSL_CERT"),
            "key": os.getenv("TELEPORT_SSL_KEY"),
            "root_cert": os.getenv("TELEPORT_SSL_ROOT_CERT")
        }
    },
    "production": {
        "agent_name": "ProductionIdentityServiceAgent",
        "user": "teleport_view",
        "password": "",
        "host": "plteleport.shopup.center",
        "port": 443,
        "db_name": "shopup_identity_service",
        "ssl_config": {
            "mode": os.getenv("TELEPORT_SSL_MODE"),
            "cert": os.getenv("TELEPORT_PROD_POSTGRES_SSL_CERT"),
            "key": os.getenv("TELEPORT_SSL_KEY"),
            "root_cert": os.getenv("TELEPORT_SSL_ROOT_CERT")
        }
    }
}


def create_postgres_agent(environment: str):
    """Create a PostgreSQL agent for the specified environment.
    
    Args:
        environment (str): The environment to use ('staging' or 'production')
    
    Returns:
        Agent: Configured PostgreSQL agent
    """
    # Get the database configuration for the specified environment
    db_config = DB_CONFIGS.get(environment)
    if not db_config:
        raise ValueError(f"Unknown environment: {environment}. Available environments: {', '.join(DB_CONFIGS.keys())}")
    
    # Set environment variables for SSL configuration
    if db_config.get('ssl_config'):
        ssl_config = db_config['ssl_config']
        os.environ['PGSSLMODE'] = ssl_config.get('mode', 'verify-full')
        os.environ['PGSSLCERT'] = ssl_config.get('cert', '')
        os.environ['PGSSLKEY'] = ssl_config.get('key', '')
        os.environ['PGSSLROOTCERT'] = ssl_config.get('root_cert', '')
    
    # Initialize PostgresTools with the provided configuration
    postgres_tool = PostgresTools(
        user=db_config.get('user', ''),
        password=db_config.get('password', ''),
        host=db_config.get('host', ''),
        port=db_config.get('port', 5432),
        db_name=db_config.get('db_name', '')
    )
    
    # Create and return the agent
    return Agent(
        name=db_config.get('agent_name', f"{environment.capitalize()}IdentityServiceAgent"),
        model=OpenAIChat(id="gpt-4o"),
        description=f"An AI agent that can query the Identity Service {environment} database and perform database operations.",
        tools=[postgres_tool],
        show_tool_calls=True,
    )

@tool(
    name="query_staging_db",
    description="Query the Identity Service staging database for information",
    show_result=True
)
def query_staging_db(query: str) -> str:
    """Execute a query against the Identity Service staging database.
    
    Args:
        query (str): SQL query or natural language query to execute against the staging database
    
    Returns:
        str: Query results from the staging database
    """
    # Create agent with staging configuration
    agent = create_postgres_agent("staging")
    # Execute the query and return results
    result = agent.run(query)
    return result.content


@tool(
    name="query_production_db",
    description="Query the Identity Service production database for information",
    show_result=True
)
def query_production_db(query: str) -> str:
    """Execute a query against the Identity Service production database.
    
    Args:
        query (str): SQL query or natural language query to execute against the production database
    
    Returns:
        str: Query results from the production database
    """
    # Create agent with production configuration
    agent = create_postgres_agent("production")
    # Execute the query and return results
    result = agent.run(query)
    return result.content


def create_router_agent():
    """Create a router agent that can select between staging and production databases
    based on the user's query content.
    
    Returns:
        Agent: Configured router agent with tools for both staging and production
    """
    return Agent(
        name="IdentityServiceRouterAgent",
        model=OpenAIChat(id="gpt-4o"),
        description="An AI agent that can route queries to either staging or production Identity Service databases based on the query content.",
        tools=[query_staging_db, query_production_db],
        show_tool_calls=True,
    )


def main():
    """Main entry point for the script."""
    # Check if enough arguments were provided
    # if len(sys.argv) < 2:
    #     print("Usage: python postgres_agent.py \"<query>\"")
    #     print("Example: python postgres_agent.py \"What tables are in the Identity Service staging database?\"")
    #     sys.exit(1)
        
    # # Get the query from command line arguments
    # query = sys.argv[1]
    
    # Create the router agent that can select between staging and production db based on the query content
    router_agent = create_router_agent()
    
    # Run the query through the router agent which will select the appropriate tool
    # print("The agent will automatically select between Identity Service staging or production database based on your query.")
    query = "How many users are mapped with Supply Manager role in staging db"
    result = router_agent.run(query)
    print("Query: ", query)
    print("\n")
    print(result.content)

    query = "How many users are mapped with Supply Manager role in production db"
    result = router_agent.run(query)
    print("Query: ", query)
    print("\n")
    print(result.content)

    query = "How many users are mapped with Supply Manager role in staging db"
    result = router_agent.run(query)
    print("Query: ", query)
    print("\n")
    print(result.content)

if __name__ == "__main__":
    main()
