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

from .decorators import facebook_begin, facebook_callback

from .facebook import Facebook

__all__ = [
    '__author__', '__copyright__', '__email__', '__license__',
    '__maintainer__', '__version__', 'facebook_begin', 'facebook_callback',
    'Facebook',
]

