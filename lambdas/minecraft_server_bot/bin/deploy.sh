# !/bin/bash

set -e

echo "Zipping python files."

ZIP_FILE="minecraft_server_bot.zip"
zip $ZIP_FILE *.py > /dev/null

echo "Pushing zip to lambda."

aws lambda update-function-code \
  --function-name MinecraftServerBot \
  --zip-file "fileb://$ZIP_FILE" > /dev/null

rm $ZIP_FILE

echo "Deployed!"
