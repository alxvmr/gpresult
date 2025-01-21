---
hide:
  - navigation
---

# Summary
Displays information about the resulting set of group policies for the current user on the current machine.

The information about the applied group policies is generated from the data obtained after the last execution of [gpupdate](https://github.com/altlinux/gpupdate). GPResult does not call the gpupdate utility.

## Syntax

```
gpresult [-h] [-r] [-c] [-v] [-l] [-p] [-w WIDTH] [-i POLICY_GUID] [-n POLICY_NAME] [-u] [-m]
```

<div class="warning" style='padding:0.1em; background-color:#CFDFF5; color:#0F174A'>
<span>
<p style='margin-left:1em; margin-top:1em'>
The <code>-l/--list</code> option  are not used with the <code>-i/--policy_guid</code> и <code>-n/--policy_name</code> options
</p></span>
</div>

<div class="warning" style='padding:0.1em; background-color:#CFDFF5; color:#0F174A; margin-top: 10px'>
<span>
<p style='margin-left:1em; margin-top:1em'>
Without selecting the output format option, the default output format is <code>-v/--verbose</code>
</p></span>
</div>

<div class="warning" style='padding:0.1em; background-color:#CFDFF5; color:#0F174A; margin-top: 10px'>
<span>
<p style='margin-left:1em; margin-top:1em'>
The option <code>-p/--previous</code> applies only in cases where GPO keys are used (with options <code>--verbose</code>, <code>--raw</code> + their variations with other options)
</p></span>
</div>

## Parameters

| Parameter                                                    | Description                                                                                                                                                                               |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-h, --help`                                                 | Get reference information                                                                                                                                                                 |
|`-r, --raw`| **Output format**: display of keys and values|
|`-c, --common`| **Output format**: displays system information and group policy names|
|`-v, --verbose`| **Output format**: display Group Policy details|
|`-l, --list`|**Output format**: formatted display of Group Policy names and their GUIDs|
|`-p, --previous`|**Output format**: include previous GPO key values in the output|
|`-w, --width`|**Output customization**: sets the output width of the internal tables. By default, the column width is equal to the width of the longest row|
| `-i POLICY_GUID, --policy_guid POLICY_GUID`                  | Get information about applied keys and policy values by **GUID**                                                                                                                          |
| `-n POLICY_NAME, --policy_name POLICY_NAME`                  | Get information about applied keys and policy values by **name**                                                                                                                          |
| `-u, --user`                                                   | Display information for the current **user**                                                                                                                                              |
| `-m, --machine`                                               | Display information for the current **machine**                                                                                                                                           |

### Remarks
- The `-l\--list` option can be used in conjunction with the `-r\--row` option - the **non** output will be formatted, with the GPO name and GUID separated by a single space
- Group Policy GUID can be passed with or without curly braces: `{1BA9EB0C-7B29-49CC-813D-813D-75D8701FC221}` and `1BA9EB0C-7B29-49CC-813D-75D8701FC221`.

## Examples
1. To get a report of Group Policies applied for a user and machine enter:
   
    ```
    gpresult -v
    ```

2. To get a complete report of applied policies for **user** enter:
   
    ```
    gpresult -v -u
    ```

    for **machine**:

    ```
    gpresult -v -m
    ```

3. To get information about applied Group Policy Keys by **GUID** enter:
   
    ```
    gpresult -f standard -i 1BA9EB0C-7B29-49CC-813D-75D8701FC221
    ```

4. To get information about applied group policy keys by **name** (for example, group policy name is policy) enter:
   
    ```
    gpresult -c -n policy
    ```

## Related links
- [Group Policies on ALT Linux](https://www.altlinux.org/Групповые_политики)
- [Group Policies/ALT System Control](https://www.altlinux.org/Групповые_политики/ALT_System_Control)
- [GPResult source code](https://github.com/alxvmr/gpresult)