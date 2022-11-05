import time
from pyipcore import *
from PIL import Image, ImageDraw, ImageFont

_vp = None
def CreateVerilogParser():
    global _vp
    _vp = VerilogParser()

def GetVerilogParser():
    if _vp is None:
        CreateVerilogParser()
    return _vp

class IPCoreGraphic:
    def __init__(self, ast) -> None:
        self.ast = ast
        self.fnt_S = ImageFont.truetype(font_path, 10)
        self.fnt_M = ImageFont.truetype(font_path, 20)
        self.fnt_L = ImageFont.truetype(font_path, 30)
        self.fnt_XL = ImageFont.truetype(font_path, 40)
        self.ipcparse = IPCoreParse(ast)

    def reset(self):
        self.wss = None
        self.hss = None

    def getStringWidth(self, string, fnt_size):
        return int(len(string) * fnt_size / 40 * 30) + 1

    def buildInfo(self):
        data = {}
        ws, lws, rws = [0], [0], [0]
        data['name'] = self.ipcparse.module_name
        ws += [self.getStringWidth(data['name'], 30)]

        data["params"] = []
        for k, v in self.ipcparse.getParams().items():
            data["params"] += [f"# {k} = {v}"]
            ws += [self.getStringWidth(data["params"][-1], 20)]
        
        data["leftports"] = []
        data["rightports"] = []
        for k, v in self.ipcparse.getPorts().items():
            temp = self.getStringWidth(str(v), 20)
            if v.type_name == "input":
                lws += [temp]
                data["leftports"] += [f"{v}"]
            else:
                rws += [temp]
                data["rightports"] += [f"{v}"]

        ws = max(ws)
        lws = max(lws)
        rws = max(rws)
        self.wss = [lws, ws, rws]

        hs = max(30, 2 * 30 * len(data["leftports"]), 2 * 30 * len(data["rightports"]))
        ths = 20 * (len(data["params"]) + 1)
        self.hss = [ths, hs, 10]
        return data

    def draw(self):
        base_width = 1
        bold_width = 5

        def draw_txt(pos, txt, fnt):
            draw.text(pos, txt, fill="black", anchor="mm", font=fnt)
        def draw_arrow(pos, length, direct="left", width=base_width):
            delta = int(length * 0.717)
            if direct == "left":
                draw.line((pos[0], pos[1], pos[0] + delta, pos[1] - delta), fill="black", width=width)
                draw.line((pos[0], pos[1], pos[0] + delta, pos[1] + delta), fill="black", width=width)
            elif direct == "right":
                draw.line((pos[0], pos[1], pos[0] - delta, pos[1] - delta), fill="black", width=width)
                draw.line((pos[0], pos[1], pos[0] - delta, pos[1] + delta), fill="black", width=width)
        
        data = self.buildInfo()
        width = sum(self.wss)
        height = sum(self.hss)
        wss = self.wss
        hss = self.hss

        # print(self.wss, self.hss)
        img = Image.new(mode='RGBA', size=(width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        draw.rectangle(
            [self.wss[0], self.hss[0], self.wss[0] + self.wss[1] - 1, self.hss[0] + self.hss[1]],
            outline=(0, 0, 0), width=base_width
        )

        # draw module name
        draw_txt((wss[0] + int(0.5 * wss[1]), hss[0] + int(0.5 * hss[1])), data["name"], self.fnt_L)
        
        # draw parameters
        for i, each in enumerate(data["params"]):
            draw_txt((wss[0] + int(0.5 * wss[1]), 20 + 20 * i), each, self.fnt_M)
        
        # draw left ports
        span = hss[1] / (len(data["leftports"]) + 1)
        for i, each in enumerate(data["leftports"]):
            line_width = bold_width if each.find("[") != -1 else base_width
            draw_txt((int(self.getStringWidth(each, 20) / 2), int(hss[0] + span + span * i)), each, self.fnt_M)
            draw_arrow((wss[0], int(hss[0] + 1.5 * span + span * i)), 16, "right", line_width)
            draw.line((0, int(hss[0] + 1.5 * span + span * i), wss[0], int(hss[0] + 1.5 * span + span * i)), "black", width=line_width)

        # draw left ports
        span = hss[1] / (len(data["rightports"]) + 1)
        for i, each in enumerate(data["rightports"]):
            line_width = bold_width if each.find("[") != -1 else base_width
            draw_txt((wss[0] + wss[1] + int(self.getStringWidth(each, 20) / 2), int(hss[0] + span + span * i)), each, self.fnt_M)
            draw_arrow((width, int(hss[0] + 1.5 * span + span * i)), 16, "right", line_width)
            if each.find("inout") != -1:
                draw_arrow((wss[0] + wss[1], int(hss[0] + 1.5 * span + span * i)), 20, "left", line_width)
            draw.line((wss[0] + wss[1], int(hss[0] + 1.5 * span + span * i), width, int(hss[0] + 1.5 * span + span * i)), "black", width=line_width)

        # print(data)
        return img


CreateVerilogParser()

if __name__ == "__main__":
    ...
    # ipcg = IPCoreGraphic(ast)
    # ipcg.draw().show()


