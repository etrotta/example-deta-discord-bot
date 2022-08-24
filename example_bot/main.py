from flask_discord_interactions import DiscordInteractions

app = DiscordInteractions()

@app.command("hello")
def hello_world(ctx):
    return f"Hello world! ~{__name__!r}"

if __name__ == "__main__":
    app.update_commands()