#! /bin/bash

sysMem="$(free -m|awk 'FNR == 2 {print  $3"mb"}')"
sysUsage="$(awk 'FNR==1{usage=($2+$4)*100/($2+$4+$5)}; END{print usage"%"}' /proc/stat)"
sysSpace="$( df -m|awk 'BEGIN{size=0};FNR!=1{size = size+$3};END{print size "mb"}')"
sysCurTime="$(uptime|awk '{print $1}')"
sysUpTime="$(uptime -p|sed 's/up\ //g')"
sysNetWorkCount="$(netstat -na|awk '{print $1}'|wc -l)" ##NEEDS SUDO USER
sysMostUsage="$(ps aux|awk '{print $4, $11}'|sort -k1 -n -r | head -1|awk '{print $2}')"

JSON="{\"memory\":"$sysMem", \"usage\":"$sysUsage", \"space\":"$sysSpace", \"time\":"$sysUpTime", \"netCount\":"$sysNetWorkCount", \"process\":"$sysMostUsage"}"

curl --data "$JSON" http://localhost:9000/postData

echo $JSON


