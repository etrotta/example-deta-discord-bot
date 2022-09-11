from deta_discord_interactions import DiscordInteractionsBlueprint
from deta_discord_interactions import Message
from deta_discord_interactions import Context
from deta_discord_interactions import Embed, embed

from deta_discord_interactions.utils.database import Database
from deta_discord_interactions.utils.database import AutoSyncRecord


from deta_discord_interactions.utils.oauth import OAuthToken, OAuthInfo, request_oauth


# NOTE: If you plan to make your Application public,
# be extra careful about how you manage user data and communicate it to your users.
# You may also have to check relevant laws about how and in which ways you can manage user data,
# specially Personally Identificable Information
database = Database(name="oauth_users")

blueprint = DiscordInteractionsBlueprint()

oauth = blueprint.command_group(
    name="oauth",
    description="Give extra permissions to the Application.",
    dm_permission=True,  # requires for you to register commands globally
)


def save_user_info(oauth_token: OAuthToken, ctx: Context):
    key = f'oauth_{ctx.author.id}'
    info: OAuthInfo = oauth_token.get_user_data()
    record: AutoSyncRecord = database.get(key)
    with record:
        record["token"] = oauth_token
        record["info"] = info
        # record.setdefault("history", []).append([oauth_token, info])
    # Do NOT return a Message - this is what the end user will see in their browser
    return f"Registered for user {info.user}"


@oauth.command("register")
def register(ctx: Context, scope: str = 'identify email'):
    "Register to see how the OAuth process works"
    message = request_oauth(ctx, internal_id=f'oauth_{ctx.author.id}', scope=scope, callback=save_user_info)
    return message


@oauth.command("check")
def check_saved_info(ctx: Context):
    "Confirm some of the information we have saved about you"
    # "we" = the bot developer(s). 
    # Needless to say, it is not shared with other library users or the developers.
    key = f'oauth_{ctx.author.id}'
    record = database.get(key)

    token: OAuthToken = record.get("token")
    info: OAuthInfo = record.get("info")
    if info is None:
        return Message("You never registered or deleted your data after last registering.", ephemeral=True)

    fields = [
        embed.Field(
            name="OAuth scopes",
            value=', '.join(token.scope.split(" ")),
        ),
        embed.Field(
            name="OAuth expires",
            value=token.expire_date.isoformat(),
        ),
    ]
    if info.user is not None:
        fields.append(
            embed.Field(
                name="discord ID",
                value=info.user.id,
            ),
        )
        fields.append(
            embed.Field(
                name="discord locale",
                value=info.user.locale,
            ),
        )
        if info.user.email is not None:
            fields.append(
                embed.Field(
                    name="email address",
                    value=info.user.email,
                )
            )

    return Message(
        Embed(
            title="Saved Information",
            description="Some of the data granted by {info.user.username} to {info.application.name}",
            fields=fields,
        ),
        ephemeral=True,
    )


@oauth.command("fullcheck")
def full_check(ctx: Context):
    "Returns ALL information we have saved about you"
    # NOTE: The user themselves must NOT have access to their access_token
    record = database.get(f'oauth_{ctx.author.id}')
    info: OAuthInfo = record.get("info")
    if info is None:
        return Message("We have no data about you", ephemeral=True)
    info.application = "redacted"
    return Message(str(info), ephemeral=True)


@oauth.command("delete", annotations={
    "check_exists": "Check if we even had any data stored before trying to delete it",
})
def delete_oauth(ctx, check_exists: bool = False):
    "Deletes any data we have about your account from our database. Does not revokes the authorization."
    key = f'oauth_{ctx.author.id}'
    if check_exists:
        record = database.get(key)
        if record.get("info") is None:
            return Message("There is no data to delete", ephemeral=True)
        else:
            del database[key]
            return Message("Found and deleted data", ephemeral=True)
    else:
        del database[key]
        return Message("Deleted any data we might've had", ephemeral=True)


@oauth.command("revoke")
def revoke_oauth(ctx):
    "Revokes the access token we have for interacting with your account"
    key = f'oauth_{ctx.author.id}'
    record = database.get(key)
    token: OAuthToken = record.get("token")
    if token is None:
        return Message("We do not have a stored Token to delete", ephemeral=True)
    token.revoke()
    return Message("Revoked the stored access_token. If you wish to delete existing saved data, use `/oauth delete` as well", ephemeral=True)
