#!/usr/bin/python3
''' esta fucion es para hacer marckdown'''

import sys
import re
import hashlib

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
    ''' bold '''
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
    ''' save in new file '''
    with open(destinyfile, 'w') as f:
        for line in list:
            f.write(line)


def heading(text):
    ''' put h tags '''
    flag = 'heading'
    typeHeader = str(text[0].count('#'))
    opentag = '<h' + typeHeader + '>'
    closetag = '</h' + typeHeader + '>'
    linewhitboldoremphasis = boldemphasis(text[1])
    linewhitboldoremphasis = butwhy(linewhitboldoremphasis)
    linetosave = opentag + \
        linewhitboldoremphasis.replace('\n', '') + closetag + '\n'
    linestosave.append(linetosave)


def unorderedlisting(text):
    ''' put ul tags '''
    global flag
    actualflag = 'ul'
    opentag = '<ul>\n'
    closetag = '</ul>\n'
    linewhitboldoremphasis = boldemphasis(text[1])
    linewhitboldoremphasis = butwhy(linewhitboldoremphasis)
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
    ''' put ol tags '''
    global flag
    actualflag = 'ol'
    opentag = '<ol>\n'
    closetag = '</ol>\n'
    linewhitboldoremphasis = boldemphasis(text[1])
    linewhitboldoremphasis = butwhy(linewhitboldoremphasis)
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
    ''' put bold and emphasis tags '''
    global flag
    actualflag = 'text'
    opentag = '<p>\n'
    closetag = '</p>\n'
    linewhitboldoremphasis = boldemphasis(text)
    linewhitboldoremphasis = butwhy(linewhitboldoremphasis)
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


def butwhy(text):
    ''' made weird things '''
    translations = {}
    coincidencias = re.findall("\[\[.*\]\]|\(\(.*\)\)", text)
    for coincidencia in coincidencias:
        if coincidencia.find('[[') >= 0 or coincidencia.find(']]') >= 0:
            value = coincidencia
            for simbol in ['[[', ']]']:
                value = value.replace(simbol, '')
                translations[coincidencia] = hashlib.md5(
                    value.encode()).hexdigest()
        if coincidencia.find('((') >= 0 or coincidencia.find('))') >= 0:
            value = coincidencia
            for simbol in ['C', 'c', '(', ')']:
                value = value.replace(simbol, '')
                translations[coincidencia] = value
    for translation in translations:
        text = text.replace(translation, translations[translation])
    return (text)


myfunctions = {
    "#": heading,
    "-": unorderedlisting,
    "*": orderedlisting
}


def operation(name, listline):
    myfunctions[name](listline)


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) < 3:
        sys.stderr.write('Usage: ./markdown2html.py README.md README.html\n')
        sys.exit(1)

    try:
        fileToRead = arguments[1]
        with open(fileToRead, 'r') as f:
            lista = list(f)
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
        message = 'Missing ' + arguments[1] + '\n'
        sys.stderr.write(message)
        sys.exit(1)
