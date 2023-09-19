import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime

from .gpo import GPO
from .event import Error, Warning
from .rep import ReportComputer, ReportUser
from .pol import Policy

import ipdb


entity = None


def create_entity(data):
    if str(data["is_machine"]) == "True":
        return ReportComputer(data["username"])
    return ReportUser(data["username"])


def reporting(message_code, data, mess):
    global entity
    mess = str(mess).split("|")[1].strip()

    if not entity:
        if message_code == "D61" or message_code == "D1":
            entity = create_entity(data)
    else:
        if message_code == "I2":
            entity.set_gpo(GPO(data["gpo_name"], data["gpo_uuid"], data["file_sys_path"]))
        elif message_code == "D18":
            entity.domain = data["domain"]
        elif message_code == "D19":
            if data["varname"] == 'machine_name':
                entity.computer_name = data["value"]
        elif message_code == "D91": # firefox
            # p = Policy(data["destfile"], "firefox")
            entity.policies = Policy(data["destfile"], "firefox")
        elif message_code[0] == "W":
            entity.set_warning(Warning(mess, data))
        elif message_code[0] == "E":
            entity.set_error(Error(mess, data))

def save_to_json(full_path, dict_info=None):
    json.dump(dict_info, open(full_path, "w"), ensure_ascii=False)


def save_to_html(full_path, dict_info=None):
    env = Environment(
        loader=FileSystemLoader('/usr/lib/python3/site-packages/gpoa/report/html/templates'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('main.html')
    render_page = template.render(info=dict_info)

    with open(full_path, 'w') as file:
        file.write(render_page)

def save_report(path="~/work"):
    global entity

    report = entity.get_info_dict()
    name = "gpresult_" + str(datetime.now()).replace(' ', '_')

    full_path_json = os.path.join(path, f"{name}.json")
    full_path_html = os.path.join(path, f"{name}.html")
    
    save_to_json(full_path_json, report)
    save_to_html(full_path_html, report)