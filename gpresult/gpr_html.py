import gettext
import html
import os
import socket
from pathlib import Path

from . import gpr_system

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext

_ASSET_DIR = Path(__file__).resolve().parent / "assets"


def _read_asset(name):
    return (_ASSET_DIR / name).read_text(encoding="utf-8")


CSS = _read_asset("gpr_html.css")
JS = _read_asset("gpr_html.js")

PREF_GROUP_TITLES = {
    "Files": "Files",
    "Folders": "Folders",
    "Inifiles": "Ini Files",
    "Drives": "Drive Maps",
    "Environmentvariables": "Environment",
    "Networkshares": "Network Shares",
    "Shortcuts": "Shortcuts",
}

PREF_GROUP_ORDER = [
    "Files",
    "Folders",
    "Inifiles",
    "Drives",
    "Environmentvariables",
    "Networkshares",
    "Shortcuts",
]


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value))


def esc_js(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def js_strings():
    return (
        'var strShow = "{}";\n'
        'var strHide = "{}";\n'
        'var strShowAll = "{}";\n'
        'var strHideAll = "{}";\n'
        "var strShowHide = 1;\n"
    ).format(
        esc_js(_("show")),
        esc_js(_("hide")),
        esc_js(_("show all")),
        esc_js(_("hide all")),
    )


def fmt(value):
    if value is True:
        return _("Yes")
    if value is False:
        return _("No")
    if value is None or str(value) == "None":
        return "-"
    return str(value)


def section(level, title, inner, expanded=False, h_variant=False):
    cls = f"he{level}"
    if h_variant:
        cls += "h"
    if expanded:
        cls += "_expanded"

    return (
        f'<div class="{cls}"><span class="sectionTitle" tabindex="0">{esc(title)}</span>'
        '<a class="expando" href="#"></a></div>\n'
        f'<div class="container">{inner}</div>\n'
    )


def info_table(rows, css_class="info"):
    out = [f'<table class="{css_class}">']
    for label, value in rows:
        text = fmt(value)
        if text == "-":
            continue
        out.append(
            f"<tr><td><strong>{esc(label)}</strong></td><td>{esc(text)}</td></tr>"
        )
    out.append("</table>")
    return "".join(out)


def extract_domain(gpos):
    for gpo in gpos:
        path = gpo.path or ""
        marker = "gpo_cache/"
        idx = path.find(marker)
        if idx != -1:
            tail = path[idx + len(marker) :]
            return tail.split("/")[0].lower()
    return None


def netbios_domain(gpos):
    domain = extract_domain(gpos)
    return domain.split(".")[0].upper() if domain else None


def qualify(netbios, name):
    return f"{netbios}\\{name}" if netbios else name


def general_section(obj_type, gpos):
    rows = []
    domain = extract_domain(gpos)
    netbios = netbios_domain(gpos)

    if obj_type == "machine":
        host = socket.gethostname().split(".")[0]
        rows.append([_("Computer name"), qualify(netbios, host)])
    else:
        rows.append([_("User name"), qualify(netbios, os.getlogin())])

    rows.append([_("Domain"), domain])

    body = f'<div class="he2i">{info_table(rows)}</div>'
    return section(0, _("General"), body, expanded=True, h_variant=True)


def keys_values_table(kvs, previous=False):
    css_class = "info4" if previous else "info3"
    out = [f'<table class="{css_class}">']

    if previous:
        out.append(
            '<tr><th scope="col">{}</th><th scope="col">{}</th>'
            '<th scope="col">{}</th><th scope="col">{}</th></tr>'.format(
                esc(_("Setting")),
                esc(_("State")),
                esc(_("Previous Value")),
                esc(_("Winning GPO")),
            )
        )
    else:
        out.append(
            '<tr><th scope="col">{}</th><th scope="col">{}</th>'
            '<th scope="col">{}</th></tr>'.format(
                esc(_("Setting")), esc(_("State")), esc(_("Winning GPO"))
            )
        )

    for kv in sorted(kvs, key=lambda x: x.key):
        if previous:
            out.append(
                "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                    esc(kv.key),
                    esc(fmt(kv.value)),
                    esc(fmt(kv.mod_previous_value)),
                    esc(kv.policy_name or "-"),
                )
            )
        else:
            out.append(
                "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                    esc(kv.key), esc(fmt(kv.value)), esc(kv.policy_name or "-")
                )
            )
    out.append("</table>")
    return "".join(out)


def pref_titles(ptype, po):
    if ptype == "Files":
        target = po.targetPath or po.source or po.fromPath or ""
        return (
            _("File") + " (" + _("Target Path") + ": " + str(target) + ")",
            Path(str(target)).name or str(target),
        )
    if ptype == "Folders":
        path = po.path or ""
        return (
            _("Folder") + " (" + _("Path") + ": " + str(path) + ")",
            Path(str(path)).name or str(path),
        )
    if ptype == "Inifiles":
        return (
            _("Ini File")
            + " ("
            + _("File Path")
            + ": "
            + str(po.path or "")
            + ", "
            + _("Section Name")
            + ": "
            + str(po.section or "")
            + ", "
            + _("Property Name")
            + ": "
            + str(po.property or "")
            + ")",
            str(po.property or po.path or ""),
        )
    if ptype == "Drives":
        path = po.path or ""
        return (_("Drive Map") + " (" + str(path) + ")", str(po.label or path))
    if ptype == "Environmentvariables":
        return (_("Environment") + " (" + str(po.name or "") + ")", str(po.name or ""))
    if ptype == "Networkshares":
        return (
            _("Network Share") + " (" + str(po.name or "") + ")",
            str(po.name or ""),
        )
    if ptype == "Shortcuts":
        return (_("Shortcut") + " (" + str(po.name or "") + ")", str(po.name or ""))

    return (str(ptype), str(ptype))


