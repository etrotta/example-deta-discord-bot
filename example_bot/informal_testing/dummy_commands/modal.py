from .base_modal import dummy_modal_submit

@dummy_modal_submit
def set_note_via_modal(name, description):
    return {
        "custom_id": "create_note_modal",
        "components": [
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
    }
