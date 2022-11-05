# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .provider import *

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_render.config as __config
    config = __config
    import pulumi_render.owners as __owners
    owners = __owners
    import pulumi_render.services as __services
    services = __services
else:
    config = _utilities.lazy_import('pulumi_render.config')
    owners = _utilities.lazy_import('pulumi_render.owners')
    services = _utilities.lazy_import('pulumi_render.services')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "render",
  "mod": "services",
  "fqn": "pulumi_render.services",
  "classes": {
   "render:services:BackgroundWorker": "BackgroundWorker",
   "render:services:CronJob": "CronJob",
   "render:services:CustomDomain": "CustomDomain",
   "render:services:Deploy": "Deploy",
   "render:services:Job": "Job",
   "render:services:PrivateService": "PrivateService",
   "render:services:Scale": "Scale",
   "render:services:StaticSite": "StaticSite",
   "render:services:Suspend": "Suspend",
   "render:services:WebService": "WebService"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "render",
  "token": "pulumi:providers:render",
  "fqn": "pulumi_render",
  "class": "Provider"
 }
]
"""
)
