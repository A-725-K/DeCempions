#!/bin/bash

SEASON=2022-2023

# flask init-db

# curl -i -X POST 'http://localhost:16000/admin/import-teams' \
# --data-binary "@data/$SEASON/squadre.json" -H 'DC-Token: 1234' \
# -H 'Content-Type: application/json'

# curl -i -X POST 'http://localhost:16000/admin/import-league' \
# --data-binary "@data/$SEASON/campionato.json" -H 'DC-Token: 1234' \
# -H 'Content-Type: application/json'

# for i in `seq 1 30`; do
i=12
echo -e "\n#################################"
echo "########## GIORNATA $i ##########"
echo -e "#################################\n"
curl -i -X POST 'http://localhost:16000/admin/import-week-results' \
--data-binary "@data/$SEASON/giornata_$i.json" -H 'DC-Token: 1234' \
-H 'Content-Type: application/json'
# done