def preference_item(pref):
    po = pref.preference_obj
    item_title, instance = pref_titles(pref.type, po)

    rows = list(po.get_info_list())
    lifecycle = pref.get_lifecycle_info_list()
    if lifecycle:
        rows.extend(lifecycle)

    winning = '<div class="he4i">{}</div>'.format(
        info_table([[_("Winning GPO"), pref.policy_name]])
    )
    general = section(
        4,
        _("General"),
        f'<div class="he4i">{info_table(rows)}</div>',
        h_variant=True,
    )

    intro = (
        '<div class="he4i">'
        + esc(
            _(
                "The following settings have applied to this object. Within "
                "this category, settings nearest the top of the report are "
                "the prevailing settings when resolving conflicts."
            )
        )
        + "</div>"
    )
    instance_inner = winning + general
    instance_section = section(4, instance, instance_inner)

    return section(3, item_title, intro + instance_section)


def preferences_section(gpos):
    grouped = {}
    for gpo in gpos:
        for pref in gpo.preferences:
            grouped.setdefault(pref.type, []).append(pref)

    if not grouped:
        return None

    groups_html = []
    for ptype in PREF_GROUP_ORDER:
        prefs = grouped.get(ptype)
        if not prefs:
            continue
        items = "".join(preference_item(p) for p in prefs)
        title = _(PREF_GROUP_TITLES.get(ptype, ptype))
        groups_html.append(section(2, title, items))

    if not groups_html:
        return None

    return section(
        1, _("Preferences"), "".join(groups_html), expanded=True, h_variant=True
    )


def settings_section(obj_type, gpos, previous=False):
    kvs = []
    for gpo in gpos:
        kvs.extend(gpo.keys_values)

    blocks = []

    if kvs:
        admin = section(
            1,
            _("Administrative Templates"),
            f'<div class="he4i">{keys_values_table(kvs, previous)}</div>',
        )
        blocks.append(section(1, _("Policies"), admin, expanded=True, h_variant=True))

    prefs = preferences_section(gpos)
    if prefs:
        blocks.append(prefs)

    if not blocks:
        return None

    return section(0, _("Settings"), "".join(blocks), expanded=True, h_variant=True)


def gpo_objects_section(gpos):
    seen = set()
    items = []

    for gpo in gpos:
        marker = (gpo.name, gpo.guid)
        if marker in seen:
            continue
        seen.add(marker)

        title = "{} [{}]".format(gpo.name, gpo.guid or "Local")
        rows = [
            [_("Link Location"), gpo.path],
            [_("Revision"), gpo.version],
            ["GUID", gpo.guid],
        ]
        body = f'<div class="he4i">{info_table(rows)}</div>'
        items.append(section(2, title, body))

    if not items:
        return None

    applied = section(
        1, _("Applied GPOs"), "".join(items), expanded=True, h_variant=True
    )
    return section(0, _("Group Policy Objects"), applied, expanded=True, h_variant=True)


def details_section(obj_type, gpos, previous=False):
    gpos_t = [g for g in gpos if g.obj == obj_type]
    if not gpos_t:
        return None

    title = _("Computer Details") if obj_type == "machine" else _("User Details")

    inner = [general_section(obj_type, gpos_t)]

    settings = settings_section(obj_type, gpos_t, previous)
    if settings:
        inner.append(settings)

    objects = gpo_objects_section(gpos_t)
    if objects:
        inner.append(objects)

    return section(0, title, "".join(inner), expanded=True)


def build_report(gpos, obj_type, previous=False):
    netbios = netbios_domain(gpos)
    user = qualify(netbios, os.getlogin())
    host = qualify(netbios, socket.gethostname().split(".")[0])
    name_label = _("{user} on {computer}").format(user=user, computer=host)
    timestamp = gpr_system.get_timestamp()

    parts = [
        '<html dir="ltr">\n<head>\n',
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n',
        f"<title>{esc(name_label)}</title>\n",
        f'<style type="text/css">{CSS}</style>\n',
        f'<script type="text/javascript">{js_strings()}{JS}</script>\n',
        "</head>\n",
        '<body onload="window_onload();" onclick="return document_onclick(event);" '
        'onkeypress="return document_onkeypress(event);">\n',
        '<table class="title">\n',
        '<tr><td colspan="2" class="rsopheader">{}</td></tr>\n'.format(
            esc(_("Group Policy Results"))
        ),
        f'<tr><td colspan="2" class="rsopname">{esc(name_label)}</td></tr>\n',
        '<tr><td id="dtstamp">{} {}</td>'
        '<td><div id="objshowhide" tabindex="0" '
        'onclick="objshowhide_onClick();return false;"></div></td></tr>\n'.format(
            esc(_("Data collected on:")), esc(timestamp)
        ),
        "</table>\n",
        '<div class="rsopsettings">\n',
    ]

    for obj_type_iter in ("machine", "user"):
        if obj_type and obj_type != obj_type_iter:
            continue
        block = details_section(obj_type_iter, gpos, previous)
        if block:
            parts.append(block)

    parts.append("</div>\n</body>\n</html>\n")
    return "".join(parts)


def save(gpos, obj_type, filepath="gpresult.html", previous=False):
    report = build_report(gpos, obj_type, previous)

    with Path(filepath).open("w", encoding="utf-8") as f:
        f.write(report)

    print(_("HTML report saved to {}").format(filepath))
