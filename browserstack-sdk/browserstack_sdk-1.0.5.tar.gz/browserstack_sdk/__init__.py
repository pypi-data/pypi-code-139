# coding: UTF-8
import sys
bstack1ll1_opy_ = sys.version_info [0] == 2
bstack1l111_opy_ = 2048
bstack111_opy_ = 7
def bstack1l1_opy_ (bstack1llll_opy_):
    global bstack1lll_opy_
    bstack1ll_opy_ = ord (bstack1llll_opy_ [-1])
    bstack1ll11_opy_ = bstack1llll_opy_ [:-1]
    bstack11_opy_ = bstack1ll_opy_ % len (bstack1ll11_opy_)
    bstack1l11_opy_ = bstack1ll11_opy_ [:bstack11_opy_] + bstack1ll11_opy_ [bstack11_opy_:]
    if bstack1ll1_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l111_opy_ - (bstack11ll_opy_ + bstack1ll_opy_) % bstack111_opy_) for bstack11ll_opy_, char in enumerate (bstack1l11_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1l111_opy_ - (bstack11ll_opy_ + bstack1ll_opy_) % bstack111_opy_) for bstack11ll_opy_, char in enumerate (bstack1l11_opy_)])
    return eval (bstack1l_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
from packaging import version
from browserstack.local import Local
bstack1lll1_opy_ = {
	bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࠨࢌ"),
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢍ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡱࡥࡺࠩࢎ"),
  bstack1l1_opy_ (u"ࠧࡰࡵࠪ࢏"): bstack1l1_opy_ (u"ࠨࡱࡶࠫ࢐"),
  bstack1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࢑"): bstack1l1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ࢒"),
  bstack1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ࢓"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬ࢔"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ࢕"): bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨ࢖"),
  bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢗ"): bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨ࢘"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࢙"): bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦ࢚ࠩ"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡣࡷࡪ࢛ࠫ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫ࢜"),
  bstack1l1_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬ࢝"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨ࢞"),
  bstack1l1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧ࢟"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࢠ"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࢡ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࢢ"),
  bstack1l1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࢣ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬࢤ"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࢥ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࢦ"),
  bstack1l1_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࢧ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࢨ"),
  bstack1l1_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࢩ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࢪ"),
  bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࢫ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࢬ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭ࢭ"): bstack1l1_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧࢮ"),
  bstack1l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࢯ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢰ"),
  bstack1l1_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬࢱ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬࢲ"),
  bstack1l1_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ࢳ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ࢴ"),
  bstack1l1_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪࢵ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪࢶ"),
  bstack1l1_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧࢷ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧࢸ"),
  bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩࢹ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩࢺ"),
  bstack1l1_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨࢻ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨࢼ"),
  bstack1l1_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࢽ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬࢾ"),
  bstack1l1_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧࢿ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧࣀ"),
  bstack1l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫࣁ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫࣂ"),
  bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧࣃ"): bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫࣄ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࣅ"): bstack1l1_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫࣆ"),
  bstack1l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧࣇ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣈ"),
  bstack1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ࣉ"): bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧ࣊"),
  bstack1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫ࣋"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫ࣌"),
  bstack1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧ࣍"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧ࣎"),
  bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹ࣏ࠧ"): bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵ࣐ࠪ"),
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏ࣑ࠬ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏ࣒ࠬ"),
  bstack1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩ࣓ࠬ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬࣔ"),
}
bstack11lll_opy_ = [
  bstack1l1_opy_ (u"ࠧࡰࡵࠪࣕ"),
  bstack1l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࣖ"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࣗ"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣘ"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࣙ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࣚ"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࣛ"),
]
bstack11l1_opy_ = {
  bstack1l1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࣜ"): bstack1l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࣝ"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࣞ"): [bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࣟ"), bstack1l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ࣠")],
  bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࣡"): bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ࣢"),
  bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࣣࠫ"): bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨࣤ"),
  bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧࣥ"): [bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࣦࠫ"), bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪࣧ")],
  bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࣨ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣩ"),
  bstack1l1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ࣪"): bstack1l1_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭࣫"),
  bstack1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ࣬"): [bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰ࣭ࠪ"), bstack1l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲ࣮ࠬ")],
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶ࣯ࠫ"): [bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࣰࠧ"), bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࣱࠧ")]
}
bstack11l_opy_ = {
  bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࣲࠧ"): [bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪࣳ"), bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪࣴ")]
}
bstackl_opy_ = [
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪࣵ"),
  bstack1l1_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨࣶ"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬࣷ"),
  bstack1l1_opy_ (u"ࠧࡴࡧࡷ࡛࡮ࡴࡤࡰࡹࡕࡩࡨࡺࠧࣸ"),
  bstack1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࣹࠪ"),
  bstack1l1_opy_ (u"ࠩࡶࡸࡷ࡯ࡣࡵࡈ࡬ࡰࡪࡏ࡮ࡵࡧࡵࡥࡨࡺࡡࡣ࡫࡯࡭ࡹࡿࣺࠧ"),
  bstack1l1_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ࣻ")
]
bstack111l_opy_ = [
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣼ"),
  bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣽ"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣾ"),
  bstack1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࣿ"),
  bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫँ"),
  bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ं"),
  bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨः"),
  bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨऄ"),
]
bstack1ll1l_opy_ = [
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ"),
  bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭आ"),
]
bstack1l11l_opy_ = bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩइ")
bstack1_opy_ = bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬई")
bstack1l1l1_opy_ = {
  bstack1l1_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬउ"): 50,
  bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪऊ"): 40,
  bstack1l1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ऋ"): 30,
  bstack1l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫऌ"): 20,
  bstack1l1_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ऍ"): 10
}
DEFAULT_LOG_LEVEL = bstack1l1l1_opy_[bstack1l1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ऎ")]
bstack11ll1_opy_ = bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨए")
bstack1l1ll_opy_ = bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨऐ")
bstack11l1l_opy_ = bstack1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩऑ")
bstack1l1l_opy_ = [bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ऒ"), bstack1l1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ओ")]
bstack1111_opy_ = [bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪऔ"), bstack1l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪक")]
bstack1lll1l1_opy_ = bstack1l1_opy_ (u"ࠩࡖࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠮ࠣࡹࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠿ࠦࡻࡾࠩख")
bstack11l1l1l_opy_ = bstack1l1_opy_ (u"ࠪࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡳࡦࡶࡸࡴࠦ࠭ग")
bstack1lll11ll_opy_ = bstack1l1_opy_ (u"ࠫࡕࡧࡲࡴࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭घ")
bstack1llllll_opy_ = bstack1l1_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤ࡭ࡻࡢࠡࡷࡵࡰ࠿ࠦࡻࡾࠩङ")
bstack1ll11l11_opy_ = bstack1l1_opy_ (u"࠭ࡓࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࡿࢂ࠭च")
bstack1l1lll1_opy_ = bstack1l1_opy_ (u"ࠧࡓࡧࡦࡩ࡮ࡼࡥࡥࠢ࡬ࡲࡹ࡫ࡲࡳࡷࡳࡸ࠱ࠦࡥࡹ࡫ࡷ࡭ࡳ࡭ࠧछ")
bstack11111ll_opy_ = bstack1l1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭ज")
bstack1lllll_opy_ = bstack1l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࡥ࠭झ")
bstack1ll11ll_opy_ = bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶ࠯ࠤࡵࡧࡢࡰࡶࠣࡥࡳࡪࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧࡶࠤࡹࡵࠠࡳࡷࡱࠤࡷࡵࡢࡰࡶࠣࡸࡪࡹࡴࡴࠢ࡬ࡲࠥࡶࡡࡳࡣ࡯ࡰࡪࡲ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡳࡥࡧࡵࡴࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬञ")
bstack1ll1llll_opy_ = bstack1l1_opy_ (u"ࠫࡍࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤ࡮ࡲࡷࡪ࠭ट")
bstack111l1l_opy_ = bstack1l1_opy_ (u"ࠬࡇ࡬࡭ࠢࡧࡳࡳ࡫ࠡࠨठ")
bstack1111ll_opy_ = bstack1l1_opy_ (u"࠭ࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡧࡴࠡࠤࡾࢁࠧ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡦࡰࡺࡪࡥࠡࡣࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮࡭ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡵ࠱ࠫड")
bstack111l11l_opy_ = bstack1l1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤࡳࡵࡴࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡶ࡫ࡩࡲࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡥࡸࠦࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤࠣࡥࡳࡪࠠࠣࡣࡦࡧࡪࡹࡳࡌࡧࡼࠦࠥࡵࡲࠡࡵࡨࡸࠥࡺࡨࡦ࡯ࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹ࠺ࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥࠤࡦࡴࡤࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠧ࠭ढ")
bstack11l1111_opy_ = bstack1l1_opy_ (u"ࠨࡏࡤࡰ࡫ࡵࡲ࡮ࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠥࡿࢂࠨࠧण")
bstack1l1111l_opy_ = bstack1l1_opy_ (u"ࠩࡈࡲࡨࡵࡵ࡯ࡶࡨࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢ࠰ࠤࢀࢃࠧत")
bstack1ll1l1ll_opy_ = bstack1l1_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪथ")
bstack1ll1lll_opy_ = bstack1l1_opy_ (u"ࠫࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫद")
bstack111l1ll_opy_ = bstack1l1_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠣ࡭ࡸࠦ࡮ࡰࡹࠣࡶࡺࡴ࡮ࡪࡰࡪࠥࠬध")
bstack11l1lll_opy_ = bstack1l1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࡀࠠࡼࡿࠪन")
bstack1l111l1_opy_ = bstack1l1_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢ࡯ࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡽࢀࠫऩ")
bstack111ll1_opy_ = bstack1l1_opy_ (u"ࠨࡗࡳࡨࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩप")
bstack11l11ll_opy_ = bstack1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠨफ")
bstack11l11l_opy_ = bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡦࡴࠠࡢࡲࡳࡶࡴࡶࡲࡪࡣࡷࡩࠥࡌࡗࠡࠪࡵࡳࡧࡵࡴ࠰ࡲࡤࡦࡴࡺࠩࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠮ࠣࡷࡰ࡯ࡰࠡࡶ࡫ࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡩ࡮ࡲ࡯ࡩࠥࡶࡹࡵࡪࡲࡲࠥࡹࡣࡳ࡫ࡳࡸࠥࡽࡩࡵࡪࡲࡹࡹࠦࡡ࡯ࡻࠣࡊ࡜࠴ࠧब")
bstack1111l11_opy_ = bstack1l1_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡮ࡴࡵࡲࡓࡶࡴࡾࡹ࠰ࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࠫࡿࢂ࠯ࠬࠡࡲ࡯ࡩࡦࡹࡥࠡࡷࡳ࡫ࡷࡧࡤࡦࠢࡷࡳ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳ࠾࠾࠶࠱࠴࠳࠶ࠠࡰࡴࠣࡶࡪ࡬ࡥࡳࠢࡷࡳࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠰ࡴࡸࡲ࠲ࡺࡥࡴࡶࡶ࠱ࡧ࡫ࡨࡪࡰࡧ࠱ࡵࡸ࡯ࡹࡻࠦࡴࡾࡺࡨࡰࡰࠣࡪࡴࡸࠠࡢࠢࡺࡳࡷࡱࡡࡳࡱࡸࡲࡩ࠴ࠧभ")
bstack1llll1l_opy_ = bstack1l1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱࠲ࠬम")
bstack1l1l11l_opy_ = bstack1l1_opy_ (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠤࠫय")
bstack1l11lll_opy_ = bstack1l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪ࠴ࠠࡼࡿࠪर")
__version__ = bstack1l1_opy_ (u"ࠨ࠳࠱࠴࠳࠻ࠧऱ")
bstack1lll1l11_opy_ = None
CONFIG = {}
bstack111ll11_opy_ = None
bstack1111l_opy_ = None
bstack11ll11l_opy_ = None
bstack1ll11l1_opy_ = -1
bstack111llll_opy_ = DEFAULT_LOG_LEVEL
bstack1lllll1_opy_ = 1
bstack1lll11_opy_ = False
bstack1ll11l1l_opy_ = bstack1l1_opy_ (u"ࠩࠪल")
bstack11l1ll1_opy_ = bstack1l1_opy_ (u"ࠪࠫळ")
bstack111l1l1_opy_ = None
bstack11ll1l_opy_ = None
bstack1llll11l_opy_ = None
bstack11lll11_opy_ = None
bstack1l11l11_opy_ = None
bstack1l1l1ll_opy_ = None
bstack1ll1l11l_opy_ = None
bstack1l1lll_opy_ = None
bstack1l111ll_opy_ = None
logger = logging.getLogger(__name__)
def bstack1ll1ll1l_opy_():
  global CONFIG
  global bstack111llll_opy_
  if bstack1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ऴ") in CONFIG:
    bstack111llll_opy_ = bstack1l1l1_opy_[CONFIG[bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧव")]]
  logging.basicConfig(level=bstack111llll_opy_,
                      format=bstack1l1_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫश"),
                      datefmt=bstack1l1_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩष"))
def bstack1lll1l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l111_opy_():
  bstack1ll1111l_opy_ = bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫस")
  bstack1ll11ll1_opy_ = os.path.abspath(bstack1ll1111l_opy_)
  if not os.path.exists(bstack1ll11ll1_opy_):
    bstack1ll1111l_opy_ = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭ह")
    bstack1ll11ll1_opy_ = os.path.abspath(bstack1ll1111l_opy_)
    if not os.path.exists(bstack1ll11ll1_opy_):
      bstack1l1llll_opy_(
        bstack1111ll_opy_.format(os.getcwd()))
  with open(bstack1ll11ll1_opy_, bstack1l1_opy_ (u"ࠪࡶࠬऺ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l1llll_opy_(bstack11l1111_opy_.format(str(exc)))
def bstack1l11l1l_opy_(config):
  bstack111ll1l_opy_ = config.keys()
  bstack111lll_opy_ = []
  if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऻ") in config:
    bstack111lll_opy_ = config[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ़")]
  for bstack1ll1lll1_opy_, bstack1l1ll1l_opy_ in bstack1lll1_opy_.items():
    if bstack1l1ll1l_opy_ in bstack111ll1l_opy_:
      config[bstack1ll1lll1_opy_] = config[bstack1l1ll1l_opy_]
      del config[bstack1l1ll1l_opy_]
  for bstack1ll1lll1_opy_, bstack1l1ll1l_opy_ in bstack11l1_opy_.items():
    for platform in bstack111lll_opy_:
      if isinstance(bstack1l1ll1l_opy_, list):
        for bstack1l1l1l_opy_ in bstack1l1ll1l_opy_:
          if bstack1l1l1l_opy_ in platform:
            platform[bstack1ll1lll1_opy_] = platform[bstack1l1l1l_opy_]
            del platform[bstack1l1l1l_opy_]
            break
      elif bstack1l1ll1l_opy_ in platform:
        platform[bstack1ll1lll1_opy_] = platform[bstack1l1ll1l_opy_]
        del platform[bstack1l1ll1l_opy_]
  for bstack1ll1lll1_opy_, bstack1l1ll1l_opy_ in bstack11l_opy_.items():
    for bstack1l1l1l_opy_ in bstack1l1ll1l_opy_:
      if bstack1l1l1l_opy_ in bstack111ll1l_opy_:
        config[bstack1ll1lll1_opy_] = config[bstack1l1l1l_opy_]
        del config[bstack1l1l1l_opy_]
  for bstack1l1l1l_opy_ in list(config):
    for bstack111ll_opy_ in bstack1ll1l_opy_:
      if bstack1l1l1l_opy_.lower() == bstack111ll_opy_.lower() and bstack1l1l1l_opy_ != bstack111ll_opy_:
        config[bstack111ll_opy_] = config[bstack1l1l1l_opy_]
        del config[bstack1l1l1l_opy_]
  return config
def bstack1lll1ll1_opy_(config):
  global bstack11l1ll1_opy_
  if bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऽ") in config and str(config[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫा")]).lower() != bstack1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧि"):
    if not bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ी") in config:
      config[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧु")] = {}
    if not bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू") in config[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩृ")]:
      if bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨॄ") in os.environ:
        config[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॅ")][bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॆ")] = os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫे")]
      else:
        current_time = datetime.datetime.now()
        bstack1ll1ll11_opy_ = current_time.strftime(bstack1l1_opy_ (u"ࠪࠩࡲࡥࠥࡣࡡࠨࡌࠪࡓࠧै"))
        hostname = socket.gethostname()
        bstack111111_opy_ = bstack1l1_opy_ (u"ࠫࠬॉ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack1l1_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧॊ").format(bstack1ll1ll11_opy_, hostname, bstack111111_opy_)
        config[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪो")][bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩौ")] = identifier
    bstack11l1ll1_opy_ = config[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷ्ࠬ")][bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫॎ")]
  return config
