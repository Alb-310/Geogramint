__version__ = "v1.3"

import codecs
import os
import shutil
import typer
import pandas as pd

from rich.console import Console
from rich.table import Table
from CLI import settings_cli, ressources_cli
from CLI.TelegramAPIRequests_CLI import geolocate_AllEntities_Nearby
from CLI import surveillance_cli
import json
import time
import difflib
from datetime import datetime, timedelta
import random

logo_ascii = """
\033[38;5;172;49m___________________________________________________\033[1;0m\n
\033[1;0m|                                                 |
\033[1;0m|                \033[38;5;172;49m▄ ████████████  ▄\033[1;0m                |
\033[1;0m|            \033[38;5;172;49m▄██████████████████████\033[1;0m              |
\033[1;0m|           \033[38;5;172;49m███████████████████████████\033[1;0m           |
\033[1;0m|        \033[38;5;172;49m████████████████████████████████\033[1;0m         |
\033[1;0m|      \033[38;5;172;49m,██████████████████████████████████\033[1;0m        |
\033[1;0m|     \033[38;5;172;49m▄███████████████████████\033[1;47m      ████████\033[1;0m      |
\033[1;0m|     \033[38;5;172;49m███████████████████\033[1;47m          █████████\033[1;0m      |
\033[1;0m|    \033[38;5;172;49m███████████████\033[1;47m      ,██     ███████████\033[1;0m     |
\033[1;0m|    \033[38;5;172;49m█████████\033[1;47m          ███       ███████████\033[1;0m     |
\033[1;0m|    \033[38;5;172;49m██████\033[1;47m          ████        ████████████\033[1;0m     |
\033[1;0m|    \033[38;5;172;49m██████████\033[1;47m  █████           ████████████\033[1;0m     |
\033[1;0m|     \033[38;5;172;49m███████████████\033[1;47m            ███████████\033[1;0m      |
\033[1;0m|      \033[38;5;172;49m█████████████████\033[1;47m         ███████████\033[1;0m      |
\033[1;0m|       \033[38;5;172;49m███████████████████\033[1;47m     ███████████\033[1;0m       |
\033[1;0m|        \033[38;5;172;49m████████████████████████████████\033[1;0m         |
\033[1;0m|          \033[38;5;172;49m████████████████████████████\033[1;0m           |
\033[1;0m|             \033[38;5;172;49m███████████████████████▀\033[1;0m            |
\033[1;0m|                 \033[38;5;172;49m███████████████\033[1;0m                 |
\033[38;5;172;49m___________________________________________________\033[1;0m\n
"""

CLI = typer.Typer(rich_markup_mode="rich", help=logo_ascii)
console = Console()


def version_callback(value: bool):
    if value:
        typer.echo(f"{__version__}")
        raise typer.Exit()


@CLI.callback()
def version(
        version: bool = typer.Option(
            False, "--version", help="Show the version", callback=version_callback
        )
):
    pass


@CLI.command(rich_help_panel='Config Commands')
def set_hash(hash: str):
    api_id, api_hash, phone_number, extended_report = settings_cli.loadConfig()
    settings_cli.saveConfig(api_id, hash, phone_number, extended_report)
    typer.echo(typer.style("API_Hash Updated !", fg=typer.colors.GREEN, bold=True))


@CLI.command(rich_help_panel='Config Commands')
def set_id(id: int):
    api_id, api_hash, phone_number, extended_report = settings_cli.loadConfig()
    settings_cli.saveConfig(id, api_hash, phone_number, extended_report)
    typer.echo(typer.style("API_ID Updated !", fg=typer.colors.GREEN, bold=True))


@CLI.command(rich_help_panel='Config Commands')
def set_phone(phone: str):
    api_id, api_hash, phone_number, extended_report = settings_cli.loadConfig()
    settings_cli.saveConfig(api_id, api_hash, phone, extended_report)
    typer.echo(typer.style("Phone Number Updated !", fg=typer.colors.GREEN, bold=True))


@CLI.command(rich_help_panel='Config Commands')
def set_report_settings(extended_report: bool = typer.Option(False, help="enable or disable extended report")):
    api_id, api_hash, phone_number, report = settings_cli.loadConfig()
    settings_cli.saveConfig(api_id, api_hash, phone_number, extended_report)
    if extended_report:
        typer.echo(typer.style("Extended Report Set !", fg=typer.colors.GREEN, bold=True))
    else:
        typer.echo(typer.style("Extended Report Unset !", fg=typer.colors.GREEN, bold=True))


@CLI.command(rich_help_panel='Config Commands')
def set_config(id: int, hash: str, phone: str, extended_report: bool = typer.Option(False, help="enable or disable "
                                                                                                "extended report")):
    settings_cli.saveConfig(id, hash, phone, extended_report)
    typer.echo(typer.style("Config Updated !", fg=typer.colors.GREEN, bold=True))


