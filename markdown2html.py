#!/usr/bin/python3
import sys

linestosave = []
flag = ''
selectores = [
    "#",
    "##",
    "###",
    "####",
    "#####",
    "######",
    "-",
    "*"
]


def boldemphasis(text):
    bold = '**'
    emphasis = '__'
    if bold in text and text.count(bold) % 2 == 0:
        index = 1
        while(bold in text):
            if index % 2 == 0:
                text = text.replace(bold, '</b>', 1)
            else:
                text = text.replace(bold, '<b>', 1)
            index = index + 1
    if emphasis in text and text.count(emphasis) % 2 == 0:
        index = 1
        while(emphasis in text):
            if index % 2 == 0:
                text = text.replace(emphasis, '</em>', 1)
            else:
                text = text.replace(emphasis, '<em>', 1)
            index = index + 1
    return text


def saveLine(list, destinyfile):
    with open(destinyfile, 'a') as f:
        for line in list:
            f.write(line)


def heading(text):
    flag = 'heading'
    typeHeader = str(text[0].count('#'))
    opentag = '<h' + typeHeader + '>'
    closetag = '</h' + typeHeader + '>'
    linewhitboldoremphasis = boldemphasis(text[1])
    linetosave = opentag + \
        linewhitboldoremphasis.replace('\n', '') + closetag + '\n'
    linestosave.append(linetosave)


def unorderedlisting(text):
    global flag
    actualflag = 'ul'
    opentag = '<ul>\n'
    closetag = '</ul>\n'
    linewhitboldoremphasis = boldemphasis(text[1])
    linetosave = '<li>' + linewhitboldoremphasis.replace('\n', '') + '</li>\n'
    if flag == actualflag:
        linestosave.pop()
        linestosave.append(linetosave)
    else:
        linestosave.append(opentag)
        linestosave.append(linetosave)
    linestosave.append(closetag)

    flag = 'ul'


def orderedlisting(text):
    global flag
    actualflag = 'ol'
    opentag = '<ol>\n'
    closetag = '</ol>\n'
    linewhitboldoremphasis = boldemphasis(text[1])
    linetosave = '<li>' + linewhitboldoremphasis.replace('\n', '') + '</li>\n'
    if flag == actualflag:
        linestosave.pop()
        linestosave.append(linetosave)
    else:
        linestosave.append(opentag)
        linestosave.append(linetosave)
    linestosave.append(closetag)

    flag = 'ol'


def simpletex(text):
    global flag
    actualflag = 'text'
    opentag = '<p>\n'
    closetag = '</p>\n'
    linewhitboldoremphasis = boldemphasis(text)
    linetosave = linewhitboldoremphasis.replace('\n', '') + '\n'
    if flag == actualflag:
        linestosave.pop()
        linestosave.append('<br/>\n')
        linestosave.append(linetosave)
    else:
        linestosave.append(opentag)
        linestosave.append(linetosave)
    linestosave.append(closetag)
    flag = 'text'


myfunctions = {
    "#": heading,
    "-": unorderedlisting,
    "*": orderedlisting
}


def operation(name, listline):
    myfunctions[name](listline)


if __name__ == "__main__":
    print('hola')

    arguments = sys.argv

    print(arguments)
    print(len(arguments))

    if len(arguments) < 3:
        sys.stderr.write('Usage: ./markdown2html.py README.md README.html\n')
        sys.exit(1)

    try:
        fileToRead = arguments[1]
        print(fileToRead)
        with open(fileToRead, 'r') as f:
            lista = list(f)
            print(lista)
            for line in lista:
                splitline = line.split(' ', 1)
                if splitline[0] == '\n':
                    flag = 'lineblank'
                if splitline[0] in selectores:
                    operation(splitline[0][0], splitline)
                else:
                    if splitline[0][0] is not '\n':
                        simpletex(line)
        saveLine(linestosave, arguments[2])
        flag = ''
        sys.exit(0)
    except OSError:
        sys.stderr.write('Missing <filename>\n')
        sys.exit(1)
