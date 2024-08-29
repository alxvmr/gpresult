# GPResult
---
The **documentation** can be found at this [link](https://alxvmr.github.io/gpresult/).

---

The program is designed to display applied user and machine policies in ALT Linux OS.

GPResult uses the GVDB database to determine the applied policies: `/etc/dconf/db/policy<UID>`. This database is updated as a result of [`gpupdate`](https://github.com/altlinux/gpupdate), which applies various GPO/GPT settings.

---
## Required packages
The package is based on the [Sisyphus](https://packages.altlinux.org/ru/sisyphus/) repository.

The `gpresult` package depends on the following packages:

```bash
rpm-build-python3
gettext-tools
libgvdb-gir
python3-module-distro
```
---
## Summary
GPResult is a console utility. Help on available options can be obtained with the command `gpresult --help`.

The project supports **Russian** and **English** languages. The system language is used by default.

---
## TODO
> Add error handling

> Get away from using getpwnam

> Generating HTML report

> View applied policies on different nodes for different users

> Which groups the user is a member of

> ...
