import gettext
import html
import os
import socket

from . import gpr_system

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext

CSS = """
                body    { background-color:#FFFFFF; border:1px solid #666666; color:#000000; font-size:68%; font-family:MS Shell Dlg, sans-serif; margin:0 0 10px 0; word-break:normal; word-wrap:break-word; }
                table   { font-size:100%; table-layout:fixed; width:100%; }
                td,th   { overflow:visible; text-align:left; vertical-align:top; white-space:normal; }
                .title  { background:#FFFFFF; border:none; color:#333333; display:inline-table; height:24px; margin:0px 0px 0px 0px; padding-top:0px; position:relative; table-layout:fixed; z-index:5; }
                .he0_expanded    { background-color:#FEF7D6; border:1px solid #BBBBBB; color:#3333CC; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:0px; margin-right:0px; padding-left:8px; padding-right:5em; padding-top:4px; position:relative; }
                .he1_expanded    { background-color:#A0BACB; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:20px; margin-right:0px; padding-left:8px; padding-right:5em; padding-top:4px; position:relative; }
                .he0h_expanded   { background-color: #FEF0D0; border: 1px solid #BBBBBB; color: #000000; cursor: pointer; display: block; font-family: MS Shell Dlg, sans-serif; font-size: 100%; font-weight: bold; height: 2.25em; margin-bottom: -1px; margin-left: 5px; margin-right: 0px; padding-left: 8px; padding-right: 5em; padding-top: 4px; position: relative;  }
                .he1h_expanded   { background-color: #7197B3; border: 1px solid #BBBBBB; color: #000000; cursor: pointer; display: block; font-family: MS Shell Dlg, sans-serif; font-size: 100%; font-weight: bold; height: 2.25em; margin-bottom: -1px; margin-left: 10px; margin-right: 0px; padding-left: 8px; padding-right: 5em; padding-top: 4px; position: relative; }
                .he1    { background-color:#A0BACB; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:20px; margin-right:0px; padding-left:8px; padding-right:5em; padding-top:4px; position:relative; }
                .he2    { background-color:#C0D2DE; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:30px; margin-right:0px; padding-left:8px; padding-right:5em; padding-top:4px; position:relative; }
                .he3    { background-color:#D9E3EA; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:40px; margin-right:0px; padding-left:11px; padding-right:5em; padding-top:4px; position:relative; }
                .he4    { background-color:#E8E8E8; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:50px; margin-right:0px; padding-left:11px; padding-right:5em; padding-top:4px; position:relative; }
                .he4h   { background-color:#E8E8E8; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:55px; margin-right:0px; padding-left:11px; padding-right:5em; padding-top:4px; position:relative; }
                .he4i   { background-color:#F9F9F9; border:1px solid #BBBBBB; color:#000000; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; margin-bottom:-1px; margin-left:55px; margin-right:0px; padding-bottom:5px; padding-left:21px; padding-top:4px; position:relative; }
                .he2i   { background-color:#F9F9F9; border:1px solid #BBBBBB; color:#000000; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; margin-bottom:-1px; margin-left:35px; margin-right:0px; padding-bottom:5px; padding-left:21px; padding-top:4px; position:relative;}
                .he5    { background-color:#E8E8E8; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; height:2.25em; margin-bottom:-1px; margin-left:60px; margin-right:0px; padding-left:11px; padding-right:5em; padding-top:4px; position:relative; }
                .he5h   { background-color:#E8E8E8; border:1px solid #BBBBBB; color:#000000; cursor:pointer; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; padding-left:11px; padding-right:5em; padding-top:4px; margin-bottom:-1px; margin-left:65px; margin-right:0px; position:relative; }
                .he5i   { background-color:#F9F9F9; border:1px solid #BBBBBB; color:#000000; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; margin-bottom:-1px; margin-left:65px; margin-right:0px; padding-left:21px; padding-bottom:5px; padding-top: 4px; position:relative; }
                div .expando { color:#000000; text-decoration:none; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:normal; position:absolute; right:10px; text-decoration:underline; z-index: 0; }
                .he0 .expando { font-size:100%; }
                .info, .info3, .info4, .disalign  { line-height:1.6em; padding:0px 0px 0px 0px; margin:0px 0px 0px 0px; }
                .disalign TD                      { padding-bottom:5px; padding-right:10px; }
                .info TD                          { padding-right:10px; width:50%; }
                .info3 TD                         { padding-right:10px; width:33%; }
                .info4 TD, .info4 TH              { padding-right:10px; width:25%; }
                .info TH, .info3 TH, .info4 TH, .disalign TH { border-bottom:1px solid #CCCCCC; padding-right:10px; }
                .subtable, .subtable3             { border:1px solid #CCCCCC; margin-left:0px; background:#FFFFFF; margin-bottom:10px; }
                .subtable TD, .subtable3 TD       { padding-left:10px; padding-right:5px; padding-top:3px; padding-bottom:3px; line-height:1.1em; }
                .subtable TH, .subtable3 TH       { border-bottom:1px solid #CCCCCC; font-weight:normal; padding-left:10px; line-height:1.6em;  }
                .subtable .footnote               { border-top:1px solid #CCCCCC; }
                .subtable3 .footnote, .subtable .footnote { border-top:1px solid #CCCCCC; }
                .subtable_frame     { background:#D9E3EA; border:1px solid #CCCCCC; margin-bottom:10px; margin-left:15px; }
                .subtable_frame TD  { line-height:1.1em; padding-bottom:3px; padding-left:10px; padding-right:15px; padding-top:3px; }
                .subtable_frame TH  { border-bottom:1px solid #CCCCCC; font-weight:normal; padding-left:10px; line-height:1.6em; }
                .subtableInnerHead { border-bottom:1px solid #CCCCCC; border-top:1px solid #CCCCCC; }
                .explainlink            { color:#0000FF; text-decoration:none; cursor:pointer; }
                .explainlink:hover      { color:#0000FF; text-decoration:underline; }
                .spacer { background:transparent; border:1px solid #BBBBBB; color:#FFFFFF; display:block; font-family:MS Shell Dlg, sans-serif; font-size:100%; height:10px; margin-bottom:-1px; margin-left:43px; margin-right:0px; padding-top: 4px; position:relative; }
                .filler { background:transparent; border:none; color:#FFFFFF; display:block; font:100% MS Shell Dlg, sans-serif; line-height:8px; margin-bottom:-1px; margin-left:53px; margin-right:0px; padding-top:4px; position:relative; }
                .container { display:block; position:relative; }
                .rsopheader { background-color:#A0BACB; border-bottom:1px solid black; color:#333333; font-family:MS Shell Dlg, sans-serif; font-size:130%; font-weight:bold; padding-bottom:5px; text-align:center; }
                .rsopname { color:#333333; font-family:MS Shell Dlg, sans-serif; font-size:130%; font-weight:bold; padding-left:11px; }
                #dtstamp{ color:#333333; font-family:MS Shell Dlg, sans-serif; font-size:100%; padding-left:11px; text-align:left; width:30%; }
                #objshowhide { color:#000000; cursor:pointer; font-family:MS Shell Dlg, sans-serif; font-size:100%; font-weight:bold; margin-right:0px; padding-right:10px; text-align:right; text-decoration:underline; z-index:2; word-wrap:normal; }
                @media print {
                    #objshowhide{ display:none; }
                    body    { color:#000000; border:1px solid #000000; }
                    .title  { color:#000000; border:1px solid #000000; }
                    .he0_expanded    { color:#000000; border:1px solid #000000; }
                    .he1h_expanded   { color:#000000; border:1px solid #000000; }
                    .he1_expanded    { color:#000000; border:1px solid #000000; }
                    .he1    { color:#000000; border:1px solid #000000; }
                    .he2    { color:#000000; background:#EEEEEE; border:1px solid #000000; }
                    .he3    { color:#000000; border:1px solid #000000; }
                    .he4    { color:#000000; border:1px solid #000000; }
                    .he4h   { color:#000000; border:1px solid #000000; }
                    .he4i   { color:#000000; border:1px solid #000000; }
                    .he5    { color:#000000; border:1px solid #000000; }
                    .he5h   { color:#000000; border:1px solid #000000; }
                    .he5i   { color:#000000; border:1px solid #000000; }
                    }
"""

