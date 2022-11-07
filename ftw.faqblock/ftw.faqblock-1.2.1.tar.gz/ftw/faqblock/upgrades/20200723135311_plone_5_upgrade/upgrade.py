from Products.CMFPlone.utils import getFSVersionTuple
from ftw.upgrade import UpgradeStep


class Plone5Upgrade(UpgradeStep):
    """Plone 5 upgrade.
    """

    def __call__(self):
        if getFSVersionTuple() > (5, ):
            self.install_upgrade_profile()
