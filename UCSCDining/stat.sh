#!/bin/bash

function getPath(){
python - << END
from UCSCDining import UCSCDining
dining=UCSCDining()
print(dining.get_path())
END
}

path=$(getPath)

echo "################"
echo "#   Telegram   #"
echo "################"
# Telegram stats
echo -n "Queries:       "
cat "$path""telegram_users.txt" | wc -l
echo -n "Unique users:  "
cat "$path""telegram_users.txt" | sort | uniq | wc -l
cat "$path""telegram_users.txt" | sort | uniq -c
echo ""

echo "################"
echo "#   Discord    #"
echo "################"
# Discord stats
echo -n "Queries:       "
cat "$path""discord_users.txt" | wc -l
echo -n "Unique users:  "
cat "$path""discord_users.txt" | sort | uniq | wc -l
cat "$path""discord_users.txt" | sort | uniq -c
echo ""

echo "################"
echo "#     SMS      #"
echo "################"
# SMS stats
echo -n "Queries:       "
cat "$path""sms_users.txt" | wc -l
echo -n "Unique users:  "
cat "$path""sms_users.txt" | sort | uniq | wc -l
cat "$path""sms_users.txt" | sort | uniq -c
