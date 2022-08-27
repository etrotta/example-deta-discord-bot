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

from informal_testing.dummy_command import (
    create_run_data,
    read_run_data,
    update_run_data,
    delete_run_data,

    creating_modal_response,
    editing_modal_response,
)

steps = [
    create_run_data("test_data", "test description"),
    read_run_data("test_data"),
    update_run_data("test_data", "yooo edited"),
    read_run_data("test_data"),
    delete_run_data("test_data"),
    read_run_data("test_data"),

    creating_modal_response("test_modal", "hello this is coming from a modal :D"),
    read_run_data("test_modal"),
    editing_modal_response("test_modal", "modals can be used to edit too!"),
    read_run_data("test_modal"),
]

with open("test_output.log", "w") as file:
    for (user_interaction, interaction_type) in steps:
        if interaction_type == "RUN_HANDLER":
            result = app.run_handler(user_interaction)
        elif interaction_type == "RUN_COMMAND":
            result = app.run_command(user_interaction)
        else:
            raise ValueError(f"I have no idea what to do with {interaction_type=}."
            " Interaction dummy in question: \n{user_interaction}")
        print(result, end="\n\n")
        file.write(f"{result!r}\n\n")