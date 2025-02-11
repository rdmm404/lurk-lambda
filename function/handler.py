import subprocess
import sys


def handler(event, context):
    try:
        subprocess.run(
            [sys.executable, "-m", "lurk", "run"],
            check=True,
        )
        return {"statusCode": 200, "body": "Evertything went well"}
    except subprocess.CalledProcessError as e:
        return {"statusCode": 500, "error": e.stderr}
