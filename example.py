from pm2py import PM2

pm2 = PM2()

pm2.delete("all")  #  delete all processes

pm2.start("tests/test_script.py", ["-f"])
pm2.start("tests/test_script2.py", ["--name", "erkinbaba", "-f"])

for process in pm2.list():
    if process.status == "online":
        print("PROCESS ONLINE: " + process.name)
    else:
        print(f"PROCESS {process.status.upper()}: " + process.name)


def logger(process):
    print(
        f"{'>' if process['type'] == 'out' else '<'} | {process['app_name']} | {process['message']}")


pm2.logs(logger)  # sync method, will work until complete