@CLI.command(rich_help_panel='Actions Commands')
def start_scan(lat: float, lon: float, output_json: str = typer.Option("cache_telegram", help="Directory Path"),
               output_csv: str = typer.Option("", help="Directory Path"),
               output_pdf: str = typer.Option("", help="Directory Path"),
               output_osintracker: str = typer.Option("", help="Directory Path"),
               profile_pictures: bool = typer.Option(True, help="enable or disable profile pictures download")):
    print(logo_ascii)
    api_id, api_hash, phone_number, extended_report = settings_cli.loadConfig()
    typer.echo(typer.style("Config Loaded !", fg=typer.colors.GREEN, bold=True))

    users, groups, dt_string = geolocate_AllEntities_Nearby(api_id, api_hash, lat, lon, profile_pictures)

    if output_json[-1] == '/':
        output_json = output_json[:-1]
    json_string_user = json.dumps([ob.__dict__() for ob in users], ensure_ascii=False)
    with codecs.open(output_json + '/users.json', 'w', 'utf-8') as f:
        f.write(json_string_user)
    json_string_group = json.dumps([ob.__dict__() for ob in groups], ensure_ascii=False)
    with codecs.open(output_json + '/groups.json', 'w', 'utf-8') as f:
        f.write(json_string_group)
    if output_csv != "":
        if output_csv[-1] == '/':
            output_csv = output_csv[:-1]
        df = pd.read_json(output_json + '/users.json')
        df.to_csv(output_csv + '/users.csv', index=None)
        df = pd.read_json(output_json + '/groups.json')
        df.to_csv(output_csv + '/groups.csv', index=None)

    console.print("[orange1]Users detected :")
    table = Table("ID", "First Name", "Last Name", "Username", "Phone", "Distance")
    for elm in users:
        if elm.distance == '500':
            color = '[bright_green]'
        elif elm.distance == '1000':
            color = '[khaki1]'
        elif elm.distance == '2000':
            color = '[orange1]'
        else:
            color = '[indian_red]'

        if elm.lastname is not None:
            lastname = color + elm.lastname[1:-1]
        else:
            lastname = ""
        if elm.username is not None:
            username = color + elm.username[1:-1]
        else:
            username = ""
        if elm.phone is not None:
            phone = color + '+' + elm.phone[1:-1]
        else:
            phone = ""
        table.add_row(color + elm.id, color + elm.firstname[1:-1], lastname, username,
                      phone, color + elm.distance)
    console.print(table)
    console.print("[grey93]Groups detected :")
    table_g = Table("ID", "Name", "Distance")
    for elm in groups:
        if elm.distance == '500':
            color = '[bright_green]'
        elif elm.distance == '1000':
            color = '[khaki1]'
        elif elm.distance == '2000':
            color = '[orange1]'
        else:
            color = '[indian_red]'

        table_g.add_row(color + elm.id, color + elm.name[1:-1], color + elm.distance)
    console.print(table_g)

    if output_pdf != "":
        if output_pdf[-1] == '/':
            output_pdf = output_pdf[:-1]
        ressources_cli.generate_pdf_report(users, groups, lat, lon, dt_string, output_pdf, extended_report)

    if output_osintracker != "":
        if output_osintracker[-1] == '/':
            output_osintracker = output_osintracker[:-1]
        ressources_cli.generate_osintracker_investigation(users, groups, lat, lon, output_osintracker, extended_report)


@CLI.command(rich_help_panel='Actions Commands')
def reset_scan():
    shutil.rmtree("cache_telegram", ignore_errors=True)
    shutil.rmtree("cache", ignore_errors=True)
    if os.path.exists("geckodriver.log"):
        os.remove("geckodriver.log")
    typer.echo(typer.style("cache_telegram deleted", fg=typer.colors.RED, bold=True))


@CLI.command(rich_help_panel='Actions Commands')
def surveillance(lat: float, lon: float, num_days: int = typer.Argument(help="Days of Active Surveillance"),
                 webhook: str = typer.Argument(help="Discord Webhook url")):
    """
    EXPERIMENTAL FEATURE : Work In Progress
    This command aims to permit its user to establish a surveillance on an area using Geogramint.
    The tool will launch scan every ~1h and retrieve all users and compare it with its previous scan.
    If changes are detected, the results will be sent to through the discord webhook.
    """
    print(logo_ascii)
    api_id, api_hash, phone_number, extended_report = settings_cli.loadConfig()
    typer.echo(typer.style("Config Loaded !", fg=typer.colors.GREEN, bold=True))

    end_date = datetime.now() + timedelta(days=num_days)
    previous_output = ""

    while datetime.now() < end_date:

        users, groups, dt_string = geolocate_AllEntities_Nearby(api_id, api_hash, lat, lon, True)
        ressources_cli.generate_pdf_report(users, groups, lat, lon, dt_string, "cache_telegram", False)

        json_string_user = json.dumps([ob.__dict__() for ob in users], ensure_ascii=False)
        with codecs.open('cache_telegram/users.json', 'w', 'utf-8') as f:
            f.write(json_string_user)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_output_filename = f"cache_telegram/sorted_users_{timestamp}.txt"

        surveillance_cli.process_users("cache_telegram/users.json", new_output_filename)

        with open(new_output_filename, "r", encoding="utf-8") as new_output_file:
            new_output = new_output_file.readlines()

        diff = difflib.unified_diff(previous_output, new_output, lineterm="")
        diff_text = "\n".join(diff)
        if diff_text:
            notification = f"Movement found at {timestamp}:\n{diff_text}"
            print(notification)
            surveillance_cli.send_webhook_notification(webhook, notification, None)
            with open(f"cache_telegram/Report_{str(lat)},{str(lon)}.pdf", "rb") as pdf_file:
                files = {"file": ("Report.pdf", pdf_file)}
                surveillance_cli.send_webhook_notification(webhook, notification, files)
        else:
            print(f"No Movement at {timestamp}")

        previous_output = new_output

        shutil.rmtree("cache_telegram/users/", ignore_errors=True)
        shutil.rmtree("cache_telegram/groups/", ignore_errors=True)
        shutil.rmtree("cache_telegram/reportfiles/", ignore_errors=True)
        shutil.rmtree("cache", ignore_errors=True)
        time.sleep(3600 + random.randint(0, 60))  # Sleep for an hour with random seconds to diminish the risks of
                                                  # ban by Telegram

    shutil.rmtree("cache_telegram", ignore_errors=True)
    shutil.rmtree("cache", ignore_errors=True)
