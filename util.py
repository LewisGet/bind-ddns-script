import subprocess
from typing import List, Any

from pathlib import Path
from datetime import datetime

import re
import logging
import time

import config


class module:
    def __init__(self, log_path: str):
        self.logger = self.init_logging(log_path)
        self.config = config
        self.private_ip_ranges = (
            re.compile(r'^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$'),
            re.compile(r'^172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}$'),
            re.compile(r'^192\.168\.\d{1,3}\.\d{1,3}$')
        )

    def init_logging(self, log_file) -> logging.Logger:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        return logging.getLogger(__name__)

    def execute_command(
            self,
            command: list, error_message: str,
            check: bool = True, capture_output: bool = True
        ) -> subprocess.CompletedProcess[str]:
        """
        execute fail will log and raise

        :param command: command
        :param error_message: error log prefix
        :param check: check command execute
        :return: any str
        """
        try:
            result = subprocess.run(
                command,
                check=check,
                capture_output=capture_output,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"{error_message} (sub error code: {e.returncode}): {e.stderr.strip()}.")
            raise
        except FileNotFoundError:
            self.logger.error(f"file '{command[0]}' not found.")
            raise
        except Exception as e:
            self.logger.error(f"unknow error: ({error_message}): {e}")
            raise


    def is_valid_ipv4(self, ip: str) -> bool:
        return re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip) is not None

    def is_public_ipv4(self, ip: str) -> bool:
        if ip.startswith('127.'):
            return False

        if not self.is_valid_ipv4(ip):
            return False

        for pattern in self.private_ip_ranges:
            if pattern.match(ip):
                return False

        return True

    def get_public_ipv4(self) -> str | None:
        """
        use hostname -I get ip

        :param logger: logger object
        :return: public ip str or None
        """

        ip_command = ['hostname', '-I']

        stdout = self.execute_command(ip_command, "get public ipv4", check=True)
        ips = stdout.stdout.strip().split()

        for ip in ips:
            if self.is_public_ipv4(ip):
                self.logger.info(f"ip found: {ip}")
                return ip

        return None


    def get_file_content(self, path: str) -> str | None:
        """
        get_file_content

        :param path: path
        :return: str or None
        """
        file_path = Path(path)

        if not file_path.exists():
            return None

        try:
            content = file_path.read_text(encoding='utf-8').strip()
        except IOError as e:
            self.logger.error(f"read io fail, path: {path} ;;; message: {e}")
            return None
        except Exception as e:
            self.logger.error(f"read file unknow error path: {path} ;;; message: {e}")
            return None

        return content

    def set_file_content(self, path: str, content: str) -> bool:
        """
        set file content if fail return False。

        :param path: path
        :param content: content
        :return: bool
        """
        file_path = Path(path)

        try:
            file_path.write_text(content, encoding='utf-8')
        except IOError as e:
            self.logger.error(f"write io fail, path: {path} ;;; message: {e}")
            return False
        except Exception as e:
            self.logger.error(f"write file unknow error path: {path} ;;; message: {e}")
            return False

        return True

    def get_file_ip(self, path: str):
        """get file up"""
        ip = self.get_file_content(path)

        if not self.is_public_ipv4(ip):
            self.logger.error(f"path is not public ip path: {path} ;;; ip: {ip}")
            return None

        return ip

    def get_timestamp_str(self) -> str:
        "get timestamp str"
        return str(int(time.time()))
