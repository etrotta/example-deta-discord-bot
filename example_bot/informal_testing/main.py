import sys
import pathlib

from dotenv import load_dotenv

# Make sure imports work
sys.path.append(str(pathlib.Path(__file__).parent))
sys.path.append(str(pathlib.Path(__file__).parent.parent))
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

# Load any possible `.env` you might have
load_dotenv(pathlib.Path(__file__) / '.env')
load_dotenv(pathlib.Path(__file__).parent / '.env')
load_dotenv(pathlib.Path(__file__).parent.parent / '.env')
load_dotenv(pathlib.Path(__file__).parent.parent.parent / '.env')

from example_bot.main import app

from informal_testing.dummy_commands.hello_world import hello
from informal_testing.dummy_commands.crud import (
    create_note,
    read_note,
    update_note,
    delete_note,
)
from informal_testing.dummy_commands.adv_commands import (
    set_note,
    list_notes,
    open_create_modal,
    open_edit_modal,
)
from informal_testing.dummy_commands.modal import (
    set_note_via_modal,
)
from informal_testing.dummy_commands.notes_autocomplete import (
    autocomplete_get_note,
)


test_hello = [
    hello(),
]

test_crud = [
    read_note("test_data"),
    create_note("test_data", "test description"),
    create_note("hello world", "good morning world"),
    read_note("test_data"),
    update_note("test_data", "yooo edited"),
    read_note("test_data"),
    delete_note("test_data"),
    read_note("test_data"),
]

test_modal = [
    open_create_modal(),
    set_note_via_modal("test", "test123"),
    read_note("test"),
    open_edit_modal("test"),
    set_note_via_modal("test", "abcxyz"),
    read_note("test"),
]

test_adv = [
    create_note("test_data", "test description"),
    create_note("hello world", "good morning world"),
    set_note("hello world", "yooo"),
    set_note("goodbye world", "discord is cool"),
    list_notes(),
]

test_autocomplete = [
    create_note("test 1", "test one"),
    create_note("test 2", "test two"),
    create_note("test 3", "test three"),
    list_notes(),
    autocomplete_get_note("test"),
]

TEST = test_autocomplete

with open(pathlib.Path(__file__).parent / "test_output.log", "w") as file:
    for (user_interaction, interaction_type) in TEST:
        if interaction_type == "RUN_HANDLER":
            result = app.run_handler(user_interaction)
        elif interaction_type == "RUN_COMMAND":
            result = app.run_command(user_interaction)
        elif interaction_type == "RUN_AUTOCOMPLETE":
            result = app.run_autocomplete(user_interaction)
        else:
            raise ValueError(f"I have no idea what to do with {interaction_type=}."
            " Interaction dummy in question: \n{user_interaction}")
        print(result, end="\n\n")
        file.write(f"{result!r}\n\n")