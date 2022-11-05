# Copyright 2021 SpinQ Technology Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generated from Qasm2.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2Y")
        buf.write("\u027d\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\t")
        buf.write("U\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4")
        buf.write("^\t^\4_\t_\4`\t`\4a\ta\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\21")
        buf.write("\3\21\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\25\3\25")
        buf.write("\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\32\3\32")
        buf.write("\3\32\3\33\3\33\3\33\3\34\3\34\3\34\3\35\3\35\3\35\3\36")
        buf.write("\3\36\3\37\3\37\3 \3 \3!\3!\3!\3\"\3\"\3\"\3#\3#\3#\3")
        buf.write("#\3#\3$\3$\3$\3$\3$\3$\3%\3%\3%\3&\3&\3&\3\'\3\'\3\'\3")
        buf.write("\'\3(\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3+\3+\3+\3,\3,")
        buf.write("\3,\3,\3,\3-\3-\3-\3-\3-\3.\3.\3.\3.\3.\3/\3/\3/\3/\3")
        buf.write("/\3/\3/\3/\3/\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60")
        buf.write("\3\60\3\61\3\61\3\61\3\62\3\62\3\62\3\63\3\63\3\63\3\64")
        buf.write("\3\64\3\64\3\65\3\65\3\65\3\66\3\66\3\66\3\67\3\67\3\67")
        buf.write("\38\38\38\39\39\39\39\3:\3:\3:\3:\3;\3;\3;\3<\3<\3<\3")
        buf.write("<\3<\3=\3=\3>\3>\3?\3?\3@\3@\3A\3A\3B\3B\3C\3C\3D\3D\3")
        buf.write("E\3E\3F\3F\3G\3G\3H\3H\3H\3I\3I\3J\3J\3K\3K\3L\3L\3M\3")
        buf.write("M\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\5N\u01ee")
        buf.write("\nN\3O\6O\u01f1\nO\rO\16O\u01f2\3O\3O\3P\6P\u01f8\nP\r")
        buf.write("P\16P\u01f9\3P\3P\3Q\3Q\3R\6R\u0201\nR\rR\16R\u0202\3")
        buf.write("S\3S\3T\3T\3U\3U\3U\5U\u020c\nU\3V\3V\5V\u0210\nV\3W\3")
        buf.write("W\3W\3W\3W\3W\3W\3W\3W\7W\u021b\nW\fW\16W\u021e\13W\3")
        buf.write("X\3X\7X\u0222\nX\fX\16X\u0225\13X\3Y\3Y\3Z\3Z\5Z\u022b")
        buf.write("\nZ\3[\6[\u022e\n[\r[\16[\u022f\3[\3[\7[\u0234\n[\f[\16")
        buf.write("[\u0237\13[\3\\\3\\\3\\\5\\\u023c\n\\\3\\\3\\\5\\\u0240")
        buf.write("\n\\\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\5]\u024d\n]\3^\3")
        buf.write("^\5^\u0251\n^\3^\3^\3_\3_\6_\u0257\n_\r_\16_\u0258\3_")
        buf.write("\3_\3_\6_\u025e\n_\r_\16_\u025f\3_\5_\u0263\n_\3`\3`\3")
        buf.write("`\3`\7`\u0269\n`\f`\16`\u026c\13`\3`\3`\3a\3a\3a\3a\7")
        buf.write("a\u0274\na\fa\16a\u0277\13a\3a\3a\3a\3a\3a\5\u0258\u025f")
        buf.write("\u0275\2b\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write("\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+")
        buf.write("\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E")
        buf.write("$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k")
        buf.write("\67m8o9q:s;u<w=y>{?}@\177A\u0081B\u0083C\u0085D\u0087")
        buf.write("E\u0089F\u008bG\u008dH\u008fI\u0091J\u0093K\u0095L\u0097")
        buf.write("M\u0099N\u009bO\u009dP\u009fQ\u00a1\2\u00a3R\u00a5\2\u00a7")
        buf.write("\2\u00a9\2\u00ab\2\u00adS\u00afT\u00b1\2\u00b3\2\u00b5")
        buf.write("\2\u00b7U\u00b9\2\u00bbV\u00bdW\u00bfX\u00c1Y\3\2\n\4")
        buf.write("\2\13\13\"\"\4\2\f\f\17\17\3\2\62;\4\2C\\c|\4\2&&aa\4")
        buf.write("\2GGgg\5\2\13\f\17\17$$\5\2\13\f\17\17))\3\u024e\2C\2")
        buf.write("\\\2c\2|\2\u00ac\2\u00ac\2\u00b7\2\u00b7\2\u00bc\2\u00bc")
        buf.write("\2\u00c2\2\u00d8\2\u00da\2\u00f8\2\u00fa\2\u02c3\2\u02c8")
        buf.write("\2\u02d3\2\u02e2\2\u02e6\2\u02ee\2\u02ee\2\u02f0\2\u02f0")
        buf.write("\2\u0372\2\u0376\2\u0378\2\u0379\2\u037c\2\u037f\2\u0381")
        buf.write("\2\u0381\2\u0388\2\u0388\2\u038a\2\u038c\2\u038e\2\u038e")
        buf.write("\2\u0390\2\u03a3\2\u03a5\2\u03f7\2\u03f9\2\u0483\2\u048c")
        buf.write("\2\u0531\2\u0533\2\u0558\2\u055b\2\u055b\2\u0563\2\u0589")
        buf.write("\2\u05d2\2\u05ec\2\u05f2\2\u05f4\2\u0622\2\u064c\2\u0670")
        buf.write("\2\u0671\2\u0673\2\u06d5\2\u06d7\2\u06d7\2\u06e7\2\u06e8")
        buf.write("\2\u06f0\2\u06f1\2\u06fc\2\u06fe\2\u0701\2\u0701\2\u0712")
        buf.write("\2\u0712\2\u0714\2\u0731\2\u074f\2\u07a7\2\u07b3\2\u07b3")
        buf.write("\2\u07cc\2\u07ec\2\u07f6\2\u07f7\2\u07fc\2\u07fc\2\u0802")
        buf.write("\2\u0817\2\u081c\2\u081c\2\u0826\2\u0826\2\u082a\2\u082a")
        buf.write("\2\u0842\2\u085a\2\u0862\2\u086c\2\u08a2\2\u08b6\2\u08b8")
        buf.write("\2\u08bf\2\u0906\2\u093b\2\u093f\2\u093f\2\u0952\2\u0952")
        buf.write("\2\u095a\2\u0963\2\u0973\2\u0982\2\u0987\2\u098e\2\u0991")
        buf.write("\2\u0992\2\u0995\2\u09aa\2\u09ac\2\u09b2\2\u09b4\2\u09b4")
        buf.write("\2\u09b8\2\u09bb\2\u09bf\2\u09bf\2\u09d0\2\u09d0\2\u09de")
        buf.write("\2\u09df\2\u09e1\2\u09e3\2\u09f2\2\u09f3\2\u09fe\2\u09fe")
        buf.write("\2\u0a07\2\u0a0c\2\u0a11\2\u0a12\2\u0a15\2\u0a2a\2\u0a2c")
        buf.write("\2\u0a32\2\u0a34\2\u0a35\2\u0a37\2\u0a38\2\u0a3a\2\u0a3b")
        buf.write("\2\u0a5b\2\u0a5e\2\u0a60\2\u0a60\2\u0a74\2\u0a76\2\u0a87")
        buf.write("\2\u0a8f\2\u0a91\2\u0a93\2\u0a95\2\u0aaa\2\u0aac\2\u0ab2")
        buf.write("\2\u0ab4\2\u0ab5\2\u0ab7\2\u0abb\2\u0abf\2\u0abf\2\u0ad2")
        buf.write("\2\u0ad2\2\u0ae2\2\u0ae3\2\u0afb\2\u0afb\2\u0b07\2\u0b0e")
        buf.write("\2\u0b11\2\u0b12\2\u0b15\2\u0b2a\2\u0b2c\2\u0b32\2\u0b34")
        buf.write("\2\u0b35\2\u0b37\2\u0b3b\2\u0b3f\2\u0b3f\2\u0b5e\2\u0b5f")
        buf.write("\2\u0b61\2\u0b63\2\u0b73\2\u0b73\2\u0b85\2\u0b85\2\u0b87")
        buf.write("\2\u0b8c\2\u0b90\2\u0b92\2\u0b94\2\u0b97\2\u0b9b\2\u0b9c")
        buf.write("\2\u0b9e\2\u0b9e\2\u0ba0\2\u0ba1\2\u0ba5\2\u0ba6\2\u0baa")
        buf.write("\2\u0bac\2\u0bb0\2\u0bbb\2\u0bd2\2\u0bd2\2\u0c07\2\u0c0e")
        buf.write("\2\u0c10\2\u0c12\2\u0c14\2\u0c2a\2\u0c2c\2\u0c3b\2\u0c3f")
        buf.write("\2\u0c3f\2\u0c5a\2\u0c5c\2\u0c62\2\u0c63\2\u0c82\2\u0c82")
        buf.write("\2\u0c87\2\u0c8e\2\u0c90\2\u0c92\2\u0c94\2\u0caa\2\u0cac")
        buf.write("\2\u0cb5\2\u0cb7\2\u0cbb\2\u0cbf\2\u0cbf\2\u0ce0\2\u0ce0")
        buf.write("\2\u0ce2\2\u0ce3\2\u0cf3\2\u0cf4\2\u0d07\2\u0d0e\2\u0d10")
        buf.write("\2\u0d12\2\u0d14\2\u0d3c\2\u0d3f\2\u0d3f\2\u0d50\2\u0d50")
        buf.write("\2\u0d56\2\u0d58\2\u0d61\2\u0d63\2\u0d7c\2\u0d81\2\u0d87")
        buf.write("\2\u0d98\2\u0d9c\2\u0db3\2\u0db5\2\u0dbd\2\u0dbf\2\u0dbf")
        buf.write("\2\u0dc2\2\u0dc8\2\u0e03\2\u0e32\2\u0e34\2\u0e35\2\u0e42")
        buf.write("\2\u0e48\2\u0e83\2\u0e84\2\u0e86\2\u0e86\2\u0e89\2\u0e8a")
        buf.write("\2\u0e8c\2\u0e8c\2\u0e8f\2\u0e8f\2\u0e96\2\u0e99\2\u0e9b")
        buf.write("\2\u0ea1\2\u0ea3\2\u0ea5\2\u0ea7\2\u0ea7\2\u0ea9\2\u0ea9")
        buf.write("\2\u0eac\2\u0ead\2\u0eaf\2\u0eb2\2\u0eb4\2\u0eb5\2\u0ebf")
        buf.write("\2\u0ebf\2\u0ec2\2\u0ec6\2\u0ec8\2\u0ec8\2\u0ede\2\u0ee1")
        buf.write("\2\u0f02\2\u0f02\2\u0f42\2\u0f49\2\u0f4b\2\u0f6e\2\u0f8a")
        buf.write("\2\u0f8e\2\u1002\2\u102c\2\u1041\2\u1041\2\u1052\2\u1057")
        buf.write("\2\u105c\2\u105f\2\u1063\2\u1063\2\u1067\2\u1068\2\u1070")
        buf.write("\2\u1072\2\u1077\2\u1083\2\u1090\2\u1090\2\u10a2\2\u10c7")
        buf.write("\2\u10c9\2\u10c9\2\u10cf\2\u10cf\2\u10d2\2\u10fc\2\u10fe")
        buf.write("\2\u124a\2\u124c\2\u124f\2\u1252\2\u1258\2\u125a\2\u125a")
        buf.write("\2\u125c\2\u125f\2\u1262\2\u128a\2\u128c\2\u128f\2\u1292")
        buf.write("\2\u12b2\2\u12b4\2\u12b7\2\u12ba\2\u12c0\2\u12c2\2\u12c2")
        buf.write("\2\u12c4\2\u12c7\2\u12ca\2\u12d8\2\u12da\2\u1312\2\u1314")
        buf.write("\2\u1317\2\u131a\2\u135c\2\u1382\2\u1391\2\u13a2\2\u13f7")
        buf.write("\2\u13fa\2\u13ff\2\u1403\2\u166e\2\u1671\2\u1681\2\u1683")
        buf.write("\2\u169c\2\u16a2\2\u16ec\2\u16f0\2\u16fa\2\u1702\2\u170e")
        buf.write("\2\u1710\2\u1713\2\u1722\2\u1733\2\u1742\2\u1753\2\u1762")
        buf.write("\2\u176e\2\u1770\2\u1772\2\u1782\2\u17b5\2\u17d9\2\u17d9")
        buf.write("\2\u17de\2\u17de\2\u1822\2\u1879\2\u1882\2\u1886\2\u1889")
        buf.write("\2\u18aa\2\u18ac\2\u18ac\2\u18b2\2\u18f7\2\u1902\2\u1920")
        buf.write("\2\u1952\2\u196f\2\u1972\2\u1976\2\u1982\2\u19ad\2\u19b2")
        buf.write("\2\u19cb\2\u1a02\2\u1a18\2\u1a22\2\u1a56\2\u1aa9\2\u1aa9")
        buf.write("\2\u1b07\2\u1b35\2\u1b47\2\u1b4d\2\u1b85\2\u1ba2\2\u1bb0")
        buf.write("\2\u1bb1\2\u1bbc\2\u1be7\2\u1c02\2\u1c25\2\u1c4f\2\u1c51")
        buf.write("\2\u1c5c\2\u1c7f\2\u1c82\2\u1c8a\2\u1ceb\2\u1cee\2\u1cf0")
        buf.write("\2\u1cf3\2\u1cf7\2\u1cf8\2\u1d02\2\u1dc1\2\u1e02\2\u1f17")
        buf.write("\2\u1f1a\2\u1f1f\2\u1f22\2\u1f47\2\u1f4a\2\u1f4f\2\u1f52")
        buf.write("\2\u1f59\2\u1f5b\2\u1f5b\2\u1f5d\2\u1f5d\2\u1f5f\2\u1f5f")
        buf.write("\2\u1f61\2\u1f7f\2\u1f82\2\u1fb6\2\u1fb8\2\u1fbe\2\u1fc0")
        buf.write("\2\u1fc0\2\u1fc4\2\u1fc6\2\u1fc8\2\u1fce\2\u1fd2\2\u1fd5")
        buf.write("\2\u1fd8\2\u1fdd\2\u1fe2\2\u1fee\2\u1ff4\2\u1ff6\2\u1ff8")
        buf.write("\2\u1ffe\2\u2073\2\u2073\2\u2081\2\u2081\2\u2092\2\u209e")
        buf.write("\2\u2104\2\u2104\2\u2109\2\u2109\2\u210c\2\u2115\2\u2117")
        buf.write("\2\u2117\2\u211b\2\u211f\2\u2126\2\u2126\2\u2128\2\u2128")
        buf.write("\2\u212a\2\u212a\2\u212c\2\u212f\2\u2131\2\u213b\2\u213e")
        buf.write("\2\u2141\2\u2147\2\u214b\2\u2150\2\u2150\2\u2162\2\u218a")
        buf.write("\2\u2c02\2\u2c30\2\u2c32\2\u2c60\2\u2c62\2\u2ce6\2\u2ced")
        buf.write("\2\u2cf0\2\u2cf4\2\u2cf5\2\u2d02\2\u2d27\2\u2d29\2\u2d29")
        buf.write("\2\u2d2f\2\u2d2f\2\u2d32\2\u2d69\2\u2d71\2\u2d71\2\u2d82")
        buf.write("\2\u2d98\2\u2da2\2\u2da8\2\u2daa\2\u2db0\2\u2db2\2\u2db8")
        buf.write("\2\u2dba\2\u2dc0\2\u2dc2\2\u2dc8\2\u2dca\2\u2dd0\2\u2dd2")
        buf.write("\2\u2dd8\2\u2dda\2\u2de0\2\u2e31\2\u2e31\2\u3007\2\u3009")
        buf.write("\2\u3023\2\u302b\2\u3033\2\u3037\2\u303a\2\u303e\2\u3043")
        buf.write("\2\u3098\2\u309f\2\u30a1\2\u30a3\2\u30fc\2\u30fe\2\u3101")
        buf.write("\2\u3107\2\u3130\2\u3133\2\u3190\2\u31a2\2\u31bc\2\u31f2")
        buf.write("\2\u3201\2\u3402\2\u4db7\2\u4e02\2\u9fec\2\ua002\2\ua48e")
        buf.write("\2\ua4d2\2\ua4ff\2\ua502\2\ua60e\2\ua612\2\ua621\2\ua62c")
        buf.write("\2\ua62d\2\ua642\2\ua670\2\ua681\2\ua69f\2\ua6a2\2\ua6f1")
        buf.write("\2\ua719\2\ua721\2\ua724\2\ua78a\2\ua78d\2\ua7b0\2\ua7b2")
        buf.write("\2\ua7b9\2\ua7f9\2\ua803\2\ua805\2\ua807\2\ua809\2\ua80c")
        buf.write("\2\ua80e\2\ua824\2\ua842\2\ua875\2\ua884\2\ua8b5\2\ua8f4")
        buf.write("\2\ua8f9\2\ua8fd\2\ua8fd\2\ua8ff\2\ua8ff\2\ua90c\2\ua927")
        buf.write("\2\ua932\2\ua948\2\ua962\2\ua97e\2\ua986\2\ua9b4\2\ua9d1")
        buf.write("\2\ua9d1\2\ua9e2\2\ua9e6\2\ua9e8\2\ua9f1\2\ua9fc\2\uaa00")
        buf.write("\2\uaa02\2\uaa2a\2\uaa42\2\uaa44\2\uaa46\2\uaa4d\2\uaa62")
        buf.write("\2\uaa78\2\uaa7c\2\uaa7c\2\uaa80\2\uaab1\2\uaab3\2\uaab3")
        buf.write("\2\uaab7\2\uaab8\2\uaabb\2\uaabf\2\uaac2\2\uaac2\2\uaac4")
        buf.write("\2\uaac4\2\uaadd\2\uaadf\2\uaae2\2\uaaec\2\uaaf4\2\uaaf6")
        buf.write("\2\uab03\2\uab08\2\uab0b\2\uab10\2\uab13\2\uab18\2\uab22")
        buf.write("\2\uab28\2\uab2a\2\uab30\2\uab32\2\uab5c\2\uab5e\2\uab67")
        buf.write("\2\uab72\2\uabe4\2\uac02\2\ud7a5\2\ud7b2\2\ud7c8\2\ud7cd")
        buf.write("\2\ud7fd\2\uf902\2\ufa6f\2\ufa72\2\ufadb\2\ufb02\2\ufb08")
        buf.write("\2\ufb15\2\ufb19\2\ufb1f\2\ufb1f\2\ufb21\2\ufb2a\2\ufb2c")
        buf.write("\2\ufb38\2\ufb3a\2\ufb3e\2\ufb40\2\ufb40\2\ufb42\2\ufb43")
        buf.write("\2\ufb45\2\ufb46\2\ufb48\2\ufbb3\2\ufbd5\2\ufd3f\2\ufd52")
        buf.write("\2\ufd91\2\ufd94\2\ufdc9\2\ufdf2\2\ufdfd\2\ufe72\2\ufe76")
        buf.write("\2\ufe78\2\ufefe\2\uff23\2\uff3c\2\uff43\2\uff5c\2\uff68")
        buf.write("\2\uffc0\2\uffc4\2\uffc9\2\uffcc\2\uffd1\2\uffd4\2\uffd9")
        buf.write("\2\uffdc\2\uffde\2\2\3\r\3\17\3(\3*\3<\3>\3?\3A\3O\3R")
        buf.write("\3_\3\u0082\3\u00fc\3\u0142\3\u0176\3\u0282\3\u029e\3")
        buf.write("\u02a2\3\u02d2\3\u0302\3\u0321\3\u032f\3\u034c\3\u0352")
        buf.write("\3\u0377\3\u0382\3\u039f\3\u03a2\3\u03c5\3\u03ca\3\u03d1")
        buf.write("\3\u03d3\3\u03d7\3\u0402\3\u049f\3\u04b2\3\u04d5\3\u04da")
        buf.write("\3\u04fd\3\u0502\3\u0529\3\u0532\3\u0565\3\u0602\3\u0738")
        buf.write("\3\u0742\3\u0757\3\u0762\3\u0769\3\u0802\3\u0807\3\u080a")
        buf.write("\3\u080a\3\u080c\3\u0837\3\u0839\3\u083a\3\u083e\3\u083e")
        buf.write("\3\u0841\3\u0857\3\u0862\3\u0878\3\u0882\3\u08a0\3\u08e2")
        buf.write("\3\u08f4\3\u08f6\3\u08f7\3\u0902\3\u0917\3\u0922\3\u093b")
        buf.write("\3\u0982\3\u09b9\3\u09c0\3\u09c1\3\u0a02\3\u0a02\3\u0a12")
        buf.write("\3\u0a15\3\u0a17\3\u0a19\3\u0a1b\3\u0a35\3\u0a62\3\u0a7e")
        buf.write("\3\u0a82\3\u0a9e\3\u0ac2\3\u0ac9\3\u0acb\3\u0ae6\3\u0b02")
        buf.write("\3\u0b37\3\u0b42\3\u0b57\3\u0b62\3\u0b74\3\u0b82\3\u0b93")
        buf.write("\3\u0c02\3\u0c4a\3\u0c82\3\u0cb4\3\u0cc2\3\u0cf4\3\u1005")
        buf.write("\3\u1039\3\u1085\3\u10b1\3\u10d2\3\u10ea\3\u1105\3\u1128")
        buf.write("\3\u1152\3\u1174\3\u1178\3\u1178\3\u1185\3\u11b4\3\u11c3")
        buf.write("\3\u11c6\3\u11dc\3\u11dc\3\u11de\3\u11de\3\u1202\3\u1213")
        buf.write("\3\u1215\3\u122d\3\u1282\3\u1288\3\u128a\3\u128a\3\u128c")
        buf.write("\3\u128f\3\u1291\3\u129f\3\u12a1\3\u12aa\3\u12b2\3\u12e0")
        buf.write("\3\u1307\3\u130e\3\u1311\3\u1312\3\u1315\3\u132a\3\u132c")
        buf.write("\3\u1332\3\u1334\3\u1335\3\u1337\3\u133b\3\u133f\3\u133f")
        buf.write("\3\u1352\3\u1352\3\u135f\3\u1363\3\u1402\3\u1436\3\u1449")
        buf.write("\3\u144c\3\u1482\3\u14b1\3\u14c6\3\u14c7\3\u14c9\3\u14c9")
        buf.write("\3\u1582\3\u15b0\3\u15da\3\u15dd\3\u1602\3\u1631\3\u1646")
        buf.write("\3\u1646\3\u1682\3\u16ac\3\u1702\3\u171b\3\u18a2\3\u18e1")
        buf.write("\3\u1901\3\u1901\3\u1a02\3\u1a02\3\u1a0d\3\u1a34\3\u1a3c")
        buf.write("\3\u1a3c\3\u1a52\3\u1a52\3\u1a5e\3\u1a85\3\u1a88\3\u1a8b")
        buf.write("\3\u1ac2\3\u1afa\3\u1c02\3\u1c0a\3\u1c0c\3\u1c30\3\u1c42")
        buf.write("\3\u1c42\3\u1c74\3\u1c91\3\u1d02\3\u1d08\3\u1d0a\3\u1d0b")
        buf.write("\3\u1d0d\3\u1d32\3\u1d48\3\u1d48\3\u2002\3\u239b\3\u2402")
        buf.write("\3\u2470\3\u2482\3\u2545\3\u3002\3\u3430\3\u4402\3\u4648")
        buf.write("\3\u6802\3\u6a3a\3\u6a42\3\u6a60\3\u6ad2\3\u6aef\3\u6b02")
        buf.write("\3\u6b31\3\u6b42\3\u6b45\3\u6b65\3\u6b79\3\u6b7f\3\u6b91")
        buf.write("\3\u6f02\3\u6f46\3\u6f52\3\u6f52\3\u6f95\3\u6fa1\3\u6fe2")
        buf.write("\3\u6fe3\3\u7002\3\u87ee\3\u8802\3\u8af4\3\ub002\3\ub120")
        buf.write("\3\ub172\3\ub2fd\3\ubc02\3\ubc6c\3\ubc72\3\ubc7e\3\ubc82")
        buf.write("\3\ubc8a\3\ubc92\3\ubc9b\3\ud402\3\ud456\3\ud458\3\ud49e")
        buf.write("\3\ud4a0\3\ud4a1\3\ud4a4\3\ud4a4\3\ud4a7\3\ud4a8\3\ud4ab")
        buf.write("\3\ud4ae\3\ud4b0\3\ud4bb\3\ud4bd\3\ud4bd\3\ud4bf\3\ud4c5")
        buf.write("\3\ud4c7\3\ud507\3\ud509\3\ud50c\3\ud50f\3\ud516\3\ud518")
        buf.write("\3\ud51e\3\ud520\3\ud53b\3\ud53d\3\ud540\3\ud542\3\ud546")
        buf.write("\3\ud548\3\ud548\3\ud54c\3\ud552\3\ud554\3\ud6a7\3\ud6aa")
        buf.write("\3\ud6c2\3\ud6c4\3\ud6dc\3\ud6de\3\ud6fc\3\ud6fe\3\ud716")
        buf.write("\3\ud718\3\ud736\3\ud738\3\ud750\3\ud752\3\ud770\3\ud772")
        buf.write("\3\ud78a\3\ud78c\3\ud7aa\3\ud7ac\3\ud7c4\3\ud7c6\3\ud7cd")
        buf.write("\3\ue802\3\ue8c6\3\ue902\3\ue945\3\uee02\3\uee05\3\uee07")
        buf.write("\3\uee21\3\uee23\3\uee24\3\uee26\3\uee26\3\uee29\3\uee29")
        buf.write("\3\uee2b\3\uee34\3\uee36\3\uee39\3\uee3b\3\uee3b\3\uee3d")
        buf.write("\3\uee3d\3\uee44\3\uee44\3\uee49\3\uee49\3\uee4b\3\uee4b")
        buf.write("\3\uee4d\3\uee4d\3\uee4f\3\uee51\3\uee53\3\uee54\3\uee56")
        buf.write("\3\uee56\3\uee59\3\uee59\3\uee5b\3\uee5b\3\uee5d\3\uee5d")
        buf.write("\3\uee5f\3\uee5f\3\uee61\3\uee61\3\uee63\3\uee64\3\uee66")
        buf.write("\3\uee66\3\uee69\3\uee6c\3\uee6e\3\uee74\3\uee76\3\uee79")
        buf.write("\3\uee7b\3\uee7e\3\uee80\3\uee80\3\uee82\3\uee8b\3\uee8d")
        buf.write("\3\uee9d\3\ueea3\3\ueea5\3\ueea7\3\ueeab\3\ueead\3\ueebd")
        buf.write("\3\2\4\ua6d8\4\ua702\4\ub736\4\ub742\4\ub81f\4\ub822\4")
        buf.write("\ucea3\4\uceb2\4\uebe2\4\uf802\4\ufa1f\4\u0290\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2")
        buf.write("\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write("\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2")
        buf.write("\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2")
        buf.write("\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2")
        buf.write("\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3")
        buf.write("\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_")
        buf.write("\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2")
        buf.write("i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2")
        buf.write("\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2")
        buf.write("\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3")
        buf.write("\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2")
        buf.write("\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a3\3\2\2\2\2\u00ad\3\2\2\2\2\u00af\3\2\2")
        buf.write("\2\2\u00b7\3\2\2\2\2\u00bb\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf")
        buf.write("\3\2\2\2\2\u00c1\3\2\2\2\3\u00c3\3\2\2\2\5\u00cc\3\2\2")
        buf.write("\2\7\u00d4\3\2\2\2\t\u00d9\3\2\2\2\13\u00df\3\2\2\2\r")
        buf.write("\u00e3\3\2\2\2\17\u00e8\3\2\2\2\21\u00ec\3\2\2\2\23\u00f1")
        buf.write("\3\2\2\2\25\u00f7\3\2\2\2\27\u00fd\3\2\2\2\31\u0103\3")
        buf.write("\2\2\2\33\u0108\3\2\2\2\35\u010e\3\2\2\2\37\u0111\3\2")
        buf.write("\2\2!\u0116\3\2\2\2#\u0118\3\2\2\2%\u011b\3\2\2\2\'\u0123")
        buf.write("\3\2\2\2)\u012b\3\2\2\2+\u012d\3\2\2\2-\u012f\3\2\2\2")
        buf.write("/\u0131\3\2\2\2\61\u0133\3\2\2\2\63\u0136\3\2\2\2\65\u0139")
        buf.write("\3\2\2\2\67\u013c\3\2\2\29\u013f\3\2\2\2;\u0142\3\2\2")
        buf.write("\2=\u0144\3\2\2\2?\u0146\3\2\2\2A\u0148\3\2\2\2C\u014b")
        buf.write("\3\2\2\2E\u014e\3\2\2\2G\u0153\3\2\2\2I\u0159\3\2\2\2")
        buf.write("K\u015c\3\2\2\2M\u015f\3\2\2\2O\u0163\3\2\2\2Q\u0167\3")
        buf.write("\2\2\2S\u016b\3\2\2\2U\u016f\3\2\2\2W\u0172\3\2\2\2Y\u0177")
        buf.write("\3\2\2\2[\u017c\3\2\2\2]\u0181\3\2\2\2_\u018a\3\2\2\2")
        buf.write("a\u0193\3\2\2\2c\u0196\3\2\2\2e\u0199\3\2\2\2g\u019c\3")
        buf.write("\2\2\2i\u019f\3\2\2\2k\u01a2\3\2\2\2m\u01a5\3\2\2\2o\u01a8")
        buf.write("\3\2\2\2q\u01ab\3\2\2\2s\u01af\3\2\2\2u\u01b3\3\2\2\2")
        buf.write("w\u01b6\3\2\2\2y\u01bb\3\2\2\2{\u01bd\3\2\2\2}\u01bf\3")
        buf.write("\2\2\2\177\u01c1\3\2\2\2\u0081\u01c3\3\2\2\2\u0083\u01c5")
        buf.write("\3\2\2\2\u0085\u01c7\3\2\2\2\u0087\u01c9\3\2\2\2\u0089")
        buf.write("\u01cb\3\2\2\2\u008b\u01cd\3\2\2\2\u008d\u01cf\3\2\2\2")
        buf.write("\u008f\u01d1\3\2\2\2\u0091\u01d4\3\2\2\2\u0093\u01d6\3")
        buf.write("\2\2\2\u0095\u01d8\3\2\2\2\u0097\u01da\3\2\2\2\u0099\u01dc")
        buf.write("\3\2\2\2\u009b\u01ed\3\2\2\2\u009d\u01f0\3\2\2\2\u009f")
        buf.write("\u01f7\3\2\2\2\u00a1\u01fd\3\2\2\2\u00a3\u0200\3\2\2\2")
        buf.write("\u00a5\u0204\3\2\2\2\u00a7\u0206\3\2\2\2\u00a9\u020b\3")
        buf.write("\2\2\2\u00ab\u020f\3\2\2\2\u00ad\u0211\3\2\2\2\u00af\u021f")
        buf.write("\3\2\2\2\u00b1\u0226\3\2\2\2\u00b3\u022a\3\2\2\2\u00b5")
        buf.write("\u022d\3\2\2\2\u00b7\u0238\3\2\2\2\u00b9\u024c\3\2\2\2")
        buf.write("\u00bb\u0250\3\2\2\2\u00bd\u0262\3\2\2\2\u00bf\u0264\3")
        buf.write("\2\2\2\u00c1\u026f\3\2\2\2\u00c3\u00c4\7Q\2\2\u00c4\u00c5")
        buf.write("\7R\2\2\u00c5\u00c6\7G\2\2\u00c6\u00c7\7P\2\2\u00c7\u00c8")
        buf.write("\7S\2\2\u00c8\u00c9\7C\2\2\u00c9\u00ca\7U\2\2\u00ca\u00cb")
        buf.write("\7O\2\2\u00cb\4\3\2\2\2\u00cc\u00cd\7k\2\2\u00cd\u00ce")
        buf.write("\7p\2\2\u00ce\u00cf\7e\2\2\u00cf\u00d0\7n\2\2\u00d0\u00d1")
        buf.write("\7w\2\2\u00d1\u00d2\7f\2\2\u00d2\u00d3\7g\2\2\u00d3\6")
        buf.write("\3\2\2\2\u00d4\u00d5\7s\2\2\u00d5\u00d6\7t\2\2\u00d6\u00d7")
        buf.write("\7g\2\2\u00d7\u00d8\7i\2\2\u00d8\b\3\2\2\2\u00d9\u00da")
        buf.write("\7s\2\2\u00da\u00db\7w\2\2\u00db\u00dc\7d\2\2\u00dc\u00dd")
        buf.write("\7k\2\2\u00dd\u00de\7v\2\2\u00de\n\3\2\2\2\u00df\u00e0")
        buf.write("\7d\2\2\u00e0\u00e1\7k\2\2\u00e1\u00e2\7v\2\2\u00e2\f")
        buf.write("\3\2\2\2\u00e3\u00e4\7e\2\2\u00e4\u00e5\7t\2\2\u00e5\u00e6")
        buf.write("\7g\2\2\u00e6\u00e7\7i\2\2\u00e7\16\3\2\2\2\u00e8\u00e9")
        buf.write("\7k\2\2\u00e9\u00ea\7p\2\2\u00ea\u00eb\7v\2\2\u00eb\20")
        buf.write("\3\2\2\2\u00ec\u00ed\7w\2\2\u00ed\u00ee\7k\2\2\u00ee\u00ef")
        buf.write("\7p\2\2\u00ef\u00f0\7v\2\2\u00f0\22\3\2\2\2\u00f1\u00f2")
        buf.write("\7h\2\2\u00f2\u00f3\7n\2\2\u00f3\u00f4\7q\2\2\u00f4\u00f5")
        buf.write("\7c\2\2\u00f5\u00f6\7v\2\2\u00f6\24\3\2\2\2\u00f7\u00f8")
        buf.write("\7c\2\2\u00f8\u00f9\7p\2\2\u00f9\u00fa\7i\2\2\u00fa\u00fb")
        buf.write("\7n\2\2\u00fb\u00fc\7g\2\2\u00fc\26\3\2\2\2\u00fd\u00fe")
        buf.write("\7h\2\2\u00fe\u00ff\7k\2\2\u00ff\u0100\7z\2\2\u0100\u0101")
        buf.write("\7g\2\2\u0101\u0102\7f\2\2\u0102\30\3\2\2\2\u0103\u0104")
        buf.write("\7d\2\2\u0104\u0105\7q\2\2\u0105\u0106\7q\2\2\u0106\u0107")
        buf.write("\7n\2\2\u0107\32\3\2\2\2\u0108\u0109\7e\2\2\u0109\u010a")
        buf.write("\7q\2\2\u010a\u010b\7p\2\2\u010b\u010c\7u\2\2\u010c\u010d")
        buf.write("\7v\2\2\u010d\34\3\2\2\2\u010e\u010f\7~\2\2\u010f\u0110")
        buf.write("\7~\2\2\u0110\36\3\2\2\2\u0111\u0112\7i\2\2\u0112\u0113")
        buf.write("\7c\2\2\u0113\u0114\7v\2\2\u0114\u0115\7g\2\2\u0115 \3")
        buf.write("\2\2\2\u0116\u0117\7W\2\2\u0117\"\3\2\2\2\u0118\u0119")
        buf.write("\7E\2\2\u0119\u011a\7Z\2\2\u011a$\3\2\2\2\u011b\u011c")
        buf.write("\7o\2\2\u011c\u011d\7g\2\2\u011d\u011e\7c\2\2\u011e\u011f")
        buf.write("\7u\2\2\u011f\u0120\7w\2\2\u0120\u0121\7t\2\2\u0121\u0122")
        buf.write("\7g\2\2\u0122&\3\2\2\2\u0123\u0124\7d\2\2\u0124\u0125")
        buf.write("\7c\2\2\u0125\u0126\7t\2\2\u0126\u0127\7t\2\2\u0127\u0128")
        buf.write("\7k\2\2\u0128\u0129\7g\2\2\u0129\u012a\7t\2\2\u012a(\3")
        buf.write("\2\2\2\u012b\u012c\7\u0080\2\2\u012c*\3\2\2\2\u012d\u012e")
        buf.write("\7#\2\2\u012e,\3\2\2\2\u012f\u0130\7@\2\2\u0130.\3\2\2")
        buf.write("\2\u0131\u0132\7>\2\2\u0132\60\3\2\2\2\u0133\u0134\7@")
        buf.write("\2\2\u0134\u0135\7?\2\2\u0135\62\3\2\2\2\u0136\u0137\7")
        buf.write(">\2\2\u0137\u0138\7?\2\2\u0138\64\3\2\2\2\u0139\u013a")
        buf.write("\7?\2\2\u013a\u013b\7?\2\2\u013b\66\3\2\2\2\u013c\u013d")
        buf.write("\7#\2\2\u013d\u013e\7?\2\2\u013e8\3\2\2\2\u013f\u0140")
        buf.write("\7(\2\2\u0140\u0141\7(\2\2\u0141:\3\2\2\2\u0142\u0143")
        buf.write("\7~\2\2\u0143<\3\2\2\2\u0144\u0145\7`\2\2\u0145>\3\2\2")
        buf.write("\2\u0146\u0147\7(\2\2\u0147@\3\2\2\2\u0148\u0149\7>\2")
        buf.write("\2\u0149\u014a\7>\2\2\u014aB\3\2\2\2\u014b\u014c\7@\2")
        buf.write("\2\u014c\u014d\7@\2\2\u014dD\3\2\2\2\u014e\u014f\7v\2")
        buf.write("\2\u014f\u0150\7t\2\2\u0150\u0151\7w\2\2\u0151\u0152\7")
        buf.write("g\2\2\u0152F\3\2\2\2\u0153\u0154\7h\2\2\u0154\u0155\7")
        buf.write("c\2\2\u0155\u0156\7n\2\2\u0156\u0157\7u\2\2\u0157\u0158")
        buf.write("\7g\2\2\u0158H\3\2\2\2\u0159\u015a\7-\2\2\u015a\u015b")
        buf.write("\7-\2\2\u015bJ\3\2\2\2\u015c\u015d\7/\2\2\u015d\u015e")
        buf.write("\7/\2\2\u015eL\3\2\2\2\u015f\u0160\7u\2\2\u0160\u0161")
        buf.write("\7k\2\2\u0161\u0162\7p\2\2\u0162N\3\2\2\2\u0163\u0164")
        buf.write("\7e\2\2\u0164\u0165\7q\2\2\u0165\u0166\7u\2\2\u0166P\3")
        buf.write("\2\2\2\u0167\u0168\7v\2\2\u0168\u0169\7c\2\2\u0169\u016a")
        buf.write("\7p\2\2\u016aR\3\2\2\2\u016b\u016c\7g\2\2\u016c\u016d")
        buf.write("\7z\2\2\u016d\u016e\7r\2\2\u016eT\3\2\2\2\u016f\u0170")
        buf.write("\7n\2\2\u0170\u0171\7p\2\2\u0171V\3\2\2\2\u0172\u0173")
        buf.write("\7u\2\2\u0173\u0174\7s\2\2\u0174\u0175\7t\2\2\u0175\u0176")
        buf.write("\7v\2\2\u0176X\3\2\2\2\u0177\u0178\7t\2\2\u0178\u0179")
        buf.write("\7q\2\2\u0179\u017a\7v\2\2\u017a\u017b\7n\2\2\u017bZ\3")
        buf.write("\2\2\2\u017c\u017d\7t\2\2\u017d\u017e\7q\2\2\u017e\u017f")
        buf.write("\7v\2\2\u017f\u0180\7t\2\2\u0180\\\3\2\2\2\u0181\u0182")
        buf.write("\7r\2\2\u0182\u0183\7q\2\2\u0183\u0184\7r\2\2\u0184\u0185")
        buf.write("\7e\2\2\u0185\u0186\7q\2\2\u0186\u0187\7w\2\2\u0187\u0188")
        buf.write("\7p\2\2\u0188\u0189\7v\2\2\u0189^\3\2\2\2\u018a\u018b")
        buf.write("\7n\2\2\u018b\u018c\7g\2\2\u018c\u018d\7p\2\2\u018d\u018e")
        buf.write("\7i\2\2\u018e\u018f\7v\2\2\u018f\u0190\7j\2\2\u0190\u0191")
        buf.write("\7q\2\2\u0191\u0192\7h\2\2\u0192`\3\2\2\2\u0193\u0194")
        buf.write("\7-\2\2\u0194\u0195\7?\2\2\u0195b\3\2\2\2\u0196\u0197")
        buf.write("\7/\2\2\u0197\u0198\7?\2\2\u0198d\3\2\2\2\u0199\u019a")
        buf.write("\7,\2\2\u019a\u019b\7?\2\2\u019bf\3\2\2\2\u019c\u019d")
        buf.write("\7\61\2\2\u019d\u019e\7?\2\2\u019eh\3\2\2\2\u019f\u01a0")
        buf.write("\7(\2\2\u01a0\u01a1\7?\2\2\u01a1j\3\2\2\2\u01a2\u01a3")
        buf.write("\7~\2\2\u01a3\u01a4\7?\2\2\u01a4l\3\2\2\2\u01a5\u01a6")
        buf.write("\7\u0080\2\2\u01a6\u01a7\7?\2\2\u01a7n\3\2\2\2\u01a8\u01a9")
        buf.write("\7`\2\2\u01a9\u01aa\7?\2\2\u01aap\3\2\2\2\u01ab\u01ac")
        buf.write("\7>\2\2\u01ac\u01ad\7>\2\2\u01ad\u01ae\7?\2\2\u01aer\3")
        buf.write("\2\2\2\u01af\u01b0\7@\2\2\u01b0\u01b1\7@\2\2\u01b1\u01b2")
        buf.write("\7?\2\2\u01b2t\3\2\2\2\u01b3\u01b4\7k\2\2\u01b4\u01b5")
        buf.write("\7h\2\2\u01b5v\3\2\2\2\u01b6\u01b7\7g\2\2\u01b7\u01b8")
        buf.write("\7n\2\2\u01b8\u01b9\7u\2\2\u01b9\u01ba\7g\2\2\u01bax\3")
        buf.write("\2\2\2\u01bb\u01bc\7]\2\2\u01bcz\3\2\2\2\u01bd\u01be\7")
        buf.write("_\2\2\u01be|\3\2\2\2\u01bf\u01c0\7}\2\2\u01c0~\3\2\2\2")
        buf.write("\u01c1\u01c2\7\177\2\2\u01c2\u0080\3\2\2\2\u01c3\u01c4")
        buf.write("\7*\2\2\u01c4\u0082\3\2\2\2\u01c5\u01c6\7+\2\2\u01c6\u0084")
        buf.write("\3\2\2\2\u01c7\u01c8\7<\2\2\u01c8\u0086\3\2\2\2\u01c9")
        buf.write("\u01ca\7=\2\2\u01ca\u0088\3\2\2\2\u01cb\u01cc\7\60\2\2")
        buf.write("\u01cc\u008a\3\2\2\2\u01cd\u01ce\7.\2\2\u01ce\u008c\3")
        buf.write("\2\2\2\u01cf\u01d0\7?\2\2\u01d0\u008e\3\2\2\2\u01d1\u01d2")
        buf.write("\7/\2\2\u01d2\u01d3\7@\2\2\u01d3\u0090\3\2\2\2\u01d4\u01d5")
        buf.write("\7-\2\2\u01d5\u0092\3\2\2\2\u01d6\u01d7\7/\2\2\u01d7\u0094")
        buf.write("\3\2\2\2\u01d8\u01d9\7,\2\2\u01d9\u0096\3\2\2\2\u01da")
        buf.write("\u01db\7\61\2\2\u01db\u0098\3\2\2\2\u01dc\u01dd\7\'\2")
        buf.write("\2\u01dd\u009a\3\2\2\2\u01de\u01df\7r\2\2\u01df\u01ee")
        buf.write("\7k\2\2\u01e0\u01ee\7\u87fc\2\2\u01e1\u01e2\7v\2\2\u01e2")
        buf.write("\u01e3\7c\2\2\u01e3\u01ee\7w\2\2\u01e4\u01e5\7\u9980\2")
        buf.write("\2\u01e5\u01ee\7\u6e4b\2\2\u01e6\u01e7\7g\2\2\u01e7\u01e8")
        buf.write("\7w\2\2\u01e8\u01e9\7n\2\2\u01e9\u01ea\7g\2\2\u01ea\u01ee")
        buf.write("\7t\2\2\u01eb\u01ec\7\u922b\2\2\u01ec\u01ee\7\uffff\2")
        buf.write("\2\u01ed\u01de\3\2\2\2\u01ed\u01e0\3\2\2\2\u01ed\u01e1")
        buf.write("\3\2\2\2\u01ed\u01e4\3\2\2\2\u01ed\u01e6\3\2\2\2\u01ed")
        buf.write("\u01eb\3\2\2\2\u01ee\u009c\3\2\2\2\u01ef\u01f1\t\2\2\2")
        buf.write("\u01f0\u01ef\3\2\2\2\u01f1\u01f2\3\2\2\2\u01f2\u01f0\3")
        buf.write("\2\2\2\u01f2\u01f3\3\2\2\2\u01f3\u01f4\3\2\2\2\u01f4\u01f5")
        buf.write("\bO\2\2\u01f5\u009e\3\2\2\2\u01f6\u01f8\t\3\2\2\u01f7")
        buf.write("\u01f6\3\2\2\2\u01f8\u01f9\3\2\2\2\u01f9\u01f7\3\2\2\2")
        buf.write("\u01f9\u01fa\3\2\2\2\u01fa\u01fb\3\2\2\2\u01fb\u01fc\b")
        buf.write("P\2\2\u01fc\u00a0\3\2\2\2\u01fd\u01fe\t\4\2\2\u01fe\u00a2")
        buf.write("\3\2\2\2\u01ff\u0201\5\u00a1Q\2\u0200\u01ff\3\2\2\2\u0201")
        buf.write("\u0202\3\2\2\2\u0202\u0200\3\2\2\2\u0202\u0203\3\2\2\2")
        buf.write("\u0203\u00a4\3\2\2\2\u0204\u0205\t\n\2\2\u0205\u00a6\3")
        buf.write("\2\2\2\u0206\u0207\t\5\2\2\u0207\u00a8\3\2\2\2\u0208\u020c")
        buf.write("\t\6\2\2\u0209\u020c\5\u00a5S\2\u020a\u020c\5\u00a7T\2")
        buf.write("\u020b\u0208\3\2\2\2\u020b\u0209\3\2\2\2\u020b\u020a\3")
        buf.write("\2\2\2\u020c\u00aa\3\2\2\2\u020d\u0210\5\u00a9U\2\u020e")
        buf.write("\u0210\5\u00a3R\2\u020f\u020d\3\2\2\2\u020f\u020e\3\2")
        buf.write("\2\2\u0210\u00ac\3\2\2\2\u0211\u0212\7u\2\2\u0212\u0213")
        buf.write("\7v\2\2\u0213\u0214\7t\2\2\u0214\u0215\7g\2\2\u0215\u0216")
        buf.write("\7v\2\2\u0216\u0217\7e\2\2\u0217\u0218\7j\2\2\u0218\u021c")
        buf.write("\3\2\2\2\u0219\u021b\5\u00a1Q\2\u021a\u0219\3\2\2\2\u021b")
        buf.write("\u021e\3\2\2\2\u021c\u021a\3\2\2\2\u021c\u021d\3\2\2\2")
        buf.write("\u021d\u00ae\3\2\2\2\u021e\u021c\3\2\2\2\u021f\u0223\5")
        buf.write("\u00a9U\2\u0220\u0222\5\u00abV\2\u0221\u0220\3\2\2\2\u0222")
        buf.write("\u0225\3\2\2\2\u0223\u0221\3\2\2\2\u0223\u0224\3\2\2\2")
        buf.write("\u0224\u00b0\3\2\2\2\u0225\u0223\3\2\2\2\u0226\u0227\t")
        buf.write("\7\2\2\u0227\u00b2\3\2\2\2\u0228\u022b\5\u0091I\2\u0229")
        buf.write("\u022b\5\u0093J\2\u022a\u0228\3\2\2\2\u022a\u0229\3\2")
        buf.write("\2\2\u022b\u00b4\3\2\2\2\u022c\u022e\5\u00a1Q\2\u022d")
        buf.write("\u022c\3\2\2\2\u022e\u022f\3\2\2\2\u022f\u022d\3\2\2\2")
        buf.write("\u022f\u0230\3\2\2\2\u0230\u0231\3\2\2\2\u0231\u0235\5")
        buf.write("\u0089E\2\u0232\u0234\5\u00a1Q\2\u0233\u0232\3\2\2\2\u0234")
        buf.write("\u0237\3\2\2\2\u0235\u0233\3\2\2\2\u0235\u0236\3\2\2\2")
        buf.write("\u0236\u00b6\3\2\2\2\u0237\u0235\3\2\2\2\u0238\u023f\5")
        buf.write("\u00b5[\2\u0239\u023b\5\u00b1Y\2\u023a\u023c\5\u00b3Z")
        buf.write("\2\u023b\u023a\3\2\2\2\u023b\u023c\3\2\2\2\u023c\u023d")
        buf.write("\3\2\2\2\u023d\u023e\5\u00a3R\2\u023e\u0240\3\2\2\2\u023f")
        buf.write("\u0239\3\2\2\2\u023f\u0240\3\2\2\2\u0240\u00b8\3\2\2\2")
        buf.write("\u0241\u0242\7f\2\2\u0242\u024d\7v\2\2\u0243\u0244\7p")
        buf.write("\2\2\u0244\u024d\7u\2\2\u0245\u0246\7w\2\2\u0246\u024d")
        buf.write("\7u\2\2\u0247\u0248\7\u788e\2\2\u0248\u024d\7u\2\2\u0249")
        buf.write("\u024a\7o\2\2\u024a\u024d\7u\2\2\u024b\u024d\7u\2\2\u024c")
        buf.write("\u0241\3\2\2\2\u024c\u0243\3\2\2\2\u024c\u0245\3\2\2\2")
        buf.write("\u024c\u0247\3\2\2\2\u024c\u0249\3\2\2\2\u024c\u024b\3")
        buf.write("\2\2\2\u024d\u00ba\3\2\2\2\u024e\u0251\5\u00a3R\2\u024f")
        buf.write("\u0251\5\u00b7\\\2\u0250\u024e\3\2\2\2\u0250\u024f\3\2")
        buf.write("\2\2\u0251\u0252\3\2\2\2\u0252\u0253\5\u00b9]\2\u0253")
        buf.write("\u00bc\3\2\2\2\u0254\u0256\7$\2\2\u0255\u0257\n\b\2\2")
        buf.write("\u0256\u0255\3\2\2\2\u0257\u0258\3\2\2\2\u0258\u0259\3")
        buf.write("\2\2\2\u0258\u0256\3\2\2\2\u0259\u025a\3\2\2\2\u025a\u0263")
        buf.write("\7$\2\2\u025b\u025d\7)\2\2\u025c\u025e\n\t\2\2\u025d\u025c")
        buf.write("\3\2\2\2\u025e\u025f\3\2\2\2\u025f\u0260\3\2\2\2\u025f")
        buf.write("\u025d\3\2\2\2\u0260\u0261\3\2\2\2\u0261\u0263\7)\2\2")
        buf.write("\u0262\u0254\3\2\2\2\u0262\u025b\3\2\2\2\u0263\u00be\3")
        buf.write("\2\2\2\u0264\u0265\7\61\2\2\u0265\u0266\7\61\2\2\u0266")
        buf.write("\u026a\3\2\2\2\u0267\u0269\n\3\2\2\u0268\u0267\3\2\2\2")
        buf.write("\u0269\u026c\3\2\2\2\u026a\u0268\3\2\2\2\u026a\u026b\3")
        buf.write("\2\2\2\u026b\u026d\3\2\2\2\u026c\u026a\3\2\2\2\u026d\u026e")
        buf.write("\b`\2\2\u026e\u00c0\3\2\2\2\u026f\u0270\7\61\2\2\u0270")
        buf.write("\u0271\7,\2\2\u0271\u0275\3\2\2\2\u0272\u0274\13\2\2\2")
        buf.write("\u0273\u0272\3\2\2\2\u0274\u0277\3\2\2\2\u0275\u0276\3")
        buf.write("\2\2\2\u0275\u0273\3\2\2\2\u0276\u0278\3\2\2\2\u0277\u0275")
        buf.write("\3\2\2\2\u0278\u0279\7,\2\2\u0279\u027a\7\61\2\2\u027a")
        buf.write("\u027b\3\2\2\2\u027b\u027c\ba\2\2\u027c\u00c2\3\2\2\2")
        buf.write("\27\2\u01ed\u01f2\u01f9\u0202\u020b\u020f\u021c\u0223")
        buf.write("\u022a\u022f\u0235\u023b\u023f\u024c\u0250\u0258\u025f")
        buf.write("\u0262\u026a\u0275\3\b\2\2")
        return buf.getvalue()


class Qasm2Lexer(Lexer):
    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    T__53 = 54
    T__54 = 55
    T__55 = 56
    T__56 = 57
    T__57 = 58
    T__58 = 59
    LBRACKET = 60
    RBRACKET = 61
    LBRACE = 62
    RBRACE = 63
    LPAREN = 64
    RPAREN = 65
    COLON = 66
    SEMICOLON = 67
    DOT = 68
    COMMA = 69
    EQUALS = 70
    ARROW = 71
    PLUS = 72
    MINUS = 73
    MUL = 74
    DIV = 75
    MOD = 76
    Constant = 77
    Whitespace = 78
    Newline = 79
    Integer = 80
    StretchN = 81
    Identifier = 82
    RealNumber = 83
    TimingLiteral = 84
    StringLiteral = 85
    LineComment = 86
    BlockComment = 87

    channelNames = [u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN"]

    modeNames = ["DEFAULT_MODE"]

    literalNames = ["<INVALID>",
                    "'OPENQASM'", "'include'", "'qreg'", "'qubit'", "'bit'", "'creg'",
                    "'int'", "'uint'", "'float'", "'angle'", "'fixed'", "'bool'",
                    "'const'", "'||'", "'gate'", "'U'", "'CX'", "'measure'", "'barrier'",
                    "'~'", "'!'", "'>'", "'<'", "'>='", "'<='", "'=='", "'!='",
                    "'&&'", "'|'", "'^'", "'&'", "'<<'", "'>>'", "'true'", "'false'",
                    "'++'", "'--'", "'sin'", "'cos'", "'tan'", "'exp'", "'ln'",
                    "'sqrt'", "'rotl'", "'rotr'", "'popcount'", "'lengthof'", "'+='",
                    "'-='", "'*='", "'/='", "'&='", "'|='", "'~='", "'^='", "'<<='",
                    "'>>='", "'if'", "'else'", "'['", "']'", "'{'", "'}'", "'('",
                    "')'", "':'", "';'", "'.'", "','", "'='", "'->'", "'+'", "'-'",
                    "'*'", "'/'", "'%'"]

    symbolicNames = ["<INVALID>",
                     "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "LPAREN", "RPAREN",
                     "COLON", "SEMICOLON", "DOT", "COMMA", "EQUALS", "ARROW", "PLUS",
                     "MINUS", "MUL", "DIV", "MOD", "Constant", "Whitespace", "Newline",
                     "Integer", "StretchN", "Identifier", "RealNumber", "TimingLiteral",
                     "StringLiteral", "LineComment", "BlockComment"]

    ruleNames = ["T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6",
                 "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13",
                 "T__14", "T__15", "T__16", "T__17", "T__18", "T__19",
                 "T__20", "T__21", "T__22", "T__23", "T__24", "T__25",
                 "T__26", "T__27", "T__28", "T__29", "T__30", "T__31",
                 "T__32", "T__33", "T__34", "T__35", "T__36", "T__37",
                 "T__38", "T__39", "T__40", "T__41", "T__42", "T__43",
                 "T__44", "T__45", "T__46", "T__47", "T__48", "T__49",
                 "T__50", "T__51", "T__52", "T__53", "T__54", "T__55",
                 "T__56", "T__57", "T__58", "LBRACKET", "RBRACKET", "LBRACE",
                 "RBRACE", "LPAREN", "RPAREN", "COLON", "SEMICOLON", "DOT",
                 "COMMA", "EQUALS", "ARROW", "PLUS", "MINUS", "MUL", "DIV",
                 "MOD", "Constant", "Whitespace", "Newline", "Digit", "Integer",
                 "ValidUnicode", "Letter", "FirstIdCharacter", "GeneralIdCharacter",
                 "StretchN", "Identifier", "SciNotation", "PlusMinus",
                 "Float", "RealNumber", "TimeUnit", "TimingLiteral", "StringLiteral",
                 "LineComment", "BlockComment"]

    grammarFileName = "Qasm2.g4"

    def __init__(self, input=None, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
