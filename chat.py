import json
import argparse
from termcolor import colored
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from perplexica_client import PerplexicaClient

# Load the configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize the Perplexica client with the loaded configuration
client = PerplexicaClient(config)

# Initialize a console object for rich output
console = Console()

def render_sources(sources):
    """Render sources with proper formatting as a numbered list."""
    if not sources:
        return

    console.print("[yellow]Sources Referenced:[/yellow]")
    for i, source in enumerate(sources, 1):
        title = source['metadata']['title']
        url = source['metadata']['url']
        link_text = Text(f"{i}. {title}: ", style="cyan")
        link_text.append(Text(url, style="blue underline"))
        console.print(link_text)

def handle_query(query):
    """Handles a single query passed via the command line or during chat."""
    response = client.send_query(query)
    if response:
        assistant_reply = response["message"]
        
        # Extract and display sources
        sources = response.get("sources", [])
        if sources:
            render_sources(sources)

        # Render Markdown reply using rich
        markdown_content = Markdown(assistant_reply)
        console.print("\n[blue]Assistant:[/blue]")
        console.print(markdown_content)
    else:
        console.print("[red]Assistant:[/red] I'm sorry, I couldn't process your request.\n")

def chat_with_agent():
    """Interactive chat session."""
    console.print("[green bold]Perplexica Chat Agent[/green bold]\nType 'exit' to end the chat.\n")

    # Initial chat history
    client.add_message("human", "Hello!")
    client.add_message("assistant", "Hi there! How can I assist you today?")
    console.print("[blue]Assistant:[/blue] Hi there! How can I assist you today?\n")

    while True:
        user_input = input(colored("You: ", "green")).strip()

        if user_input.lower() in ['exit', 'quit']:
            console.print("[cyan]Ending chat. Goodbye![/cyan]")
            break

        handle_query(user_input)

def main():
    """Entry point to handle CLI arguments or start chat."""
    parser = argparse.ArgumentParser(description="Terminal Researcher")
    parser.add_argument("query", nargs="*", help="The research query. If not provided, interactive mode starts.")
    args = parser.parse_args()

    if args.query:
        # Combine query words into a single string for direct research
        query = " ".join(args.query)
        handle_query(query)
    else:
        # Start interactive chat if no query is provided
        chat_with_agent()

if __name__ == "__main__":
    main()
