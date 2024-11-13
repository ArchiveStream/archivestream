__package__ = 'abx_spec_archivebox'
__order__ = 400

# from .effects import *
# from .events import *
# from .reads import *
# from .writes import *
# from .states import *

from typing import cast

import abx
from abx_spec_config import ConfigPluginSpec
from abx_spec_pydantic_pkgr import PydanticPkgrPluginSpec
from abx_spec_django import DjangoPluginSpec
from abx_spec_searchbackend import SearchBackendPluginSpec

class ArchiveBoxPluginSpec(ConfigPluginSpec, PydanticPkgrPluginSpec, DjangoPluginSpec, SearchBackendPluginSpec):
    """
    ArchiveBox plugins can use any of the hooks from the Config, PydanticPkgr, and Django plugin specs.
    """
    pass

PLUGIN_SPEC = ArchiveBoxPluginSpec


TypedPluginManager = abx.ABXPluginManager[ArchiveBoxPluginSpec]
pm = cast(TypedPluginManager, abx.pm)