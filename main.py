import openai, os, config, typer
from rich import print
from rich.table import Table

os.system("clear")

# Creating a table using Table (rich)
table = Table("Comando", "Descripción")
table.add_row("exit","Salir de la aplicación")
table.add_row("new","Reiniciar el contexto")

# Calls Api Key from another archive
openai.api_key = config.api_key

def main():
  print("[bold green]\nWelcome to ChatGPT Assistant.\n[/bold green]")
  # Assistant context
  context = {"role":"system", "content":"Eres un asistente muy útil"}
  messages = [context]
  # print Table
  print(table)
  # while Loop
  while True:
      # Private function "__prompt" calls user's input
      content = __prompt()
      
      # If user writes "new" its reset context
      if content == "new":
        print("Context has been restarted.")
        messages = [context]
        content= __prompt()
      # User's question are append into message list to create a context from Questions
      messages.append({"role":"user","content":content})

      response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
      )
      # GPT's responses are append into message list to create a context from Responses
      response_content = response.choices[0].message.content
      messages.append({"role":"assistant","content":response_content})

      print(f"\n[bold blue]_>[/bold blue] [green]{response_content}\n[/green]")

# It manage user's prompts and it return a data type string 
# -> It indicates data type
def __prompt() -> str:
  # prompt through typer
  prompt = typer.prompt("\nAsk me a question")
  
  # If user writes "exit"
  if prompt == "exit":
    # Ask for confirmation
    exit = typer.confirm("🤔 Are you sure you want to leave?")
    if exit:
      # stop program
      print("Bye!")
      raise typer.Abort()
    # return to the begin
    return __prompt()
  # returb user's prompt
  return prompt


if __name__ == "__main__":
    typer.run(main)