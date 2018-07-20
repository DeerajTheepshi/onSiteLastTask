#! /bin/bash

cp onSite.sh /usr/local/bin/siteWork.sh

echo "[Unit]
Description = Sema

[Service]
ExecStart = /usr/local/bin/siteWork.sh

[Install]
WantedBy = multi-user.target" >> /etc/systemd/system/loader.service

chmod 777 /etc/systemd/system/loader.service

echo "[Unit]
Description=Timed
Requires=loader.service

[Timer]

OnUnitActiveSec=1m
Unit=loader.service

[Install]
WantedBy=multi-user.target" >> /etc/systemd/system/timer.timer 

sudo systemctl daemon-reload

sudo systemctl start timer.timer
