# GPResult
---
The program is designed to display applied user and machine policies in ALT Linux OS

---
## Required packages

The following packages must be installed to run the program:

```bash
python3-module-pygobject3-devel
python3-module-pygobject3
python3-devel
gobject-introspection
gobject-introspection-devel
python-module-gettext
libgvdb
```
The `libgvdb` library is not currently collected in Sisyphus. You can build it locally using sources from [this repository](https://github.com/alxvmr/gvdb-binding).

---
## Example

Example of running the command (from the root directory of the project):
```bash
python3 gpresult.py --type=all --machine
```

Program output:
```bash
Список примененных политик для машины host-1.domain.test:

/Software/BaseALT/Policies/Control/ssh-gssapi-auth                    'enabled'                                                                                                   
/Software/BaseALT/Policies/Control/system-policy                      'gpupdate'                                                                                                  
/Software/BaseALT/Policies/Control/sshd-gssapi-auth                   'enabled'                                                                                                   
/Software/BaseALT/Policies/Control/sshd-allow-groups                  'enabled'                                                                                                   
/Software/BaseALT/Policies/SystemdUnits/sshd.service                  1                                                                                                           
/Software/BaseALT/Policies/Control/sshd-allow-groups-list             'remote'                                                                                                    
/Software/BaseALT/Policies/ReadQueue/Machine/0                        "('Local Policy', '/var/cache/gpupdate/local-policy', None)"                                                
/Software/BaseALT/Policies/SystemdUnits/gpupdate.service              1                                                                                                           
/Software/BaseALT/Policies/ReadQueue/Machine/1                        "('qwe1', '/var/cache/samba/gpo_cache/DOMAIN.TEST/POLICIES/{506A92C2-9C84-40CD-A950-FFEE42A9B0A5}', 131074)"
/Software/BaseALT/Policies/SystemdUnits/oddjobd.service               1                                                                                                           
/SOFTWARE/Policies/Microsoft/WindowsFirewall/FirewallRules/OpenSSH    'v2.20|Action=Allow|Active=TRUE|Dir=In|Protocol=6|LPort=22|Name=Open SSH port|Desc=Open SSH port|'
```

The project supports **Russian** and **English** languages. Customization is done using the `gettext` module.

---
## TODO
> Add error handling

> Add multiple policy output format

> Add policy filtering

> Get away from using getpwnam

> ...
