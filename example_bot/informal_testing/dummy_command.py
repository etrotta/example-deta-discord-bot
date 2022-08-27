from functools import wraps
import os


COMMON_DUMMY = {
    "app_permissions": "1071698660929",
    "application_id": os.getenv("DISCORD_CLIENT_ID", "123123123"),
    "channel_id": "267624335836053506",
    "guild_id": "267624335836053506",
    "guild_locale": "en-US",
    "id": "1012826765175042098",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2021-10-28T00:29:42.231000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "4398046511103",
        "premium_since": None,
        "roles": [],
        "user": {
            "avatar": "d600588da81eb2266fa35e64fcac857a",
            "avatar_decoration": None,
            "discriminator": "0000",
            "id": "683001325440860340",
            "public_flags": 256,
            "username": "testdummy"
        },
    },
    "token": "...",
    "version": 1,
}

def dummy_slash_command(name):  # Note: I am using subcommands for all of them.
    # You will most likely have to edit some things if you are not
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            options = function(*args, **kwargs)
            return {
                "data": {
                    "guild_id": "267624335836053506",
                    "id": "1012551414855245884",
                    "name": name,
                    "options": options,
                    "type": 1
                },
                "type": 2,
                **COMMON_DUMMY,
            }, "RUN_COMMAND"
        return wrapper
    return decorator


def dummy_modal_submit():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            components = function(*args, **kwargs)
            return {
                "data": {
                    "components": components,
                    "custom_id": "create_note_modal"
                },
                "type": 5,
                **COMMON_DUMMY,
            }, "RUN_HANDLER"
        return wrapper
    return decorator


@dummy_slash_command("notes")
def create_run_data(name, description):
    return [
    {
        "name": "create",
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
        "type": 1
    }
]


@dummy_slash_command("notes")
def read_run_data(name):
    return [
    {
        "name": "get",
        "options": [
            {
                "name": "name",
                "type": 3,
                "value": name
            },
        ],
        "type": 1
    }
]


@dummy_slash_command("notes")
def update_run_data(name, description):
    return [
    {
        "name": "update",
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
        "type": 1
    }
]

@dummy_slash_command("notes")
def delete_run_data(name):
    return [
        {
            "name": "delete",
            "options": [
                {
                    "name": "name",
                    "type": 3,
                    "value": name
                },
            ],
            "type": 1
        }
    ]

@dummy_modal_submit()
def creating_modal_response(name, description):
    return [
        {
            "components": [
                {
                    "custom_id": "note_name",
                    "type": 4,
                    "value": name
                }
            ],
            "type": 1
        },
        {
            "components": [
                {
                    "custom_id": "note_description",
                    "type": 4,
                    "value": description
                }
            ],
            "type": 1
        }
    ]


@dummy_modal_submit()
def editing_modal_response(name, description):
    return [
        {
            "components": [
                {
                    "custom_id": "note_name",
                    "type": 4,
                    "value": name
                }
            ],
            "type": 1
        },
        {
            "components": [
                {
                    "custom_id": "note_description",
                    "type": 4,
                    "value": description
                }
            ],
            "type": 1
        }
    ]


@dummy_slash_command("notes")
def list_all_notes():
    return [
        {
            "name": "list",
            "options": [],
            "type": 1
        }
    ],

@dummy_slash_command("notes")
def open_create_modal():
    return [
        {
            "name": "modal",
            "options": [],
            "type": 1
        }
    ]


@dummy_slash_command("notes")
def open_edit_modal(name):
    return [
        {
            "name": "get",
            "options": [
                {
                    "name": "name",
                    "type": 3,
                    "value": name
                },
            ],
            "type": 1
        }
    ]
