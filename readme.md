# getting start

1. modify `config.py` and setup `crontab -e`
2. client `*/5 * * * * /usr/bin/python3 /path/to/client.py >> /var/log/ddns_client_cron.log 2>&1`
3. server `1,6,11,16,21,26,31,36,41,46,51,56 * * * * /usr/bin/python3 /path/to/server.py >> /var/log/ddns_server_cron.log 2>&1`

