from typing import Iterable, Optional, Tuple

from babel.support import LazyProxy
from stfu_tg import Italic, Section

from ass.i18n import gettext as _


class ArgError(Exception):

    @property
    def doc(self) -> Tuple[str]:
        raise NotImplementedError


class ArgTypeError(ArgError):
    text: str
    needed_type: Tuple[LazyProxy, LazyProxy]
    description: Optional[LazyProxy]

    def __init__(self, text: str, needed_type: Tuple[LazyProxy, LazyProxy], description: Optional[LazyProxy]):
        self.text = text
        self.needed_type = needed_type
        self.description = description

    @property
    def doc(self):
        return (
            _("Argument \"{text}\" ({description}) has an invalid type!").format(
                text=Italic(self.text), description=self.description or _("Has no description")
            ),
            Section(Italic(self.needed_type[0]), title=_("Needed type"))
        )


class ArgListEmpty(ArgError):
    needed_type: Tuple[LazyProxy, LazyProxy]
    description: Optional[LazyProxy]

    def __init__(self, needed_type: Tuple[LazyProxy, LazyProxy], description: Optional[LazyProxy]):
        self.needed_type = needed_type
        self.description = description

    @property
    def doc(self):
        return (
            _("The list argument ({description}) is empty!").format(description=self.description),
            Section(Italic(self.needed_type[0]), title=_("Needed type"))
        )


class ArgInListItemError(ArgError):
    child_error: ArgError

    def __init__(self, child_error: ArgError):
        self.child_error = child_error

    @property
    def doc(self):
        return self.child_error.doc


class ArgIsRequiredError(ArgError):

    def __init__(self, description: Optional[LazyProxy]):
        self.description = description

    @property
    def doc(self):
        return _("Argument ({description}) is required!").format(description=self.description),


class ArgCustomError(ArgError):

    def __init__(self, *texts: Iterable[str | LazyProxy]):
        self.texts = texts

    @property
    def doc(self) -> Tuple[str]:
        return *(str(x) for x in self.texts),


ARGS_EXCEPTIONS = (ArgTypeError, ArgIsRequiredError, ArgListEmpty, ArgInListItemError, ArgCustomError)
