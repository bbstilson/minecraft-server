# !/bin/bash

set -e

echo "Zipping python files."

ZIP_FILE="minecraft_server_state_change.zip"
zip $ZIP_FILE *.py > /dev/null

echo "Pushing zip to lambda."

aws lambda update-function-code \
  --function-name MinecraftServerStateChange \
  --zip-file "fileb://$ZIP_FILE" > /dev/null

rm $ZIP_FILE

echo "Deployed!"
