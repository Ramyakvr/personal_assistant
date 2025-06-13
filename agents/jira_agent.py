from dotenv import load_dotenv

from agno.agent import Agent
from agno.tools.jira import JiraTools
from agno.models.openai import OpenAIChat

# Load environment variables (for JIRA_ACCESS_TOKEN)
load_dotenv()

def get_jira_agent():
    return Agent(
        name="Jira Agent",
        role="Perform various Jira operations like fetching issues, adding comments, updating status etc.",
        tools=[JiraTools()],
        model=OpenAIChat(id="gpt-4o"),
        instructions="""
        """,
        show_tool_calls=True,
        markdown=True
    )

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "get details of ticket UDH-5076"
    jira_agent = get_jira_agent()
    jira_agent.print_response(query, markdown=True)