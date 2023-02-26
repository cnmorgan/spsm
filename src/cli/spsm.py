import click
from server.server_commander import ServerCommander
from jmanager import JarManager, jar_manager
from threading import Thread
from utils.config import load_config

@click.group()
def spsm():
    pass
# ----- Server Functions ----- #
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

# ----- Jarfile Functions ----- #

@spsm.command()
@click.option('-j', '--jarfiles', default=True)
def list(jarfiles):
    if jarfiles:
        jar_manager = JarManager()
        jar_manager.list_jars()
        
@spsm.command()
@click.option('-j', '--jar-name', required=True, type=str)
@click.option('-t', '--type', required=True, type=str)
@click.option('-u', '--source-url', required=False, type=str, default=None)
@click.option('-a', '--apply', is_flag=True, default=False)
def upsert(jar_name, type, source_url, apply):
    jar_manager = JarManager()
    if jar_manager.upsert_jar(jar_name, type, source_url) == -1:
        click.secho("Could not upsert jar!", fg='red')
        return
    
    print(f"Jar: {jar_name} has been added.")
    if apply:
        jar_manager.apply_jar_data()
    else:
        click.secho("Jar data must be applied before server is updated!", fg='yellow')

@spsm.command()
def apply():
    jar_manager = JarManager()
    jar_manager.apply_jar_data()
    
@spsm.command()
@click.option('-a', '--all', default=True)
@click.option('-j', '--jar-name', type=str)
def download(all, jar_name):
    jar_manager = JarManager()
    if jar_name is not None:
        jar_manager.update_jar_file(jar_name)
    elif all:
        jar_manager.update_all_jars()
    else:
        click.secho("Nothing downloaded.")

if __name__ == '__main__':
    spsm()
