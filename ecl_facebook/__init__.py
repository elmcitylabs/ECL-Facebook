# -*- coding: utf-8 -*-

"""
ECL Facebook
~~~~~~~~~~~

:copyright: © 2012 Elm City Labs LLC
:license: Apache 2.0, see LICENSE for more details.
"""

from .metadata import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __maintainer__,
    __version__,
)

from .facebook import Facebook, FacebookError

__all__ = [
    '__author__', '__copyright__', '__email__', '__license__',
    '__maintainer__', '__version__', 'Facebook', 'FacebookError'
]

