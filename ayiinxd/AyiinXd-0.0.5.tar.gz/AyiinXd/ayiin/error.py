# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinXdSupport & t.me/AyiinSupport

# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================


class SpamFailed(Exception):
    """
    Raises when the spam task was failed
    """


class DownloadFailed(Exception):
    """
    Raises when the download task was failed
    """


class DelAllFailed(Exception):
    """
    Raises when the del all function was failed
    """


class DependencyMissingError(Exception):
    """
    raise import error as no module name
    """
