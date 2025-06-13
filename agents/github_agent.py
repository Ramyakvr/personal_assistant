from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.github import GithubTools

# Load environment variables (for GITHUB_ACCESS_TOKEN)
load_dotenv()

# Initialize a single GitHub agent with all tools enabled
def get_github_agent():
    return Agent(
        name="GitHub Agent",
        role="Perform various GitHub operations like fetching pull requests, stars, issues, etc.",
        model=OpenAIChat(id="gpt-4o"),
        tools=[GithubTools(
            get_repository=True,
            get_pull_request=True,
            get_pull_request_changes=True,
            get_repository_languages=True,
            list_branches=True,
            get_pull_request_count=True,
            get_repository_stars=True,
            get_pull_requests=True,
            get_pull_request_comments=True,
            get_pull_request_with_details=True,
            get_file_content=True,
            get_directory_content=True,
            get_branch_content=True,
            search_code=True,
            search_issues_and_prs=True,
        )],
        instructions="""Help with GitHub operations including fetching repository information, pull requests, issues, etc.
        Always look for the repository in shopuptech org. Only if not found, look for it in Ramyakvr and in Mohan-Kumar-0018.
        """,
        show_tool_calls=True,
        markdown=True
    )

def get_test_case_summary_agent():
    return Agent(
        name="Test Case Summary Agent",
        role="Generate test case summaries for given pull request",
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            GithubTools(
                get_repository=True,
                get_pull_request=True,
                get_pull_request_changes=True,
                get_pull_requests=True,
                get_pull_request_with_details=True,
                search_issues_and_prs=True,
            )
        ],
        instructions="""
        Search the given pull requests in shopuptech org in given repository.
        Find newly added and updated unit test cases in test files in the pull request.
        Prepare test case summary in the below structure.
        File name: <file_name>
        Testing object: <API or subject being tested>
        For each failure case:
        Data Setup: <Data setup details and API parameters>
        Context: <complete context or the scenario>
        Error: <error message and other assertions>
        For each success case:
        Data Setup: <Data setup details and API parameters>
        Context: <complete context or the scenario>
        Asserted fields: <API response and assertion details>
        """,
        show_tool_calls=True,
        markdown=True,
    )

def get_pr_agent():
    return Agent(
        name="PR Agent",
        role="PR Agent",
        description="Find the jira ticket associated with the given pull request",
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            GithubTools(
                get_repository=True,
                get_pull_request=True,
                get_pull_requests=True,
                get_pull_request_with_details=True,
                search_issues_and_prs=True,
            )
        ],
        instructions="""
        Search the given pull requests in shopuptech org in given repository.
        PR title will follow the convention of having the jira ticket at the end within square bracket in this format [UDH-5076].
        Extract and return jira ticket number from the PR title.
        """,
        show_tool_calls=True,
        markdown=True,
    )

# Command line interface
if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "How many stars for rag-demo repo and for warehouse_mgmt_service repo"
    github_agent = get_github_agent()
    github_agent.print_response(query, markdown=True)
