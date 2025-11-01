ssh_username = "root"
ssh_host = "ddns.host.com"
local_cache_path = "~/ddns_now_ip.txt"
report_server_path = "~/ddns_now_ip.txt"

client_command = [
    'scp',
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
    '-i', '~/.ssh/key',
    local_cache_path,
    f"{ssh_username}@{ssh_host}:{report_server_path}"
]

client_log_path = "/var/log/ddns_client.log"


# bind server
ddns_conf_path = "~/bind/bind/db.ddns"
ddns_domain = "ddns.bind.domain"
last_update_ip_path = "~/updated_ddns_ip.txt"

server_command = [
    'docker', 'exec', '-i', 'bind', '/etc/init.d/named', 'reload', ddns_domain
]

ddns_config_template = """
$TTL    60
@       IN      SOA     {hostname}. root.{hostname}. (
                {timestamp}; Serial
                300; Refresh
                60; Retry
                86400; Expire
                300
); Negative Cache TTL

@       IN      NS      {hostname}.

@       IN      A       {ip}
"""

server_log_path = "/var/log/ddns_server.log"
