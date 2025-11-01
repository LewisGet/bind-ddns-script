import config
from util import module


def update_bind(tools, ip):
    conf = config.ddns_config_template.format(
        hostname = config.ddns_domain,
        timestamp = tools.get_timestamp_str(),
        ip = ip
    )

    tools.set_file_content(config.ddns_conf_path, conf)
    tools.execute_command(config.server_command, "reload bind server")


def main():
    tools = module(config.server_log_path)

    last_ip = tools.get_file_ip(config.last_update_ip_path)
    new_ip = tools.get_file_ip(config.report_server_path)

    if last_ip != new_ip:
        update_bind(tools, new_ip)
        tools.set_file_content(config.last_update_ip_path, new_ip)

    return True

if __name__ == '__main__':
    main()
