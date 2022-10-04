from typing import Optional
from deta_discord_interactions import DiscordInteractionsBlueprint
from deta_discord_interactions import Message
from deta_discord_interactions import Context

from deta_discord_interactions import Autocomplete, Option, Choice
from deta_discord_interactions import Embed, embed

from deta_discord_interactions.enums import PERMISSION

from deta_discord_interactions.utils.database import Database, AutoSyncRecord
from deta_discord_interactions.utils.database import Query, Field


from deta_discord_interactions.utils.oauth import OAuthToken, Webhook, create_webhook


database = Database(name="webhooks", record_type=AutoSyncRecord)

blueprint = DiscordInteractionsBlueprint()

# NOTE: The frequency will be whatever you set on `deta cron set "..."`
@blueprint.task()
def send_scheduled_messages_task():
    "Run all Webhooks set on Repeat"
    query = Query(
        Field("repeat") == True  # This one is actually meant to be `== True`, NOT `is True`
    )
    from concurrent.futures import ThreadPoolExecutor
    # You only have 10 seconds to be done with the tasks unless you request a increase,
    # so might as well try to do things as fast as possible with threading etc
    with ThreadPoolExecutor() as executor:
        for record in database.fetch(query):
            webhook = record["hook"]
            executor.submit(webhook.send, record['repeat_message'])
            # webhook.send(record["repeat_message"])


hooks = blueprint.command_group(
    name="webhook",
    description="Manage this bot's Webhooks", 
    default_member_permissions=PERMISSION.MANAGE_MESSAGES + PERMISSION.MANAGE_WEBHOOKS,
    dm_permission=False,
)


def save_webhook(oauth: Optional[OAuthToken], ctx: Context, internal_name: str):
    if oauth is None:  # User declined the consent form
        return f"Canceled creation of webhook {internal_name}"
    webhook: Webhook = oauth.webhook
    key = f'webhook_{ctx.author.id}_{internal_name}'
    with database[key] as record:
        record["internal_name"] = internal_name
        record["hook"] = webhook
    # Do NOT return a Message - this is what the end user will see in their browser
    return f"Registered webhook `{internal_name}`"


@hooks.command("register")
def register_webhook(ctx, internal_name: str):
    message = create_webhook(ctx, internal_name, callback=save_webhook, args=(internal_name,))
    return message


@hooks.command("invoke")
def invoke_webhook(ctx, internal_name: Autocomplete[str], message: str):
    "Send a message via an existing Webhook"
    key = f'webhook_{ctx.author.id}_{internal_name}'
    # webhook: Webhook = database.get(key).get("hook")
    # if webhook is None:
    #     return Message(f"Webhook `{internal_name}` not found", ephemeral=True)
    webhook: Webhook = database.get(key)["hook"]
    webhook.send(message)
    return Message("Sent message", ephemeral=True)


@hooks.command("editmsg")
def edit_webhook_message(ctx, internal_name: Autocomplete[str], message_id: str, updated_message: str):
    "Edit a Message previously sent via a Webhook"
    key = f'webhook_{ctx.author.id}_{internal_name}'
    webhook: Webhook = database.get(key).get("hook")
    if webhook is None:
        return Message(f"Webhook `{internal_name}` not found", ephemeral=True)
    try:
        webhook.edit_message(Message(updated_message), message_id=message_id)
    except Exception:
        return Message("Failed to edit Message", ephemeral=True)
    else:
        return Message("Edited the message", ephemeral=True)


@hooks.command("update")
def update_webhook(ctx, internal_name: Autocomplete[str], display_name: str, reason: str = None):
    "Updates a Webhook's default display name."
    key = f'webhook_{ctx.author.id}_{internal_name}'
    record = database.get(key)
    webhook: Webhook = record.get("hook")
    if webhook is None:
        return Message(f"Webhook `{internal_name}` not found", ephemeral=True)
    try:
        webhook.patch(name=display_name, reason=reason)
        webhook.name = display_name
        record["hook"] = webhook
    except Exception:
        return Message("Failed to update webhook", ephemeral=True)
    else:
        return Message("Updated Webhook", ephemeral=True)


@hooks.command("sync")
def sync_webhook(ctx, internal_name: Autocomplete[str]):
    "Fetches the Webhook's data from Discord and updates the database"
    key = f'webhook_{ctx.author.id}_{internal_name}'
    record = database.get(key)
    webhook: Webhook = record.get("hook")
    if webhook is None:
        return Message(f"Webhook `{internal_name}` not found", ephemeral=True)
    try:
        updated = webhook.get()
        record["hook"] = updated
    except Exception:
        return Message("Failed to retrieve or save Webhook", ephemeral=True)
    else:
        return Message("Synced Webhook", ephemeral=True)


@hooks.command("delete")
def delete_webhook(ctx, internal_name: Autocomplete[str], reason: str = None):
    "Delete a Webhook"
    key = f'webhook_{ctx.author.id}_{internal_name}'
    webhook: Webhook = database.get(key).get("hook")
    if webhook is None:
        return Message(f"Webhook `{internal_name}` not found", ephemeral=True)
    try:
        del database[key]
        webhook.delete(reason=reason)
    except Exception:
        return Message("Failed to delete webhook, probably was already deleted", ephemeral=True)
    else:
        return Message("Deleted Webhook", ephemeral=True)


@hooks.command("repeater", annotations={
    "message": "Message to repeat. Leave empty to unset a previously set repeater."
})
def repeat_webhook(ctx, internal_name: Autocomplete[str], message: str = None):
    "Set an existing Webhook to send a message in repeat, or unset"
    key = f'webhook_{ctx.author.id}_{internal_name}'
    if message is None:
        with database[key] as record:
            record["repeat"] = False
            del record["repeat_message"]
        return Message(f"Set Webhook `{internal_name}` not to repeat", ephemeral=True)
    else:
        with database[key] as record:
            record["repeat"] = True
            record["repeat_message"] = message
        return Message(f"Set Webhook `{internal_name}` to repeat {message!r}", ephemeral=True)



@hooks.command("runall")
def send_scheduled_messages_command(ctx: Context):
    "Run all of your Webhooks set on Repeat"
    success = []
    fails = []
    query = Query(
        Field("key").startswith(f"webhook_{ctx.author.id}"),
        Field("repeat") == True,
    )
    for record in database.fetch(query):
        webhook = record["hook"]
        try:
            webhook.send(record["repeat_message"])
            success.append(record["internal_name"])
        except Exception:
            fails.append(record["internal_name"])
    return Message(
        embed=Embed(
            title="Sent messages",
            description="Webhooks that suceeded and failed in sending their messages",
            fields=[
                embed.Field(
                    "Sent sucessfully",
                    ", ".join(success) or "Zero",
                ),
                embed.Field(
                    "Failed to send",
                    ", ".join(fails) or "Zero",
                ),
            ],
        ),
        ephemeral=True,
    )


@invoke_webhook.autocomplete()
@delete_webhook.autocomplete()
@update_webhook.autocomplete()
@sync_webhook.autocomplete()
@repeat_webhook.autocomplete()
@edit_webhook_message.autocomplete()
def webhook_name_autocomplete_handler(ctx, internal_name: Option = None, **_):
    if internal_name is None or not internal_name.focused:
        return []
    key_prefix = f'webhook_{ctx.author.id}_{internal_name.value or ""}'

    options = []
    records = database.fetch(Query(Field("key").startswith(key_prefix)))
    for record in records:
        display = f"{record['internal_name']}: {record['hook'].name}"
        value = record["internal_name"]
        options.append(Choice(name=display, value=value))

    options.sort(key=lambda option: option.name)
    return options[:25]
