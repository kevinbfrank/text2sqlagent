import os
import sys
import argparse
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

# System prompt for the SQL agent
SYSTEM_PROMPT = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
"""

def create_sql_agent():
    """Create and return a text-to-SQL agent"""

    # Connect to Chinook database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chinook.db")
    db = SQLDatabase.from_uri(
        f"sqlite:///{db_path}",
        sample_rows_in_table_info=3
    )

    # Initialize Claude Sonnet 4.5
    model = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0
    )

    # Create SQL toolkit with tools
    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    tools = toolkit.get_tools()

    # Create the agent
    agent = create_agent(
        model,
        tools,
        system_prompt=SYSTEM_PROMPT.format(dialect=db.dialect, top_k=5)
    )

    return agent


def main():
    """Main entry point for the SQL Agent CLI"""
    parser = argparse.ArgumentParser(
        description="Text-to-SQL Agent powered by LangChain and Claude Sonnet 4.5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py "What are the top 5 best-selling artists?"
  python agent.py "Which employee generated the most revenue?"
  python agent.py "How many customers are from Canada?"
        """
    )
    parser.add_argument(
        "question",
        type=str,
        help="Natural language question to answer using the Chinook database"
    )

    args = parser.parse_args()

    # Display the question
    console.print(Panel(
        f"[bold cyan]Question:[/bold cyan] {args.question}",
        border_style="cyan"
    ))
    console.print()

    # Create the agent
    console.print("[dim]Creating SQL Agent...[/dim]")
    agent = create_sql_agent()

    # Invoke the agent
    console.print("[dim]Processing query...[/dim]\n")

    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": args.question}]
        })

        # Extract and display the final answer
        final_message = result["messages"][-1]
        answer = final_message.content if hasattr(final_message, 'content') else str(final_message)

        console.print(Panel(
            f"[bold green]Answer:[/bold green]\n\n{answer}",
            border_style="green"
        ))

    except Exception as e:
        console.print(Panel(
            f"[bold red]Error:[/bold red]\n\n{str(e)}",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == "__main__":
    main()
