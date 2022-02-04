from sh import Command, RunningCommand
from json import loads
from time import time
from typing import List, Any


class PM2Process():
    pid: int = 0
    name: str = ""
    pm_id: int = 0
    monit: dict = {}
    autorestart: bool = False
    namespace: str = "default"
    version: str = "N/A"
    mode: str = "fork"
    uptime: int = 0
    created_at: int = 0
    restart: int = 0
    status: str = "online"
    user: str = ""

    def __init__(self, json_data: dict) -> None:
        self.name = json_data["name"]
        if json_data["pid"]:
            self.pid = json_data["pid"]
        if json_data["pm_id"]:
            self.pm_id = json_data["pm_id"]
        self.monit = json_data["monit"]
        self.autorestart = json_data["pm2_env"]["autorestart"]
        self.namespace = json_data["pm2_env"]["namespace"]
        if "versioning" in json_data["pm2_env"]:
            self.version = json_data["pm2_env"]["versioning"]
        self.mode = json_data["pm2_env"]["exec_mode"]
        self.uptime = int(
            time() - round(json_data["pm2_env"]["pm_uptime"] / 1000))
        if json_data["pm2_env"]["created_at"]:
            self.created_at = int(
                round(json_data["pm2_env"]["created_at"] / 1000))
        self.restart = json_data["pm2_env"]["restart_time"]
        self.status = json_data["pm2_env"]["status"]
        self.user = json_data["pm2_env"]["username"]
        self.json_data = json_data

    def __str__(self):
        return f"{self.name} - {self.pid} - {self.status}"

    def __repr__(self):
        return f"<PM2Process {self.name} ({self.pid}) ({self.status})>"


class PM2:
    COMMAND_NAME = "pm2"

    def __init__(self, extra_args=["--no-color", "--mini-list"]) -> None:
        self.command = Command(self.COMMAND_NAME)
        self.extra_args = extra_args

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.command(*args, **kwds)

    def list(self) -> List[PM2Process]:
        command: RunningCommand = self.command.jlist().wait()
        result = []
        for process in loads(command.stdout.decode("utf-8")):
            result.append(PM2Process(process))
        return result

    def start(self, name, extra_args=[]) -> bool:
        command: RunningCommand = self.command.start(
            name, *self.extra_args, *extra_args)
        self.lines = command.stdout.decode("utf-8").splitlines()
        return (self.lines[0].startswith("[PM2] Starting") or self.lines[0].startswith("[PM2] cron restart at")) and self.lines[2 if self.lines[0].startswith("[PM2] cron restart at") else 1].startswith("[PM2] Done.")

    def stop(self, name, extra_args=[]) -> bool:
        command: RunningCommand = self.command.stop(
            name, *self.extra_args, *extra_args)
        self.lines = command.stdout.decode("utf-8").splitlines()
        return self.lines[1].endswith("✓")

    def restart(self, name, extra_args=[]) -> bool:
        command: RunningCommand = self.command.restart(
            name, *self.extra_args, *extra_args)
        self.lines = command.stdout.decode("utf-8").splitlines()
        return self.lines[2 if self.lines[0].startswith("Use --update-env to update environment") else 1].endswith("✓")

    def delete(self, name, extra_args=[]) -> bool:
        command: RunningCommand = self.command.delete(
            name, *self.extra_args, *extra_args)
        self.lines = command.stdout.decode("utf-8").splitlines()
        return self.lines[1].endswith("✓")

    def logs(self, function, name="", extra_args=["--json"]) -> str:
        command: RunningCommand = self.command.logs(
            name, *self.extra_args, *extra_args, _iter=True)
        for line in command:
            function(loads(line))
