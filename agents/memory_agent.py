
from typing import Optional

from agno.agent import Agent
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage

# ************* Database Connection *************
db_url = "postgresql://ramyakvr:@localhost:5432/personal_assistant"
# *******************************

# ************* Memory *************
memory = Memory(
    model=OpenAIChat(id="gpt-4o"),
    db=PostgresMemoryDb(table_name="memory_agent_memories", db_url=db_url),
    delete_memories=True,
    clear_memories=True,
)
# *******************************

# ************* Storage *************
memory_agent_storage = PostgresAgentStorage(
    table_name="memory_agent", db_url=db_url, auto_upgrade_schema=True
)
# *******************************


def get_memory_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Memory Agent",
        agent_id="memory-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(id="gpt-4o"),
        memory=memory,
        enable_agentic_memory=True,
        storage=memory_agent_storage,
        add_history_to_messages=True,
        num_history_runs=5,
        add_datetime_to_instructions=True,
        markdown=True,
    )
