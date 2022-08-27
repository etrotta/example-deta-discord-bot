import os
from deta_discord_interactions import DiscordInteractions
try:  # Only for syncing the commands - you should use `deta update -e` for the Micro environment variables
    from dotenv import load_dotenv
    load_dotenv('.env')
except ImportError:
    pass

app = DiscordInteractions()

from notes import blueprint as notes_blueprint

app.register_blueprint(notes_blueprint)


@app.command("hello")
def hello_world(ctx):
    return f"Hello world!"


if __name__ == "__main__":
    print("Updating commands")
    # print(app.run_command({"data": {"name": "hello"}}))
    app.update_commands(guild_id=os.getenv("GUILD_ID"))
