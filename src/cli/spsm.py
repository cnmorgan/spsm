import click
from server.server_commander import ServerCommander
from threading import Thread
from utils.config import load_config

@click.group()
def spsm():
    pass

@spsm.command()
@click.option('-a', '--attach', is_flag=True, help='Immediately attach to the activated server')
@click.option('-d', '--debug', is_flag=True, help='Toggles debug mode')
def activate(attach, debug):
    """Activates the Minecraft server and opens the console."""
    config = load_config()
    commander = ServerCommander(config)
    commander.activate_server(debug)
    if attach:
        commander.attach_server()

@spsm.command()
def start():
    config = load_config()
    commander = ServerCommander(config)
    commander.start_server()

@spsm.command()
def console():
    config = load_config()
    commander = ServerCommander(config)
    commander.attach_server()

@spsm.command()
def stop():
    config = load_config()
    commander = ServerCommander(config)
    commander.stop_server()


@spsm.command()
def restart():
    config = load_config()
    commander = ServerCommander(config)
    commander.restart_server()


@spsm.command()
@click.argument('command')
def send(command):
    config = load_config()
    commander = ServerCommander(config)
    commander.send_command(command)


@spsm.command()
def logs():
    config = load_config()
    commander = ServerCommander(config)
    Thread(target=commander.tail_logs).start()


if __name__ == '__main__':
    spsm()
