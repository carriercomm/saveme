
#
#
#

from .utils import TaskRunner, StopException
from .external import getid
import time

def genarid():
    return getid()

def makearfsfromdisk(disk):
    runner = TaskRunner()
    try:
        runner.setvalue('disk', disk)
        for step in ('add-partition-table',
                     'verify-partition-table',
                     'generate-luks-key',
                     'add-luks-partition'):
            runner.runstep(step)
        # cprt will be the part for the rest of the steps
        runner.addalias('cprt', 'part')
        runner.runstep('verify-luks-partition')
        runner.setvalue('arid', genarid())
        runner.runstep('verify-arid-unused')
        runner.runstep('add-archive-filesystem')
        time.sleep(0.2)
        for step in ('verify-archive-filesystem',
                     'mount-archive-filesystem',
                     'check-archive-filesystem'):
            runner.runstep(step)
        runner.dump()
    except TaskRunner.MissingParamException as err:
        print("Missing parameter: [%s]"% err)
        runner.dump()
        return 1
    except StopException as err:
        print("Will not continue")
        runner.dump()
        return 1
    print("Finished adding /arfs/%s" %runner.getvalue("arid"))
    return runner.getretcode()
