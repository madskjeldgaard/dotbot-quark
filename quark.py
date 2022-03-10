import os, subprocess, dotbot, time
from enum import Enum

class PkgStatus(Enum):
    # These names will be displayed
    UP_TO_DATE = 'Up to date'
    INSTALLED= 'Installed'
    UPDATED = 'Updated'
    NOT_FOUND = 'Not Found'
    ERROR = "Error"
    NOT_SURE = 'Could not determine'

class Quark(dotbot.Plugin):
    _directive = 'quark'

    def __init__(self, context):
        super(Quark, self).__init__(self)
        self._context = context
        self._strings = {}

        # Names to search the query string for
        self._strings[PkgStatus.ERROR] = "aborting"
        self._strings[PkgStatus.NOT_FOUND] = "Could not find all required packages"
        self._strings[PkgStatus.UPDATED] = "Net Upgrade Size:"
        self._strings[PkgStatus.INSTALLED] = "Total Installed Size:"
        self._strings[PkgStatus.UP_TO_DATE] = "is up to date -- skipping"

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('Quark cannot handle directive %s' %
                directive)
        return self._process(data)

    def _process(self, packages):
        defaults = self._context.defaults().get('quark', {})
        results = {}
        successful = [PkgStatus.UP_TO_DATE, PkgStatus.UPDATED, PkgStatus.INSTALLED]

        for pkg in packages:
            if isinstance(pkg, dict):
                self._log.error('Incorrect format')
            elif isinstance(pkg, list):
                # self._log.error('Incorrect format')
                pass
            else:
                pass
            result = self._install(pkg)
            results[result] = results.get(result, 0) + 1
            if result not in successful:
                self._log.error("Could not install package '{}'".format(pkg))

        if all([result in successful for result in results.keys()]):
            self._log.info('\nAll packages installed successfully')
            success = True
        else:
            success = False

        for status, amount in results.items():
            log = self._log.info if status in successful else self._log.error
            log('{} {}'.format(amount, status.value))

        return success

    def _install(self, pkg):
        # print(self.path)
        sc_script = os.path.dirname(os.path.abspath(__file__)) + "/" + "installquarks.scd"
        # sc_script = os.path.expanduser("installquarks.scd")
        cmd = '[ -f {} ] && sclang {} {}'.format(sc_script, sc_script, pkg)

        self._log.info("Installing SuperCollider quark \"{}\". Please wait...".format(pkg))

        # needed to avoid conflicts due to locking
        # time.sleep(1)

        # self._log.info(cmd)
        proc = subprocess.Popen(cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # This is necessary to have the return code set.
        _ = proc.communicate()[0]

        out = proc.returncode
        proc.stdout.close()

        if out == 0:
            self._log.info("Successfully installed quark {}".format(pkg))
            return PkgStatus.INSTALLED

        self._log.error("An error occurred with quark {}".format(pkg))
        return PkgStatus.ERROR