def bstack11l1l11_opy_(config):
  if bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ॏ") in config and config[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧॐ")] not in bstack1111_opy_:
    return config[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ॑")]
  elif bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚॒ࠩ") in os.environ:
    return os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓")]
  else:
    return None
def bstack1111lll_opy_(config):
  if bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ॔") in config:
    return config[bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬॕ")]
  elif bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭ॖ") in os.environ:
    return os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧॗ")]
  else:
    return None
def bstack1llll11_opy_(config):
  if bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧक़") in config and config[bstack1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨख़")] not in bstack1l1l_opy_:
    return config[bstack1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩग़")]
  elif bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩज़") in os.environ:
    return os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪड़")]
  else:
    return None
def bstack1ll1l11_opy_(config):
  if not bstack1llll11_opy_(config) or not bstack11l1l11_opy_(config):
    return True
  else:
    return False
def bstack1ll1l1_opy_(config):
  if bstack1lll1l1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩढ़")):
    return False
  if bstack1lll1l1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪफ़")):
    return True
  if bstack1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬय़") in config and config[bstack1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ॠ")] == False:
    return False
  else:
    return True
def bstack11111_opy_(config, index = 0):
  bstack1l111l_opy_ = {}
  if bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ") in config:
    for bstack1ll11l_opy_ in config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index]:
      if bstack1ll11l_opy_ in bstack111l_opy_ + bstackl_opy_ + [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॣ"), bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")]:
        continue
      bstack1l111l_opy_[bstack1ll11l_opy_] = config[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack1ll11l_opy_]
  for key in config:
    if key in bstack111l_opy_ + bstackl_opy_ + [bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ०")]:
      continue
    bstack1l111l_opy_[key] = config[key]
  return bstack1l111l_opy_
def bstack1ll1ll_opy_(config):
  bstack1ll1111_opy_ = {}
  for key in bstackl_opy_:
    if key in config:
      bstack1ll1111_opy_[key] = config[key]
  return bstack1ll1111_opy_
def bstack1l1l1l1_opy_(bstack1l111l_opy_, bstack1ll1111_opy_):
  bstack1111l1l_opy_ = {}
  for key in bstack1l111l_opy_.keys():
    if key in bstack1lll1_opy_:
      bstack1111l1l_opy_[bstack1lll1_opy_[key]] = bstack1l111l_opy_[key]
    else:
      bstack1111l1l_opy_[key] = bstack1l111l_opy_[key]
  for key in bstack1ll1111_opy_:
    if key in bstack1lll1_opy_:
      bstack1111l1l_opy_[bstack1lll1_opy_[key]] = bstack1ll1111_opy_[key]
    else:
      bstack1111l1l_opy_[key] = bstack1ll1111_opy_[key]
  return bstack1111l1l_opy_
def bstack1lll11l1_opy_(config, index = 0):
  caps = {}
  bstack1ll1111_opy_ = bstack1ll1ll_opy_(config)
  if bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ१") in config:
    if bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ२") in config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ३")][index]:
      caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")] = config[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭५")][index][bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")]
    if bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७") in config[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ८")][index]:
      caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९")] = str(config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॰")][index][bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॱ")])
    bstack111lll1_opy_ = {}
    for bstack11ll1ll_opy_ in bstackl_opy_:
      if bstack11ll1ll_opy_ in config[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॲ")][index]:
        bstack111lll1_opy_[bstack11ll1ll_opy_] = config[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॳ")][index][bstack11ll1ll_opy_]
        del(config[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॴ")][index][bstack11ll1ll_opy_])
    bstack1ll1111_opy_.update(bstack111lll1_opy_)
  bstack1l111l_opy_ = bstack11111_opy_(config, index)
  if bstack1ll1l1_opy_(config):
    bstack1l111l_opy_[bstack1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ॵ")] = True
    caps.update(bstack1ll1111_opy_)
    caps[bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨॶ")] = bstack1l111l_opy_
  else:
    bstack1l111l_opy_[bstack1l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨॷ")] = False
    caps.update(bstack1l1l1l1_opy_(bstack1l111l_opy_, bstack1ll1111_opy_))
    if bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॸ") in caps:
      caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫॹ")] = caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॺ")]
      del(caps[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॻ")])
    if bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧॼ") in caps:
      caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩॽ")] = caps[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩॾ")]
      del(caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॿ")])
  return caps
def bstack1lll11l_opy_():
  if bstack1lll1l1l_opy_() <= version.parse(bstack1l1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪঀ")):
    return bstack1_opy_
  return bstack1l11l_opy_
def bstack11l11l1_opy_(options):
  return hasattr(options, bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬঁ"))
def bstack1l1ll11_opy_(caps):
  browser = bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬং")
  if bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫঃ") in caps:
    browser = caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ঄")]
  elif bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩঅ") in caps:
    browser = caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪআ")]
  browser = str(browser).lower()
  if browser == bstack1l1_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧࠪই") or browser == bstack1l1_opy_ (u"ࠫ࡮ࡶࡡࡥࠩঈ"):
    browser = bstack1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬউ")
  if browser == bstack1l1_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭ࠧঊ"):
    browser = bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঋ")
  if browser not in [bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨঌ"), bstack1l1_opy_ (u"ࠩࡨࡨ࡬࡫ࠧ঍"), bstack1l1_opy_ (u"ࠪ࡭ࡪ࠭঎"), bstack1l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫএ"), bstack1l1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ঐ")]:
    return None
  try:
    package = bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ঑").format(browser)
    name = bstack1l1_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨ঒")
    browser_options = getattr(__import__(package, fromlist=[name]), name)
    options = browser_options()
    if not bstack11l11l1_opy_(options):
      return None
    for bstack1l1l1l_opy_ in caps.keys():
      options.set_capability(bstack1l1l1l_opy_, caps[bstack1l1l1l_opy_])
    return options
  except Exception as e:
    logger.debug(str(e))
    return None
def bstack1ll111l1_opy_(options, bstack1ll1l1l1_opy_):
  if not bstack11l11l1_opy_(options):
    return
  for bstack1l1l1l_opy_ in bstack1ll1l1l1_opy_.keys():
    options.set_capability(bstack1l1l1l_opy_, bstack1ll1l1l1_opy_[bstack1l1l1l_opy_])
  if bstack1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧও") in options._caps:
    if options._caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঔ")] and options._caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨক")].lower() != bstack1l1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬখ"):
      del options._caps[bstack1l1_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫগ")]
def bstack1lll1lll_opy_(proxy_config):
  if bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪঘ") in proxy_config:
    proxy_config[bstack1l1_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩঙ")] = proxy_config[bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬচ")]
    del(proxy_config[bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ছ")])
  if bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭জ") in proxy_config and proxy_config[bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧঝ")].lower() != bstack1l1_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬঞ"):
    proxy_config[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩট")] = bstack1l1_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧঠ")
  if bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭ড") in proxy_config:
    proxy_config[bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬঢ")] = bstack1l1_opy_ (u"ࠪࡴࡦࡩࠧণ")
  return proxy_config
def bstack1l11l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪত") in config:
    return proxy
  config[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫথ")] = bstack1lll1lll_opy_(config[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬদ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ধ")])
  return proxy
def bstack1ll1l111_opy_(self):
  global CONFIG
  global bstack1l1lll_opy_
  if bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫন") in CONFIG and bstack1lll11l_opy_().startswith(bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࠪ঩")):
    return CONFIG[bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭প")]
  elif bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨফ") in CONFIG and bstack1lll11l_opy_().startswith(bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠧব")):
    return CONFIG[bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪভ")]
  else:
    return bstack1l1lll_opy_(self)
def bstack11l1ll_opy_():
  if bstack1lll1l1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠧ࠵࠰࠳࠲࠵࠭ম")):
    logger.warning(bstack1111l11_opy_.format(bstack1lll1l1l_opy_()))
    return
  global bstack1l1lll_opy_
  from selenium.webdriver.remote.remote_connection import RemoteConnection
  bstack1l1lll_opy_ = RemoteConnection._get_proxy_url
  RemoteConnection._get_proxy_url = bstack1ll1l111_opy_
def bstack1ll11111_opy_(config):
  if bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬয") in config:
    if str(config[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭র")]).lower() == bstack1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨ঱"):
      return True
    else:
      return False
  elif bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࠩল") in os.environ:
    if str(os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪ঳")]).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ঴"):
      return True
    else:
      return False
  else:
    return False
def bstack1ll111ll_opy_(config):
  if bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঵") in config:
    return config[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬশ")]
  if bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨষ") in config:
    return config[bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩস")]
  return {}
def bstack1llll1l1_opy_(caps):
  global bstack11l1ll1_opy_
  if bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬহ") in caps:
    caps[bstack1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭঺")][bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ঻")] = True
    if bstack11l1ll1_opy_:
      caps[bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ়")][bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")] = bstack11l1ll1_opy_
  else:
    caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧা")] = True
    if bstack11l1ll1_opy_:
      caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫি")] = bstack11l1ll1_opy_
def bstack11ll11_opy_():
  global CONFIG
  if bstack1ll11111_opy_(CONFIG):
    bstack1lllllll_opy_ = bstack1ll111ll_opy_(CONFIG)
    bstack1lllll1l_opy_(bstack11l1l11_opy_(CONFIG), bstack1lllllll_opy_)
def bstack1lllll1l_opy_(key, bstack1lllllll_opy_):
  global bstack1lll1l11_opy_
  logger.info(bstack1ll1l1ll_opy_)
  try:
    bstack1lll1l11_opy_ = Local()
    bstack1l11ll_opy_ = {bstack1l1_opy_ (u"ࠫࡰ࡫ࡹࠨী"): key}
    bstack1l11ll_opy_.update(bstack1lllllll_opy_)
    logger.debug(bstack1l111l1_opy_.format(str(bstack1l11ll_opy_)))
    bstack1lll1l11_opy_.start(**bstack1l11ll_opy_)
    if bstack1lll1l11_opy_.isRunning():
      logger.info(bstack111l1ll_opy_)
  except Exception as e:
    bstack1l1llll_opy_(bstack11l1lll_opy_.format(str(e)))
def bstack1l11ll1_opy_():
  global bstack1lll1l11_opy_
  if bstack1lll1l11_opy_.isRunning():
    logger.info(bstack1ll1lll_opy_)
    bstack1lll1l11_opy_.stop()
  bstack1lll1l11_opy_ = None
def bstack111111l_opy_():
  logger.info(bstack1ll1llll_opy_)
  global bstack1lll1l11_opy_
  if bstack1lll1l11_opy_:
    bstack1l11ll1_opy_()
  logger.info(bstack111l1l_opy_)
def bstack1llll1_opy_(self, *args):
  logger.error(bstack1l1lll1_opy_)
  bstack111111l_opy_()
def bstack1l1llll_opy_(err):
  logger.critical(bstack1l1111l_opy_.format(str(err)))
  atexit.unregister(bstack111111l_opy_)
  sys.exit(1)
def bstack1lll1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack111111l_opy_)
  sys.exit(1)
def bstack1111ll1_opy_():
  global CONFIG
  CONFIG = bstack1l1l111_opy_()
  CONFIG = bstack1l11l1l_opy_(CONFIG)
  CONFIG = bstack1lll1ll1_opy_(CONFIG)
  if bstack1ll1l11_opy_(CONFIG):
    bstack1l1llll_opy_(bstack111l11l_opy_)
  CONFIG[bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧু")] = bstack1llll11_opy_(CONFIG)
  CONFIG[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩূ")] = bstack11l1l11_opy_(CONFIG)
  if bstack1111lll_opy_(CONFIG):
    CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ")] = bstack1111lll_opy_(CONFIG)
  bstack11ll111_opy_()
def bstack11ll111_opy_():
  global CONFIG
  global bstack1lllll1_opy_
  bstack1lll111_opy_ = 1
  if bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨৄ") in CONFIG:
    bstack1lll111_opy_ = CONFIG[bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৅")]
  bstack1llll1ll_opy_ = 0
  if bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৆") in CONFIG:
    bstack1llll1ll_opy_ = len(CONFIG[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧে")])
  bstack1lllll1_opy_ = int(bstack1lll111_opy_) * int(bstack1llll1ll_opy_)
def bstack1l1l11_opy_(self):
  return
def bstack1lll1111_opy_(self):
  return
def bstack11ll1l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1llllll1_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack111ll11_opy_
  global bstack1ll11l1_opy_
  global bstack11ll11l_opy_
  global bstack1lll11_opy_
  global bstack1ll11l1l_opy_
  global bstack111l1l1_opy_
  CONFIG[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧৈ")] = str(bstack1ll11l1l_opy_) + str(__version__)
  command_executor = bstack1lll11l_opy_()
  logger.debug(bstack1llllll_opy_.format(command_executor))
  proxy = bstack1l11l1_opy_(CONFIG, proxy)
  bstack11llll1_opy_ = 0 if bstack1ll11l1_opy_ < 0 else bstack1ll11l1_opy_
  if bstack1lll11_opy_ is True:
    bstack11llll1_opy_ = int(threading.current_thread().getName())
  bstack1ll1l1l1_opy_ = bstack1lll11l1_opy_(CONFIG, bstack11llll1_opy_)
  logger.debug(bstack1lll11ll_opy_.format(str(bstack1ll1l1l1_opy_)))
  if bstack1ll11111_opy_(CONFIG):
    bstack1llll1l1_opy_(bstack1ll1l1l1_opy_)
  if options:
    bstack1ll111l1_opy_(options, bstack1ll1l1l1_opy_)
  if desired_capabilities:
    if bstack1lll1l1l_opy_() >= version.parse(bstack1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ৉")):
      desired_capabilities = {}
    else:
      desired_capabilities.update(bstack1ll1l1l1_opy_)
  if not options:
    options = bstack1l1ll11_opy_(bstack1ll1l1l1_opy_)
  if (
      not options and not desired_capabilities
  ) or (
      bstack1lll1l1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭৊")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1l1l1_opy_)
  logger.info(bstack11l1l1l_opy_)
  if bstack1lll1l1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧো")):
    bstack111l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1l1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩৌ")):
    bstack111l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack111l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack111ll11_opy_ = self.session_id
  if bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ্࠭") in CONFIG and bstack1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩৎ") in CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৏")][bstack11llll1_opy_]:
    bstack11ll11l_opy_ = CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৐")][bstack11llll1_opy_][bstack1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ৑")]
  logger.debug(bstack1ll11l11_opy_.format(bstack111ll11_opy_))
def bstack11lll1l_opy_(self, test):
  global CONFIG
  global bstack111ll11_opy_
  global bstack1111l_opy_
  global bstack11ll11l_opy_
  global bstack11ll1l_opy_
  if bstack111ll11_opy_:
    try:
      data = {}
      bstack11lll1_opy_ = None
      if test:
        bstack11lll1_opy_ = str(test.data)
      if bstack11lll1_opy_ and not bstack11ll11l_opy_:
        data[bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭৒")] = bstack11lll1_opy_
      if bstack1111l_opy_:
        if bstack1111l_opy_.status == bstack1l1_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ৓"):
          data[bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ৔")] = bstack1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ৕")
        elif bstack1111l_opy_.status == bstack1l1_opy_ (u"ࠬࡌࡁࡊࡎࠪ৖"):
          data[bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ৗ")] = bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ৘")
          if bstack1111l_opy_.message:
            data[bstack1l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ৙")] = str(bstack1111l_opy_.message)
      user = CONFIG[bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৚")]
      key = CONFIG[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৛")]
      url = bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩড়").format(user, key, bstack111ll11_opy_)
      headers = {
        bstack1l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫঢ়"): bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ৞"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11l11ll_opy_.format(str(e)))
  bstack11ll1l_opy_(self, test)
def bstack1ll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll11l_opy_
  bstack1llll11l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1111l_opy_
  bstack1111l_opy_ = self._test
def bstack1l1111_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l1_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢয়"), bstack1l1_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧৠ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l1_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࡦ࡬ࡶࠧৡ"), bstack1l1_opy_ (u"ࠥ࠲ࠧৢ")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l1_opy_ (u"ࠦ࠯࠴ࡸ࡮࡮ࠥৣ"))))
  if not files:
    pabot._write(bstack1l1_opy_ (u"ࠬ࡝ࡁࡓࡐ࠽ࠤࡓࡵࠠࡰࡷࡷࡴࡺࡺࠠࡧ࡫࡯ࡩࡸࠦࡩ࡯ࠢࠥࠩࡸࠨࠧ৤") % outs_dir, pabot.Color.YELLOW)
    return bstack1l1_opy_ (u"ࠨࠢ৥")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1llll111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ০") in options:
    del options[bstack1l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ১")]
  if ROBOT_VERSION < bstack1l1_opy_ (u"ࠤ࠷࠲࠵ࠨ২"):
    stats = {
      bstack1l1_opy_ (u"ࠥࡧࡷ࡯ࡴࡪࡥࡤࡰࠧ৩"): {bstack1l1_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥ৪"): 0, bstack1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ৫"): 0, bstack1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ৬"): 0},
      bstack1l1_opy_ (u"ࠢࡢ࡮࡯ࠦ৭"): {bstack1l1_opy_ (u"ࠣࡶࡲࡸࡦࡲࠢ৮"): 0, bstack1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ৯"): 0, bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥৰ"): 0},
    }
  else:
    stats = {
      bstack1l1_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥৱ"): 0,
      bstack1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ৲"): 0,
      bstack1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ৳"): 0,
      bstack1l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣ৴"): 0,
    }
  if pabot_args[bstack1l1_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢ৵")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l1_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ৶")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l1_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸࠨ৷")], pabot_args[bstack1l1_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࡩ࡯ࡵࡸࡦ࡫ࡵ࡬ࡥࡧࡵࡷࠧ৸")]
      )
      outputs += [
        bstack1l1111_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l1_opy_ (u"ࠧ࠵ࠢ৹")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l1_opy_ (u"ࠨࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸࠨ৺"), bstack1l1_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠥࡴ࠰ࡻࡱࡱࠨ৻") % index),
        )
      ]
    if bstack1l1_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣৼ") not in options:
      options[bstack1l1_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤ৽")] = bstack1l1_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠢ৾")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll111l_opy_(self, ff_profile_dir):
  global bstack11lll11_opy_
  if not ff_profile_dir:
    return None
  return bstack11lll11_opy_(self, ff_profile_dir)
def bstack11111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1ll1_opy_
  bstack1lll111l_opy_ = []
  if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৿") in CONFIG:
    bstack1lll111l_opy_ = CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਀")]
  bstack1111l1_opy_ = len(suite_group) * len(pabot_args[bstack1l1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨਁ")] or [(bstack1l1_opy_ (u"ࠢࠣਂ"), None)]) * len(bstack1lll111l_opy_)
  pabot_args[bstack1l1_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢਃ")] = []
  for q in range(bstack1111l1_opy_):
    pabot_args[bstack1l1_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ਄")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦਅ")],
      pabot_args[bstack1l1_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧਆ")],
      argfile,
      pabot_args.get(bstack1l1_opy_ (u"ࠧ࡮ࡩࡷࡧࠥਇ")),
      pabot_args[bstack1l1_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤਈ")],
      platform[0],
      bstack11l1ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢਉ")] or [(bstack1l1_opy_ (u"ࠣࠤਊ"), None)]
    for platform in enumerate(bstack1lll111l_opy_)
  ]
def bstack1111111_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11lllll_opy_=bstack1l1_opy_ (u"ࠩࠪ਋")):
  global bstack1l1l1ll_opy_
  self.platform_index = platform_index
  self.bstack11l11_opy_ = bstack11lllll_opy_
  bstack1l1l1ll_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1l11l_opy_
  if not bstack1l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ਌") in item.options:
    item.options[bstack1l1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭਍")] = []
  for v in item.options[bstack1l1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ਎")]:
    if bstack1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬਏ") in v:
      item.options[bstack1l1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩਐ")].remove(v)
  item.options[bstack1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ਑")].insert(0, bstack1l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ਒").format(item.platform_index))
  item.options[bstack1l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬਓ")].insert(0, bstack1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫਔ").format(item.bstack11l11_opy_))
  return bstack1ll1l11l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11l11_opy_
  command[0] = command[0].replace(bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਕ"), bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪਖ"), 1)
  return bstack1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l111_opy_(bstack11111l1_opy_):
  global bstack1ll11l1l_opy_
  bstack1ll11l1l_opy_ = bstack11111l1_opy_
  logger.info(bstack1lll1l1_opy_.format(bstack1ll11l1l_opy_.split(bstack1l1_opy_ (u"ࠧ࠮ࠩਗ"))[0]))
  global bstack111l1l1_opy_
  global bstack11ll1l_opy_
  global bstack1llll11l_opy_
  global bstack11lll11_opy_
  global bstack1l11l11_opy_
  global bstack1l1l1ll_opy_
  global bstack1ll1l11l_opy_
  global bstack1l111ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1lll1ll_opy_(e, bstack11111ll_opy_)
  Service.start = bstack1l1l11_opy_
  Service.stop = bstack1lll1111_opy_
  webdriver.Remote.__init__ = bstack1llllll1_opy_
  WebDriver.close = bstack11ll1l1_opy_
  if (bstack1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧਘ") in str(bstack11111l1_opy_).lower() or bstack1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨਙ") in str(bstack11111l1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1lllll_opy_)
    Output.end_test = bstack11lll1l_opy_
    TestStatus.__init__ = bstack1ll111_opy_
    WebDriverCreator._get_ff_profile = bstack1ll111l_opy_
  if (bstack1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩਚ") in str(bstack11111l1_opy_).lower()):
    try:
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1ll11ll_opy_)
    QueueItem.__init__ = bstack1111111_opy_
    pabot._create_items = bstack11111l_opy_
    pabot._run = bstack1lll1l_opy_
    pabot._create_command_for_execution = bstack1ll1l1l_opy_
    pabot._report_results = bstack1llll111_opy_
def bstack111l11_opy_(bstack11l1l1_opy_, index):
  bstack11l111_opy_(bstack11ll1_opy_)
  exec(open(bstack11l1l1_opy_).read())
def bstack1ll1ll1_opy_():
  print(bstack1llll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪਛ"), help=bstack1l1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ਜ"))
  parser.add_argument(bstack1l1_opy_ (u"࠭࠭ࡶࠩਝ"), bstack1l1_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫਞ"), help=bstack1l1_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧਟ"))
  parser.add_argument(bstack1l1_opy_ (u"ࠩ࠰࡯ࠬਠ"), bstack1l1_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩਡ"), help=bstack1l1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬਢ"))
  bstack1lllll11_opy_ = parser.parse_args()
  try:
    bstack111l111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨਣ"))
    bstack11llll_opy_ = open(bstack111l111_opy_, bstack1l1_opy_ (u"࠭ࡲࠨਤ"))
    bstack1ll11lll_opy_ = bstack11llll_opy_.read()
    bstack11llll_opy_.close()
    if bstack1lllll11_opy_.username:
      bstack1ll11lll_opy_ = bstack1ll11lll_opy_.replace(bstack1l1_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧਥ"), bstack1lllll11_opy_.username)
    if bstack1lllll11_opy_.key:
      bstack1ll11lll_opy_ = bstack1ll11lll_opy_.replace(bstack1l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪਦ"), bstack1lllll11_opy_.key)
    file_name = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬਧ")
    file_path = os.path.abspath(file_name)
    bstack111l1_opy_ = open(file_path, bstack1l1_opy_ (u"ࠪࡻࠬਨ"))
    bstack111l1_opy_.write(bstack1ll11lll_opy_)
    bstack111l1_opy_.close()
    print(bstack1l1l11l_opy_)
  except Exception as e:
    print(bstack1l11lll_opy_.format(str(e)))
def bstack1l11111_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack1111ll1_opy_()
  bstack1ll1ll1l_opy_()
  atexit.register(bstack111111l_opy_)
  signal.signal(signal.SIGINT, bstack1llll1_opy_)
  signal.signal(signal.SIGTERM, bstack1llll1_opy_)
def run_on_browserstack(args):
  if sys.argv[1] == bstack1l1_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧ਩")  or sys.argv[1] == bstack1l1_opy_ (u"ࠬ࠳ࡶࠨਪ"):
    print(bstack1l1_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ਫ").format(__version__))
    return
  if sys.argv[1] == bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ਬ"):
    bstack1ll1ll1_opy_()
    return
  bstack1l11111_opy_()
  global CONFIG
  global bstack1lllll1_opy_
  global bstack1lll11_opy_
  global bstack1ll11l1_opy_
  global bstack11l1ll1_opy_
  bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠨࠩਭ")
  if args[1] == bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩਮ") or args[1] == bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫਯ"):
    bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫਰ")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ਱"):
    bstack1l1ll1_opy_ = bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ਲ਼"):
    bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ਴")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪਵ"):
    bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫਸ਼")
    args = args[2:]
  else:
    if not bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ਷") in CONFIG or str(CONFIG[bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨਸ")]).lower() in [bstack1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ਹ"), bstack1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ਺")]:
      bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ਻")
      args = args[1:]
    elif str(CONFIG[bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯਼ࠬ")]).lower() == bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ਽"):
      bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਾ")
      args = args[1:]
    elif str(CONFIG[bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨਿ")]).lower() == bstack1l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬੀ"):
      bstack1l1ll1_opy_ = bstack1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ੁ")
      args = args[1:]
    else:
      bstack1l1llll_opy_(bstack11l11l_opy_)
  global bstack111l1l1_opy_
  global bstack11ll1l_opy_
  global bstack1llll11l_opy_
  global bstack11lll11_opy_
  global bstack1l11l11_opy_
  global bstack1l1l1ll_opy_
  global bstack1ll1l11l_opy_
  global bstack1l111ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1lll1ll_opy_(e, bstack11111ll_opy_)
  bstack111l1l1_opy_ = webdriver.Remote.__init__
  bstack1l111ll_opy_ = WebDriver.close
  if (bstack1l1ll1_opy_ in [bstack1l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧੂ"), bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃"), bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ੄")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1lllll_opy_)
    bstack11ll1l_opy_ = Output.end_test
    bstack1llll11l_opy_ = TestStatus.__init__
    bstack11lll11_opy_ = WebDriverCreator._get_ff_profile
  if (bstack1l1ll1_opy_ in [bstack1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ੅"), bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭੆")]):
    try:
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1ll11ll_opy_)
    bstack1l11l11_opy_ = pabot._run
    bstack1l1l1ll_opy_ = QueueItem.__init__
    bstack1ll1l11l_opy_ = pabot._create_command_for_execution
  if bstack1l1ll1_opy_ == bstack1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ੇ"):
    bstack11ll11_opy_()
    if bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪੈ") in CONFIG:
      bstack1lll11_opy_ = True
      bstack11l111l_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")]):
        bstack11l111l_opy_.append(threading.Thread(name=str(index),
                                      target=bstack111l11_opy_, args=(args[0], index)))
      for t in bstack11l111l_opy_:
        t.start()
      for t in bstack11l111l_opy_:
        t.join()
    else:
      bstack11l111_opy_(bstack11ll1_opy_)
      exec(open(args[0]).read())
  elif bstack1l1ll1_opy_ == bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੊"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1lllll_opy_)
    bstack11ll11_opy_()
    bstack11l111_opy_(bstack1l1ll_opy_)
    run_cli(args)
  elif bstack1l1ll1_opy_ == bstack1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩੋ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1ll11ll_opy_)
    bstack11ll11_opy_()
    bstack11l111_opy_(bstack11l1l_opy_)
    if bstack1l1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩੌ") in args:
      i = args.index(bstack1l1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵ੍ࠪ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lllll1_opy_))
    args.insert(0, str(bstack1l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੎")))
    pabot.main(args)
  elif bstack1l1ll1_opy_ == bstack1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ੏"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll1ll_opy_(e, bstack1lllll_opy_)
    for a in args:
      if bstack1l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ੐") in a:
        bstack1ll11l1_opy_ = int(a.split(bstack1l1_opy_ (u"ࠩ࠽ࠫੑ"))[1])
      if bstack1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ੒") in a:
        bstack11l1ll1_opy_ = str(a.split(bstack1l1_opy_ (u"ࠫ࠿࠭੓"))[1])
    bstack11l111_opy_(bstack11l1l_opy_)
    run_cli(args)
  else:
    bstack1l1llll_opy_(bstack11l11l_opy_)