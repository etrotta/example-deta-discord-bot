from deta_discord_interactions import (
    DiscordInteractionsBlueprint,
    Context,

    Modal,
    ActionRow,
    TextInput,
    TextStyles,

    Message,
    SelectMenu,
    SelectMenuOption,
)
from deta_discord_interactions.utils import Database

blueprint = DiscordInteractionsBlueprint()
database = Database()
def modal(name: str, description: str) -> Modal:
    return Modal(
        "create_note_modal",
        "Create a new note",
        [
            ActionRow(
                [TextInput("note_name", "Name", value=name)],
            ),
            ActionRow(
                [TextInput("note_description", "Description", style=TextStyles.PARAGRAPH, value=description)],
            ),
        ]
    )

notes = blueprint.command_group("notes", "Create and manage your notes")


@notes.command("create", "Add a new note to your collection.")
def add_note(ctx: Context, name: str, description: str):
    user = database[ctx.author]
    user_notes = user.setdefault("notes", {})
    if name in user_notes:
        return Message(f"Note {name} already exists, use `/notes update` or `/notes set` if you want to change it", ephemeral=True)
    user_notes[name] = description
    return Message(f"Registered note {name}", ephemeral=True)


@notes.command("modal", "Opens a model for you to add or edit a note.")
def add_note(ctx: Context, name: str = ''):
    if name:
        user = database[ctx.author]
        user_notes = user.setdefault("notes", {})
        return modal(name, user_notes.get(name, ''))
    else:
        return modal('', '')

@blueprint.custom_handler("create_note_modal")
def save_modal_note(ctx: Context):
    user = database[ctx.author]
    user_notes = user.setdefault("notes", {})
    name = ctx.get_component("note_name").value
    is_update = name in user_notes
    # if name in user_notes:
    #     return Message(f"Note {name} already exists, use `/notes update` if you want to change it", ephemeral=True)
    description = ctx.get_component("note_description").value
    user_notes[name] = description
    # return Message(f"Registered note {name}", ephemeral=True)
    if is_update:
        return Message(f"Updated note {name}", ephemeral=True)
    else:
        return Message(f"Registered note {name}", ephemeral=True)


@notes.command("get", "Retrieve a note from collection.")
def get_note(ctx: Context, name: str):
    user = database[ctx.author]
    return Message(
        user.setdefault("notes", {}).get(name, f"Note {name} not found"),
        ephemeral=True,
    )


@notes.command("list", "List all notes from your collection.")
def list_notes(ctx: Context):
    user = database[ctx.author]
    user_notes = user.setdefault("notes", {})
    if len(user_notes) > 25:
        result = ", ".join(user_notes.keys())
        if len(result) > 1900:
            return Message("You have **way** too many notes to list!", ephemeral=True)
        else:
            return Message(f"You have way too many notes to put in a dropdown menu:\n{result}", ephemeral=True)
    options = []
    for name, description in user_notes.items():
        if len(description) > 100:
            description = description[:97] + "..."
        options.append(
            SelectMenuOption(name, name, description),
        )
    return Message(components=[SelectMenu("notes_list", options, placeholder="Select a note to see it.")], ephemeral=True)


@blueprint.custom_handler("notes_list")
def show_full_note(ctx: Context):
    name = ctx.values[0]
    return Message(
        database[ctx.author]["notes"][name],
        ephemeral=True,
    )
    # NOTE: Add buttons later?
    # Actually can you even add them to an ephemeral message?
    # I might have to un-ephemeral the other one huh...


@notes.command("update")
def update_note(ctx: Context, name: str, description: str):
    "Updates an existing note"
    user = database[ctx.author]
    user_notes = user.setdefault("notes", {})
    if name not in user_notes:
        return Message(f"Note {name} not found. Use `/note create` or `/note set` to add a new one", ephemeral=True)
    elif user_notes[name] == description:
        return Message(f"Note {name} was already set to that", ephemeral=True)
    else:
        user_notes[name] = description
        return Message(f"Note {name} updated", ephemeral=True)


@notes.command("set")
def set_note(ctx: Context, name: str, description: str):
    "Update an existing note or create a new one"
    user = database[ctx.author]
    user_notes = user.setdefault("notes", {})
    is_update = name in user_notes
    user_notes[name] = description
    if is_update:
        return Message(f"Note {name} updated", ephemeral=True)
    else:
        return Message(f"Note {name} registered", ephemeral=True)


@notes.command("delete")
def delete_note(ctx: Context, name: str):
    "Delete an existing note"
    user = database[ctx.author]
    user_notes = user.setdefault("notes", {})
    if name not in user_notes:
        return Message(f"Note {name} not found", ephemeral=True)
    else:
        user_notes.pop(name)
        return Message(f"Note {name} deleted", ephemeral=True)
