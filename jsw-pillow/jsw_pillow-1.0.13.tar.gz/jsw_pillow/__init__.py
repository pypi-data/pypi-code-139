import pkg_resources

version = pkg_resources.get_distribution('jsw-pillow').version
__version__ = version

# pillow modules
from jsw_pillow.modules.watermark import Watermark
