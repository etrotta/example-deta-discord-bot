import os

USER_DUMMY = {
    "avatar": "d600588da81eb2266fa35e64fcac857a",
    "avatar_decoration": None,
    "discriminator": "0000",
    "id": "683001325440860340",
    "public_flags": 256,
    "username": "testdummy"
}

MEMBER_DUMMY = {
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
    "user": USER_DUMMY,
}

COMMON_INTERACTION_DUMMY = {
    "app_permissions": "1071698660929",
    "application_id": os.getenv("DISCORD_CLIENT_ID", "123123123"),
    "channel_id": "267624335836053506",
    "guild_id": "267624335836053506",
    "guild_locale": "en-US",
    "id": "1012826765175042098",
    "locale": "en-GB",
    "member": MEMBER_DUMMY,
    "token": "...",
    "version": 1,
}
