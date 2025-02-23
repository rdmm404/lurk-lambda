import os

import subprocess
import sys


def get_telegram_credentials() -> tuple[str, str]:
    import boto3
    token = os.getenv("LURK_TELEGRAM_TOKEN")
    chat_id = os.getenv("LURK_TELEGRAM_CHAT_ID")

    ssm_client = boto3.client("ssm")

    try:
        token_response = ssm_client.get_parameter(Name=token, WithDecryption=True)
        chat_id_response = ssm_client.get_parameter(Name=chat_id, WithDecryption=True)

        token = token_response.get("Parameter", {}).get("Value", "")
        chat_id = chat_id_response.get("Parameter", {}).get("Value", "")
    except Exception as e:
        print(
            f"Something happened while getting the telegram credentials: {e}. Using env vars instead"
        )

    return token, chat_id


def handler(event, context):
    try:
        token, chat_id = get_telegram_credentials()
        subprocess.run(
            [sys.executable, "-m", "lurk", "run"],
            check=True,
            env=dict(os.environ, LURK_TELEGRAM_TOKEN=token, LURK_TELEGRAM_CHAT_ID=chat_id),
        )
        return {"statusCode": 200, "body": "Evertything went well"}
    except subprocess.CalledProcessError as e:
        return {"statusCode": 500, "error": e.stderr}