JS = """
function IsSectionHeader(obj) {
    var c = obj.className;
    return (c === "he0_expanded") || (c === "he0h_expanded") || (c === "he1h_expanded") ||
           (c === "he1_expanded") || (c === "he1") || (c === "he2") || (c === "he3") ||
           (c === "he4") || (c === "he4h") || (c === "he5") || (c === "he5h");
}

function IsSectionExpandedByDefault(objHeader) {
    if (objHeader === null) {
        return false;
    }
    return (objHeader.className.slice(objHeader.className.lastIndexOf("_")) === "_expanded");
}

function GetContainer(objHeader) {
    var node = objHeader.nextSibling;
    while (node && (node.nodeType !== 1 || node.className !== "container")) {
        node = node.nextSibling;
    }
    return node;
}

function GetExpando(objHeader) {
    var links = objHeader.getElementsByTagName("a");
    return links.length ? links[0] : null;
}

function SetSectionState(objHeader, strState) {
    var objContainer = GetContainer(objHeader);
    if (!objContainer) {
        return;
    }
    var objExpando = GetExpando(objHeader);

    if (strState === "toggle") {
        SetSectionState(objHeader, objContainer.style.display === "none" ? "show" : "hide");
        return;
    }
    if (strState === "show") {
        objContainer.style.display = "block";
        if (objExpando) { objExpando.innerHTML = strHide; }
    } else if (strState === "hide") {
        objContainer.style.display = "none";
        if (objExpando) { objExpando.innerHTML = strShow; }
    }
}

function ShowSection(objHeader) { SetSectionState(objHeader, "show"); }
function HideSection(objHeader) { SetSectionState(objHeader, "hide"); }
function ToggleSection(objHeader) { SetSectionState(objHeader, "toggle"); }

function objshowhide_onClick() {
    var objBody = document.body.getElementsByTagName("*");
    var i;
    if (strShowHide === 0) {
        strShowHide = 1;
        document.getElementById("objshowhide").innerHTML = strShowAll;
        for (i = 0; i < objBody.length; i++) {
            if (IsSectionHeader(objBody[i])) { HideSection(objBody[i]); }
        }
    } else {
        strShowHide = 0;
        document.getElementById("objshowhide").innerHTML = strHideAll;
        for (i = 0; i < objBody.length; i++) {
            if (IsSectionHeader(objBody[i])) { ShowSection(objBody[i]); }
        }
    }
}

function window_onload() {
    var objBody = document.body.getElementsByTagName("*");
    for (var i = 0; i < objBody.length; i++) {
        if (IsSectionHeader(objBody[i])) {
            if (IsSectionExpandedByDefault(objBody[i])) {
                ShowSection(objBody[i]);
            } else {
                HideSection(objBody[i]);
            }
        }
    }
    document.getElementById("objshowhide").innerHTML = strShowAll;
}

function GetEventTarget(e) {
    e = e || window.event;
    return e.target || e.srcElement;
}

function GetHeaderFrom(target) {
    while (target && (target.className === "sectionTitle" || target.className === "expando")) {
        target = target.parentNode;
    }
    return target;
}

function document_onclick(e) {
    e = e || window.event;
    var target = GetHeaderFrom(GetEventTarget(e));
    if (!target || !IsSectionHeader(target)) {
        return true;
    }
    ToggleSection(target);
    if (e.preventDefault) { e.preventDefault(); }
    return false;
}

function document_onkeypress(e) {
    e = e || window.event;
    var chCode = ("charCode" in e) ? e.charCode : e.keyCode;
    if (chCode === 32 || chCode === 13 || chCode === 10) {
        var target = GetEventTarget(e);
        if (target.className === "expando" || target.className === "sectionTitle") {
            var header = GetHeaderFrom(target);
            if (header && IsSectionHeader(header)) { ToggleSection(header); }
            if (e.preventDefault) { e.preventDefault(); }
            return false;
        }
        if (target.id === "objshowhide") {
            objshowhide_onClick();
            if (e.preventDefault) { e.preventDefault(); }
            return false;
        }
    }
    return true;
}
"""

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
    cls = "he{}".format(level)
    if h_variant:
        cls += "h"
    if expanded:
        cls += "_expanded"

    return (
        '<div class="{cls}"><span class="sectionTitle" tabindex="0">{title}</span>'
        '<a class="expando" href="#"></a></div>\n'
        '<div class="container">{inner}</div>\n'
    ).format(cls=cls, title=esc(title), inner=inner)


