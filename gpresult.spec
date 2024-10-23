%add_python3_req_skip gpresult.Preferences.Preferences.Drive
%add_python3_req_skip gpresult.Preferences.Preferences.EnvVar
%add_python3_req_skip gpresult.Preferences.Preferences.File
%add_python3_req_skip gpresult.Preferences.Preferences.Folder
%add_python3_req_skip gpresult.Preferences.Preferences.Inifile
%add_python3_req_skip gpresult.Preferences.Preferences.Networkshare
%add_python3_req_skip gpresult.Preferences.Preferences.Shortcut

Name: gpresult
Version: 0.0.2
Release: alt0.c10f2

Summary: Display applied policies
License: GPLv3+
Group: Other
Url: https://gitlab.basealt.space/alt/gpresult
BuildArch: noarch

BuildRequires: rpm-build-python3
Requires: libgvdb-gir gpupdate >= 0.11.0

Source0: %name-%version.tar

%description
gpresult is used to get the result set of Group Policies that apply to a user and/or computer in domain.
The utility allows you to display a list of domain  (GPO) policies that apply to the computer and user.

%prep
%setup -q

%install
mkdir -p \
	%buildroot%python3_sitelibdir/
cp -r gpresult \
	%buildroot%python3_sitelibdir/
cp -r locales \
	%buildroot%python3_sitelibdir/%name/

# Generate translation
for lang in "en_US" "ru_RU"
do
  for entry in %buildroot%python3_sitelibdir/%name/locales/$lang/LC_MESSAGES/*
    do
      msgfmt -o ${entry:0:(-2)}mo $entry
    done
done

mkdir -p \
	%buildroot%_bindir/

cat > %buildroot%_bindir/%name <<EOF
#!/usr/bin/python3

import sys

from gpresult.gpresult import main

if __name__ == "__main__":
    sys.exit(main())
EOF

%files
%attr(755,-,-) %_bindir/%name
%python3_sitelibdir/%name
%python3_sitelibdir/%name/locales
%exclude %python3_sitelibdir/%name/locales/en_US/LC_MESSAGES/*.po
%exclude %python3_sitelibdir/%name/locales/ru_RU/LC_MESSAGES/*.po

%changelog
* Tue Oct 22 2024 Maria Alexeeva <alxvmr@altlinux.org> 0.0.2-alt0.c10f2
- Downgrade for c10f2

* Mon Sep 16 2024 Maria Alexeeva <alxvmr@altlinux.org> 0.0.2-alt1
- Added output containing information about Preference
- Added analysis of policies that have no keys

* Mon Sep 02 2024 Evgeny Sinelnikov <sin@altlinux.org> 0.0.1-alt2
- Initial build for Sisyphus

* Mon Aug 19 2024 Maria Alexeeva <alxvmr@altlinux.org> 0.0.1-alt1
- First build

