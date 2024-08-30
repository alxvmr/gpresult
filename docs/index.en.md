---
hide:
  - navigation
---

# Summary
Displays information about the resulting set of group policies for the current user on the current machine.

The information about the applied group policies is generated from the data obtained after the last execution of [gpupdate](https://github.com/altlinux/gpupdate). GPResult does not call the gpupdate utility.

## Syntax

```
gpresult [-h] [-f {raw,standard,verbose}] [-i POLICY_GUID] [-n POLICY_NAME] [-u] [-m]
```

<div class="warning" style='padding:0.1em; background-color:#CFDFF5; color:#0F174A'>
<span>
<p style='margin-left:1em; margin-top:1em'>
The <code>-i</code> and <code>-n</code> options  are not used with the <code>-f verbose</code> option
</p></span>
</div>

<div class="warning" style='padding:0.1em; background-color:#CFDFF5; color:#0F174A; margin-top: 10px'>
<span>
<p style='margin-left:1em; margin-top:1em'>
Without specifying the <code>-f</code> option the default is <code>-f verbose</code>
</p></span>
</div>

## Parameters

| Parameter                                                    | Description                                                                                                                                                                               |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-h, --help`                                                 | Get reference information                                                                                                                                                                 |
| `-f {raw,standard,verbose}, --format {raw,standard,verbose}` | Output format:<br> ***raw*** - display keys and values<br> ***standard*** - оdisplay summary data, only policy names are included<br> ***verbose*** - display detailed policy information |
| `-i POLICY_GUID, --policy_guid POLICY_GUID`                  | Get information about applied keys and policy values by **GUID**                                                                                                                          |
| `-n POLICY_NAME, --policy_name POLICY_NAME`                  | Get information about applied keys and policy values by **name**                                                                                                                          |
| -u, --user                                                   | Display information for the current **user**                                                                                                                                              |
| -m, --machine                                                | Display information for the current **machine**                                                                                                                                           |

### Remarks
- To get information about applied keys and policy values by GUID, a key in curly braces is passed as a parameter.

## Examples
1. To get a complete report of Group Policies applied for a user and machine enter:
   
    ```
    gpresult -f verbose
    ```

2. To get a complete report of applied policies for **user** enter:
   
    ```
    gpresult -f verbose -u
    ```

    for **machine**:

    ```
    gpresult -f verbose -m
    ```

3. To get information about applied Group Policy Keys by **GUID** enter:
   
    ```
    gpresult -f standard -i {1BA9EB0C-7B29-49CC-813D-75D8701FC221}
    ```

4. To get information about applied group policy keys by **name** (for example, group policy name is policy) enter:
   
    ```
    gpresult -f standard -n policy
    ```

## Related links
- [Group Policies on ALT Linux](https://www.altlinux.org/Групповые_политики)
- [Group Policies/ALT System Control](https://www.altlinux.org/Групповые_политики/ALT_System_Control)
- [GPResult source code](https://github.com/alxvmr/gpresult)