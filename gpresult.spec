%add_python3_req_skip gpresult.Preferences.Preferences.Drive
%add_python3_req_skip gpresult.Preferences.Preferences.EnvVar
%add_python3_req_skip gpresult.Preferences.Preferences.File
%add_python3_req_skip gpresult.Preferences.Preferences.Folder
%add_python3_req_skip gpresult.Preferences.Preferences.Inifile
%add_python3_req_skip gpresult.Preferences.Preferences.Networkshare
%add_python3_req_skip gpresult.Preferences.Preferences.Shortcut

Name: gpresult
Version: 0.0.2
Release: alt2

Summary: Display applied policies
License: GPLv3+
Group: Other
Url: https://gitlab.basealt.space/alt/gpresult
BuildArch: noarch

BuildRequires: rpm-build-python3
BuildRequires: python3(wheel), python3(hatchling)
Requires: libgvdb-gir

Source0: %name-%version.tar

%description
gpresult is used to get the result set of Group Policies that apply to a user and/or computer in domain.
The utility allows you to display a list of domain  (GPO) policies that apply to the computer and user.

%prep
%setup -q

%build
%pyproject_build

%install
%pyproject_install
install -Dm0644 completions/%name %buildroot/%_datadir/bash-completion/completions/%name

%files
%python3_sitelibdir/%name
%python3_sitelibdir/%name/locales
%python3_sitelibdir/%name-%version.dist-info
%_bindir/%name
%_datadir/bash-completion/completions/%name

%changelog
* Mon Sep 16 2024 Maria Alexeeva <alxvmr@altlinux.org> 0.0.2-alt2
- Added output containing information about Preference
- Added analysis of policies that have no keys

* Mon Sep 02 2024 Evgeny Sinelnikov <sin@altlinux.org> 0.0.1-alt2
- Initial build for Sisyphus

* Mon Aug 19 2024 Maria Alexeeva <alxvmr@altlinux.org> 0.0.1-alt1
- First build