def info_table(rows, css_class="info"):
    out = ['<table class="{}">'.format(css_class)]
    for label, value in rows:
        text = fmt(value)
        if text == "-":
            continue
        out.append(
            "<tr><td><strong>{}</strong></td><td>{}</td></tr>".format(
                esc(label), esc(text)
            )
        )
    out.append("</table>")
    return "".join(out)


def extract_domain(gpos):
    for gpo in gpos:
        path = gpo.path or ""
        marker = "gpo_cache/"
        idx = path.find(marker)
        if idx != -1:
            tail = path[idx + len(marker):]
            return tail.split("/")[0].lower()
    return None


def netbios_domain(gpos):
    domain = extract_domain(gpos)
    return domain.split(".")[0].upper() if domain else None


def qualify(netbios, name):
    return "{}\\{}".format(netbios, name) if netbios else name


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

    body = '<div class="he2i">{}</div>'.format(info_table(rows))
    return section(0, _("General"), body, expanded=True, h_variant=True)


def keys_values_table(kvs, previous=False):
    css_class = "info4" if previous else "info3"
    out = ['<table class="{}">'.format(css_class)]

    if previous:
        out.append(
            "<tr><th scope=\"col\">{}</th><th scope=\"col\">{}</th>"
            "<th scope=\"col\">{}</th><th scope=\"col\">{}</th></tr>".format(
                esc(_("Setting")),
                esc(_("State")),
                esc(_("Previous Value")),
                esc(_("Winning GPO")),
            )
        )
    else:
        out.append(
            "<tr><th scope=\"col\">{}</th><th scope=\"col\">{}</th>"
            "<th scope=\"col\">{}</th></tr>".format(
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
            os.path.basename(str(target)) or str(target),
        )
    if ptype == "Folders":
        path = po.path or ""
        return (
            _("Folder") + " (" + _("Path") + ": " + str(path) + ")",
            os.path.basename(str(path)) or str(path),
        )
    if ptype == "Inifiles":
        return (
            _("Ini File")
            + " ("
            + _("File Path") + ": " + str(po.path or "") + ", "
            + _("Section Name") + ": " + str(po.section or "") + ", "
            + _("Property Name") + ": " + str(po.property or "")
            + ")",
            str(po.property or po.path or ""),
        )
    if ptype == "Drives":
        path = po.path or ""
        return (_("Drive Map") + " (" + str(path) + ")", str(po.label or path))
    if ptype == "Environmentvariables":
        return (_("Environment") + " (" + str(po.name or "") + ")", str(po.name or ""))
    if ptype == "Networkshares":
        return (_("Network Share") + " (" + str(po.name or "") + ")", str(po.name or ""))
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
        '<div class="he4i">{}</div>'.format(info_table(rows)),
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
            '<div class="he4i">{}</div>'.format(keys_values_table(kvs, previous)),
        )
        blocks.append(
            section(1, _("Policies"), admin, expanded=True, h_variant=True)
        )

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
        body = '<div class="he4i">{}</div>'.format(info_table(rows))
        items.append(section(2, title, body))

    if not items:
        return None

    applied = section(
        1, _("Applied GPOs"), "".join(items), expanded=True, h_variant=True
    )
    return section(
        0, _("Group Policy Objects"), applied, expanded=True, h_variant=True
    )


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
        "<title>{}</title>\n".format(esc(name_label)),
        '<style type="text/css">{}</style>\n'.format(CSS),
        '<script type="text/javascript">{}{}</script>\n'.format(js_strings(), JS),
        "</head>\n",
        '<body onload="window_onload();" onclick="return document_onclick(event);" '
        'onkeypress="return document_onkeypress(event);">\n',
        '<table class="title">\n',
        '<tr><td colspan="2" class="rsopheader">{}</td></tr>\n'.format(
            esc(_("Group Policy Results"))
        ),
        '<tr><td colspan="2" class="rsopname">{}</td></tr>\n'.format(esc(name_label)),
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

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    print(_("HTML report saved to {}").format(filepath))
