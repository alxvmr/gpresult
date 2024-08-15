%add_python3_req_skip gpr_get_policies
%add_python3_req_skip gpr_show
%add_python3_req_skip gpr_system

Name: gpresult
Version: 0.0.1
Release: alt1

Summary: Display applied policies
License: GPLv3+
Group: Other
Url: https://github.com/alxvmr/gpresult
BuildArch: noarch

BuildRequires: python3-module-setuptools
BuildRequires: rpm-build-python3 gettext-tools
Requires: libgvdb-gir
Requires: python3-module-distro

Source0: %name-%version.tar

%description
gpresult is used to get the result set of Group Policies that apply to a user and/or computer in domain.
The utility allows you to display a list of domain  (GPO) policies that apply to the computer and user.

%prep
%setup -q

%install
mkdir -p \
	%buildroot%python3_sitelibdir/%{name}/%{name}
cp -r src/* \
	%buildroot%python3_sitelibdir/%{name}/%{name}

# Transfering translation
mkdir -p \
	%buildroot%python3_sitelibdir/%{name}/
cp -r locales \
	%buildroot%python3_sitelibdir/%{name}/

mkdir -p \
	%buildroot%_bindir/

ln -s %python3_sitelibdir/%{name}/%{name}/gpresult.py \
	%buildroot%_bindir/gpresult

%files
%python3_sitelibdir/%{name}/%{name}
%python3_sitelibdir/%{name}/locales
%_bindir/gpresult

%changelog
* Wed Aug 14 2024 Maria Alexeeva <alxvmr@altlinux.org> 0.0.1-alt1
- First build

