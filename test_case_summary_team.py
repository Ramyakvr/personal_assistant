from dotenv import load_dotenv

from agno.models.openai import OpenAIChat
from agno.team import Team
from agents.github_agent import get_test_case_summary_agent
from agents.github_agent import get_pr_agent
from agents.jira_agent import get_jira_agent

load_dotenv()

def get_test_case_summary_team():
    test_case_summary_agent = get_test_case_summary_agent()
    pr_agent = get_pr_agent()
    jira_agent = get_jira_agent() 
    return Team(
        name="Test Case Summary Agent",
        description="Generate test case summary for the given pull request and add comment in the jira ticket",
        mode="coordinate",
        model=OpenAIChat(id="gpt-4o"),
        members=[test_case_summary_agent, pr_agent, jira_agent],
        instructions="""
        Generate test case summary for the given pull request using Test Case Summary Agent.
        Fetch jira ticket associated with the given pull request using PR Agent.
        Always add the generated test case summary as comment in the fetched jira ticket using Jira Agent.
        """,
        enable_agentic_context=True,
        share_member_interactions=True,
        show_members_responses=True,
        show_tool_calls=True,
        markdown=True,
        debug_mode=True,
    )

# Command line interface
if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Prepare the test case summary of warehouse_mgmt_service PR 3887 and add comment in the associated jira ticket"
    test_case_summary_team = get_test_case_summary_team()
    test_case_summary_team.print_response(query, markdown=True)