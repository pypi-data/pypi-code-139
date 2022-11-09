from .animals import COW

INDENT_DEFAULT = 4
MAXWIDTH_DEFAULT = 100

def genquotebubble(lines):
    lineslen = len(lines)
    if (lineslen < 1):
        raise ValueError("Length of lines must be at least 1.")
    maxwidth = max([len(s) for s in lines])
    linespadded = [str.center(s, maxwidth) for s in lines]
    out = [" "+("-"*(maxwidth+2))]
    if lineslen == 1:
        out.append("< " + lines[0] + " >")
    else:
        for i in range(0, lineslen):
            outline = ""
            if i == 0:
                outline = "/ " + linespadded[i] + " \\"
            elif i == lineslen-1:
                outline = "\\ " + linespadded[i] + " /"
            else:
                outline = "| " + linespadded[i] + " |"
            out.append(outline)
    out.append(" "+("-"*(maxwidth+2)))
    return out

def animalsay(lines, animal=COW, indent=INDENT_DEFAULT):
    if lines == []:
        lines = [animal.sound]
    out = genquotebubble(lines)
    out.append((" "*(indent))+"\\")
    out.append((" "*(indent))+" \\")
    out.extend([((" "*(indent+2))+line) for line in animal.body])
    return "\n".join(out)
