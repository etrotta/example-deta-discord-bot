from .base_slash_command import dummy_slash_command


@dummy_slash_command
def create_note(name, description):
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "create",
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
    

@dummy_slash_command
def read_note(name):
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "get",
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
    

@dummy_slash_command
def update_note(name, description):
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "update",
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
    

@dummy_slash_command
def delete_note(name):
    return {
        "name": "notes",
        "type": 1,
        "options": [
            {
                "name": "delete",
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
