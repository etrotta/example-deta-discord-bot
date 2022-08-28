from .base_slash_command import dummy_slash_command

@dummy_slash_command
def hello():
    return {
        "name": "hello",
        "type": 1,
    }
    
