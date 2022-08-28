from .base_autocomplete import dummy_autocomplete

@dummy_autocomplete
def autocomplete_get_note(name):
    return {
        "name": "notes",
        "options": [
            {
                "name": "get",
                "options": [
                    {
                        "focused": True,
                        "name": "name",
                        "type": 3,
                        "value": name
                    }
                ],
                "type": 1
            }
        ],
        "type": 1
    }
