try:  # Only for syncing the commands - you should use `deta update -e` for the Micro environment variables
    from dotenv import load_dotenv
    load_dotenv('.env')
except ImportError:
    pass

import os
from deta_discord_interactions import DiscordInteractions
from deta_discord_interactions.utils.oauth import enable_oauth

app = DiscordInteractions()
enable_oauth(app)

from notes import blueprint as notes_blueprint
from webhooks import blueprint as webhooks_blueprint
from oauth import blueprint as oauth_blueprint

app.register_blueprint(notes_blueprint)
app.register_blueprint(webhooks_blueprint)
app.register_blueprint(oauth_blueprint)

@app.command("hello")
def hello_world(ctx):
    return f"Hello world!"


if __name__ == "__main__":
    print("Updating commands")
    app.update_commands(guild_id=os.getenv("GUILD_ID"))
