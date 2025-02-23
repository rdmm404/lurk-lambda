import os

import subprocess
import sys
import boto3


def get_telegram_credentials() -> tuple[str, str]:
    token = os.getenv("LURK_TELEGRAM_TOKEN")
    chat_id = os.getenv("LURK_TELEGRAM_CHAT_ID")

    ssm_client = boto3.client("ssm")

    try:
        token = ssm_client.get_parameter(Name=token, WithDecryption=True)
        chat_id = ssm_client.get_parameter(Name=chat_id, WithDecryption=True)
    except Exception as e:
        print(
            f"Something happened while getting the telegram credentials: {e}. Using env vars instead"
        )

    return token, chat_id


def handler(event, context):
    try:
        token, chat_id = get_telegram_credentials()
        print(token, chat_id)
        subprocess.run(
            [sys.executable, "-m", "lurk", "run"],
            check=True,
            env={"LURK_TELEGRAM_TOKEN": token, "LURK_TELEGRAM_CHAT_ID": chat_id},
        )
        return {"statusCode": 200, "body": "Evertything went well"}
    except subprocess.CalledProcessError as e:
        return {"statusCode": 500, "error": e.stderr}
