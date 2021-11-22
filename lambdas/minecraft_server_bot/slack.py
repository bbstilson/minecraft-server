import json


def respond(text: str, quiet: bool = False):
    return {
        "statusCode": "200",
        "body": json.dumps(
            {
                "response_type": "ephemeral" if quiet else "in_channel",
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": text},
                    }
                ],
            }
        ).encode("utf8"),
        "headers": {
            "Content-Type": "application/json",
        },
    }
