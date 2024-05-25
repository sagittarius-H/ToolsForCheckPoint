#!/bin/bash -f
source /opt/CPshrd-R81.10/tmp/.CPprofile.sh

#Here we connect as root, this is undocumented API flag -r
mgmt_cli login --port 4434 -r true > credAPI.txt


date >> autoPolicy.log
echo "Automatic policy installation started" >> autoPolicy.log

mgmt_cli install-policy policy-package "Standard" access true threat-prevention true targets.1 "GW8110" -s credAPI.txt >> autoPolicy.log

#mgmt_cli install-policy policy-package "standard" access true threat-prevention true targets.1 "corporate-gateway" targets.2 "corporate-gateway1" targets.3 "corporate-gateway2"

#Close connection
mgmt_cli logout -s credAPI.txt

rm credAPI.txt

exit 0