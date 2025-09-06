import httpx
import asyncio
import uuid
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/api/v1/query/natural-language"
SESSION_ID = f"terminal-session-{uuid.uuid4()}"

# --- Initialize Rich for beautiful terminal output ---
console = Console()

def display_results(result: dict):
    """Formats and displays the API response in the terminal."""

    # Display the generated SQL query
    sql_query = result.get("generated_sql", "No SQL was generated.")
    console.print(Panel(Syntax(sql_query, "sql", theme="monokai", line_numbers=True), 
                        title="[bold green]Generated SQL[/bold green]", 
                        border_style="green"))

    # Display the data in a table
    data = result.get("data")
    if not data:
        console.print("[yellow]The query returned no results.[/yellow]")
        return

    try:
        table = Table(title="[bold blue]Query Results[/bold blue]", show_header=True, header_style="bold magenta")
        
        # Create columns from the keys of the first row
        headers = data[0].keys()
        for header in headers:
            table.add_column(header, style="cyan")
            
        # Add rows
        for row in data:
            # Convert all values to strings for display
            table.add_row(*[str(item) for item in row.values()])
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error rendering table:[/bold red] {e}")
        console.print("Raw data:", data)


async def main():
    """Main function to run the interactive chat loop."""
    console.print(Panel(f"[bold]Database Assistant[/bold]\nSession ID: {SESSION_ID}\nType 'exit' or 'quit' to end the conversation.", 
                        title="[bold cyan]Welcome![/bold cyan]", 
                        border_style="cyan"))

    async with httpx.AsyncClient(timeout=90.0) as client:
        while True:
            try:
                question = console.input("[bold yellow]You:[/bold yellow] ")

                if question.lower() in ["exit", "quit"]:
                    console.print("[bold]Goodbye![/bold]")
                    break

                if not question.strip():
                    continue

                with console.status("[bold green]Assistant is thinking...[/bold green]", spinner="dots"):
                    response = await client.post(
                        API_URL,
                        json={"question": question, "session_id": SESSION_ID}
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    display_results(result)
                else:
                    error_data = response.json()
                    error_message = error_data.get("detail", "An unknown error occurred.")
                    console.print(Panel(f"[bold red]API Error {response.status_code}:[/bold red]\n{error_message}", border_style="red"))

            except httpx.ConnectError:
                console.print("[bold red]Connection Error:[/bold red] Could not connect to the server. Is it running?")
                break
            except Exception as e:
                console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")

if __name__ == "__main__":
    asyncio.run(main())