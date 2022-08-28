from .base_slash_command import dummy_slash_command

@dummy_slash_command
def set_note(name, description):
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "set",
                "type": 1,
                "options": [
                    {
                        "name": "name",
                        "type": 3,
                        "value": name
                    },
                    {
                        "name": "description",
                        "type": 3,
                        "value": description
                    }
                ],
            }
        ]
    }

from .base_slash_command import dummy_slash_command

@dummy_slash_command
def list_notes():
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "list",
                "type": 1,
                "options": [],
            }
        ]
    }


@dummy_slash_command
def open_create_modal():
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "modal",
                "type": 1,
                "options": [],
            }
        ]
    }


@dummy_slash_command
def open_edit_modal(name):
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "modal",
                "type": 1,
                "options": [
                    {
                        "name": "name",
                        "type": 3,
                        "value": name
                    },
                ],
            }
        ]
    }
