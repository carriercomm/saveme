
#
#
#

from .snapshots import manage, create, listsnapshot, deletesnapshot
from .cfg import getdefsnappol as _cfg_default_snapshot_policy

class CommandLine:
    def __init__(self):
        pass

    def usage(self, proc):
        print("""usage: %s

COMMANDS
 manage <path> [--policy=XXX] [--noprompt]
 delete <path> <label>\n create <path> [--label=XXX] [--noprompt]
   list <path>

OPTIONS
 policy = [0-9]*[hr,dy,wk,yr]
 label = use a manual id
 noprompt = will take action, no pause for confirmation""" % proc)

    def go(self, args):
        status = 12
        if len(args) == 1:
            self.usage(args[0])
        elif args[1] == "manage":
            if len(args) == 2:
                print("manage: you must specify <path>")
                status = 1
            elif args[2] in ("--help", "help"):
                print("usage: manage  <path> [--policy=XXX] [--noprompt]\nexample policy=\"1wk+\"")
                status = 12
            else:
                pool = args[2]
                policy = _cfg_default_snapshot_policy()
                promptuser = True
                for options in args[3:]:
                    if options.startswith("--policy="):
                        policy = options[9:]
                    elif options == "--noprompt":
                        promptuser = False
                    else:
                        print("unknown option = %s" % options)
                        return 3
                print("Managing snapshots for path=\"%s\" with policy=\"%s\" "
                      % (pool, policy))
                status = manage(pool, policy, promptuser=promptuser)
        elif args[1] == "list":
            if len(args) == 2:
                print("list: you must specify <path>")
                status = 1
            else:
                pool = args[2]
                label = None
                for options in args[3:]:
                    print("unknown option = %s" % options)
                    return 3
                status = listsnapshot(pool)
        elif args[1] == "create":
            if len(args) == 2:
                print("create: you must specify <path>")
                status = 1
            else:
                pool = args[2]
                label = None
                promptuser = True
                for options in args[3:]:
                    if options.startswith("--label="):
                        label = options[8:]
                    elif options == "--noprompt":
                        promptuser = False
                    else:
                        print("unknown option = %s" % options)
                        return 3
                status = create(pool, label=label, promptuser=promptuser)
        elif args[1] == "delete":
            if len(args) < 4:
                print("delete: you must specify <path> <label>")
                status = 1
            else:
                pool = args[2]
                label = args[3]
                for options in args[4:]:
                    print("unknown option = %s" % options)
                    return 3
                status = deletesnapshot(pool, label)
        else:
            print("not a valid action")
            status = 2
        return status

    def help(self):
        print('i am suppossed to go, check usage')
        return True

