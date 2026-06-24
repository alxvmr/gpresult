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
