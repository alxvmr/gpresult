#!/bin/bash

dirs=(locales/*)
dirs=("${dirs[@]/%//LC_MESSAGES/}")
source_path="gpresult/"

echo "Enter the name <.po> file: "
read po_file

echo "Enter the name source (.py): "
read py_file

for d in "${dirs[@]}"
do
    po_path=("${d/%/${po_file}}")
    mo_path=${po_path:0:${#po_path}-2}"mo"
    py_path=("${source_path/%/${py_file}}")
    mess_path="${d/%/"message.po"}"

    xgettext -o "$mess_path" "$py_path"
    msgmerge -N "$po_path" "$mess_path" > "${d/%/"temp.po"}"
    mv "${d/%/"temp.po"}" "$po_path"
    rm "$mess_path"

    msgfmt -o "$mo_path" "$po_path" 
done

echo "Localization file $po_file updated successfully!"