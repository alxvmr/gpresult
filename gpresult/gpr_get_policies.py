from GPO import GPO
import gpr_system, gpr_init
import os


def get_policies(obj=None, cmd=None, cmd_arg=None):
    uid = None
    name = os.getlogin()
    gpos = None

    if obj:
        if obj == 'user':
            uid = gpr_system.get_uid_from_name(name)
        path = gpr_system.get_path_to_policy(uid)
        gpr_init.init_data(path, obj)
    
    else:
        path = gpr_system.get_path_to_policy(uid)
        gpr_init.init_data(path, 'machine')

        uid = gpr_system.get_uid_from_name(name)
        path = gpr_system.get_path_to_policy(uid)
        gpr_init.init_data(path, 'user')

    if cmd == "guid":
        gpos = GPO.get_gpos_by_guid(cmd_arg, obj)
    elif cmd == "name":
        gpos = GPO.get_gpos_by_name(cmd_arg, obj)
    else:
        gpos = GPO.get_all_gpos(obj)

    return gpos