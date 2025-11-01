import config
from util import module

def main():
    tools = module(config.client_log_path)

    last_ip = tools.get_file_ip(config.local_cache_path)
    now_ip = tools.get_public_ipv4()

    if last_ip != now_ip:
        tools.set_file_content(config.local_cache_path, now_ip)

    tools.execute_command(config.client_command, "update")

    return True

if __name__ == '__main__':
    main()
