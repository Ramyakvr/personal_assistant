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

        When handling queries about test cases in pull requests, format your response as follows:
        File name: <file_name>
        Test cases added: 
        Failure cases:
        Context: <context>
        Error: <error>
        Success case:
        Context: <context>
        Asserted fields: <asserted_fields>
        
        Always provide detailed and structured information about test cases when requested.
        """,
        show_tool_calls=True,
        markdown=True
    )

# Command line interface
if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "How many stars for rag-demo repo and for warehouse_mgmt_service repo"
    github_agent = get_github_agent()
    result = github_agent.run(query)
    print(result.content)




