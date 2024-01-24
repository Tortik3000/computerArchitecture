import sys

registerRiscFive = {
    0: "zero",
    1: "ra",
    2: "sp",
    3: "gp",
    4: "Tp",
    5: "t0",
    6: "t1",
    7: "t2",
    8: "s0",
    9: "s1",
    10: "a0",
    11: "a1",
    12: "a2",
    13: "a3",
    14: "a4",
    15: "a5",
    16: "a6",
    17: "a7",
    18: "s2",
    19: "s3",
    20: "s4",
    21: "s5",
    22: "s6",
    23: "s7",
    24: "s8",
    25: "s9",
    26: "s10",
    27: "s11",
    28: "t3",
    29: "t4",
    30: "t5",
    31: "t6"
}
commandType = {
    "0110111": "U",
    "0010111": "U",
    "1101111": "J",
    "1100111": "I",
    "1100011": "B",
    "0000011": "I",
    "0100011": "S",
    "0010011": "I",
    "0110011": "R",
    "0001111": "fence",
    "1110011": "I",
}
CommandR = {
    "01100110000000000": "add",
    "01100110000100000": "sub",
    "01100110010000000": "sll",
    "01100110100000000": "slt",
    "01100110110000000": "sltu",
    "01100111000000000": "xor",
    "01100110110000001": "mulhu",
    "01100111000000001": "div",
    "01100111010000001": "divu",
    "01100111100000001": "rem",
    "01100111010000000": "srl",
    "01100111010100000": "sra",
    "01100111100000000": "or",
    "01100111110000000": "and",
    "01100110000000001": "mul",
    "01100110010000001": "mulh",
    "01100110100000001": "mulhsu",
    "01100111110000001": "remu"
}
CommandI = {
    "1100111000": "jalr",
    "0000011000": "lb",
    "0000011001": "lh",
    "0000011010": "lw",
    "0010011010": "slti",
    "0010011011": "sltiu",
    "0010011100": "xori",
    "0010011110": "ori",
    "0010011111": "andi",
    "1110011000": "ecall",
    "0010011001": "slli",
    "0010011101": "srli",
    "0000011100": "lbu",
    "0000011101": "lhu",
    "0010011000": "addi",
}
CommandFence = {
    "0001111": "fence"
}
CommandU = {
    "0110111": "lui",
    "0010111": "auipc"
}
CommandJ = {
    "1101111": "jal"
}
CommandS = {
    "0100011000": "sb",
    "0100011001": "sh",
    "0100011010": "sw"
}
CommandB = {
    "1100011000": "beq",
    "1100011001": "bne",
    "1100011100": "blt",
    "1100011101": "bge",
    "1100011110": "bltu",
    "1100011111": "bgeu",
}

typeSymtab = {
    0: "NOTYPE",
    1: "OBJECT",
    2: "FUNC",
    3: "SECTION",
    4: "FILE",
    5: "COMMON",
    6: "TLS",
    10: "LOOS",
    12: "HIOS",
    13: "LOPROC",
    14: "SPARC_REGISTER",
    15: "HIPROC"
}
bindSymtab = {
    0: "LOCAL",
    1: "GLOBAL",
    2: "WEAK",
    10: "LOOS",
    12: "HIOS",
    13: "LOPROC",
    15: "HIPROC"
}
visSymtab = {
    0: "DEFAULT",
    1: "INTERNAL",
    2: "HIDDEN",
    3: "PROTECTED",
    4: "EXPORTED",
    5: "SINGLETON",
    6: "ELIMINATE"
}
indexSymtab = {
    0: "UNDEF",
    0xff00: "LOPROC",
    0xff1f: "HIPROC",
    0xfff1: "ABS",
    0xfff2: "COMMON",
    0xffff: "HIRESERVE"
}


def dopForTwo(data):
    number = 0
    for i in range(len(data)):
        if (i == 0):
            number -= int(data[i]) * 2 ** (len(data) - 1)
        else:
            number += int(data[i]) * 2 ** (len(data) - 1 - i)
    return number


def commandI(addr, data):
    value = int(data, 2)
    opcode = data[-7:]
    funct3 = data[-15:-12]
    name = CommandI[opcode + funct3]
    if name == "ecall" and int(data[-32: -20], 2) == 1:
        name = "ebreak"
    if name == "slli" or name == "srli":
        imm = int(data[-25:-20], 2)
    else:
        imm = dopForTwo(data[-32:-20])
    if int(data[-32:-25]) != 0 and name == "srli":
        name = "srai"
    rs1 = registerRiscFive[int(data[-20:-15], 2)]
    rd = registerRiscFive[int(data[-12:-7], 2)]



    if name in ["ebreak", "ecall"]:
        return ("   %05x:\t%08x\t%7s\n" %
                (addr, value, name))
    elif name in ["lhu", "lb", "jalr", "lh", "lw", "lbu"]:
        return ("   %05x:\t%08x\t%7s\t%s, %d(%s)\n" %
                (addr, value, name, rd, imm, rs1))
    else:
        return ("   %05x:\t%08x\t%7s\t%s, %s, %s\n" %
                (addr, value, name, rd, rs1, imm))


def commandR(addr, data):
    value = int(data, 2)
    opcode = data[-7:]
    funct3 = data[-15:-12]
    funct7 = data[-32:-25]
    rd = registerRiscFive[int(data[-12:-7], 2)]
    rs1 = registerRiscFive[int(data[-20:-15], 2)]
    rs2 = registerRiscFive[int(data[-25:-20], 2)]
    name = CommandR[opcode + funct3 + funct7]

    return ("   %05x:\t%08x\t%7s\t%s, %s, %s\n" %
            (addr, value, name, rd, rs1, rs2))


def commandU(addr, data):
    value = int(data, 2)
    opcode = data[-7:]
    name = CommandU[opcode]
    imm = dopForTwo(data[-32:-12])

    if(imm < 0):
        imm = 4294967295 + imm +1
    imm = hex(imm)
    rd = registerRiscFive[int(data[-12:-7], 2)]

    return ("   %05x:\t%08x\t%7s\t%s, %s\n" %
            (addr, value, name, rd, imm))


def commandS(addr, data):
    value = int(data, 2)
    opcode = data[-7:]
    funct3 = data[-15:-12]
    rs1 = registerRiscFive[int(data[-20:-15], 2)]
    rs2 = registerRiscFive[int(data[-25:-20], 2)]
    imm = dopForTwo(data[-32:-25] + data[-12:-7])
    name = CommandS[opcode + funct3]

    return ("   %05x:\t%08x\t%7s\t%s, %d(%s)\n" %
            (addr, value, name, rs2, imm, rs1))


def commandB(addr, data, indexMark, countUrl):
    value = int(data, 2)
    opcode = data[-7:]
    funct3 = data[-15: -12]
    rs1 = registerRiscFive[int(data[-20:-15], 2)]
    rs2 = registerRiscFive[int(data[-25:-20], 2)]
    imm = dopForTwo(data[-32] + data[-8] + data[-31:-25] + data[-12:-8] + "0")
    name = CommandB[opcode + funct3]
    addrUrl = imm + addr

    if (addrUrl not in indexMark):
        indexMark[addrUrl] = "L" + str(countUrl)
        countUrl += 1
    nameUrl = indexMark[addrUrl]

    return ("   %05x:\t%08x\t%7s\t%s, %s, 0x%x, <%s>\n" %
            (addr, value, name, rs1, rs2, addrUrl, nameUrl)), countUrl


def commandJ(addr, data, indexMark, countUrl):
    value = int(data, 2)
    opcode = data[-7:]
    rd = registerRiscFive[int(data[-12:-7], 2)]
    name = CommandJ[opcode]
    imm = dopForTwo(data[-32] + data[-20:-12] + data[-21] + data[-31:-21] + "0")
    addrUrl = addr + imm

    if (addrUrl not in indexMark):
        indexMark[addrUrl] = "L" + str(countUrl)
        countUrl += 1
    nameUrl = indexMark[addrUrl]

    return ("   %05x:\t%08x\t%7s\t%s, 0x%x <%s>\n" %
            (addr, value, name, rd, addrUrl, nameUrl)), countUrl


def commandFence(addr, data):
    opcode = data[-7:]
    name = CommandFence[opcode]
    value = int(data, 2)
    pred = data[4:8]
    succ = data[8:12]
    ans1 = ""
    ans2 = ""
    for i in range(4):
        if pred[i] == '1':
            if i == 0:
                ans1 += 'i'
            elif i == 1:
                ans1 += 'o'
            elif i == 2:
                ans1 += 'r'
            elif i == 3:
                ans1 += 'w'
    for i in range(4):
        if succ[i] == '1':
            if i == 0:
                ans2 += 'i'
            elif i == 1:
                ans2 += 'o'
            elif i == 2:
                ans2 += 'r'
            elif i == 3:
                ans2 += 'w'

    return ("   %05x:\t%08x\t%7s\t%s, %s\n" %
            (addr, value, name, ans1, ans2))


def commandUnknown(addr, data):
    value = int(data, 2)
    name = "invalid_instruction"
    return ("   %05x:\t%08x\t%-7s\n" %
            (addr, value, name))

def searchIndexHeader(inputList, nameHeader, indexStartHeader, indexShstrndxData):
    ans = 0
    i = 0
    while ans == 0:
        name = ""
        indexNow = indexShstrndxData + decoderElfData(
            inputList[indexStartHeader + i * 40:indexStartHeader + i * 40 + 4])
        while inputList[indexNow] != 0:
            name += chr(inputList[indexNow])
            indexNow += 1
        if name == nameHeader:
            ans = indexStartHeader + i * 40
        i += 1
    return ans


def decoderElfData(data):
    num = ""
    for i in range(len(data) - 1, -1, -1):
        nowBit = hex(data[i])[2:]
        if (len(nowBit) == 1):
            nowBit = "0" + nowBit
        num += nowBit
    return int(num, 16)


def parser(inputList):
    e_shentsize = 40
    e_shoff = decoderElfData(inputList[32:36])
    e_shnum = decoderElfData(inputList[48:50])
    e_shstrndx = decoderElfData(inputList[50: 52])

    indexShstrndx = e_shstrndx * e_shentsize + e_shoff
    indexShstrndxOffset = indexShstrndx + 16
    indexShstrndxData = decoderElfData(inputList[indexShstrndxOffset: indexShstrndxOffset + 4])

    symtabOut = []
    indexMark = parserSymtab(inputList, e_shoff, indexShstrndxData, symtabOut)

    textOut = []
    parserText(inputList, e_shoff, indexShstrndxData, indexMark, textOut)
    return textOut + symtabOut


def parserSymtab(inputList, e_shoff, indexShstrndxData, symtabOut):
    indexSymtabHeader = searchIndexHeader(inputList, ".symtab", e_shoff, indexShstrndxData)
    indexStrtabHeader = searchIndexHeader(inputList, ".strtab", e_shoff, indexShstrndxData)

    indexDataSymtab = decoderElfData(inputList[indexSymtabHeader + 16: indexSymtabHeader + 20])
    sizeDataSymtab = decoderElfData(inputList[indexSymtabHeader + 20: indexSymtabHeader + 24])
    indexDataStrtab = decoderElfData(inputList[indexStrtabHeader + 16: indexStrtabHeader + 20])

    indexMark = {}
    symtabOut.append("\n.symtab\n")
    symtabOut.append("\nSymbol Value              Size Type     Bind     Vis       Index Name\n")

    for i in range(sizeDataSymtab // 16):
        nowMark = inputList[indexDataSymtab + i * 16: indexDataSymtab + (i + 1) * 16]
        indexName = indexDataStrtab + decoderElfData(nowMark[0:4])
        name = ""
        while inputList[indexName] != 0:
            name += chr(inputList[indexName])
            indexName += 1

        if (decoderElfData(nowMark[14:16]) in indexSymtab):
            index = indexSymtab[decoderElfData(nowMark[14:16])]
        else:
            index = decoderElfData(nowMark[14:16])
        symtabOut.append("[%4i] 0x%-15X %5i %-8s %-8s %-8s %6s %s\n" % (
            i, decoderElfData(nowMark[4:8]), decoderElfData(nowMark[8:12]),
            typeSymtab[decoderElfData(nowMark[12: 13]) & 15],
            bindSymtab[decoderElfData(nowMark[12: 13]) >> 4], visSymtab[decoderElfData(nowMark[13:14]) & 3], index,
            name))
        if (typeSymtab[decoderElfData(nowMark[12: 13]) & 15] == "FUNC"):
            indexMark[decoderElfData(nowMark[4:8])] = name
    return indexMark


def parserText(inputList, e_shoff, indexShstrndxData, indexMark, textOut):
    textOut.append(".text\n")
    indexTextHeader = searchIndexHeader(inputList, ".text", e_shoff, indexShstrndxData)
    virtualAddr = decoderElfData(inputList[indexTextHeader + 12: indexTextHeader + 16])
    indexData = decoderElfData(inputList[indexTextHeader + 16: indexTextHeader + 20])
    sizeData = decoderElfData(inputList[indexTextHeader + 20: indexTextHeader + 24])
    countUrl = 0
    commands = []
    for i in range(sizeData // 4):
        command = decoderElfData(inputList[indexData + i * 4: indexData + (i + 1) * 4])
        command = (32 - len(bin(command)[2:])) * "0" + bin(command)[2:]
        opcode = command[-7:]
        typeCom = commandType[opcode]

        addr = virtualAddr + i * 4

        if typeCom == "I":
            commands.append(commandI(addr, command))
        elif typeCom == "R":
            commands.append(commandR(addr, command))
        elif typeCom == "S":
            commands.append(commandS(addr, command))
        elif typeCom == "U":
            commands.append(commandU(addr, command))
        elif typeCom == "B":
            text, countUrl = commandB(addr, command, indexMark, countUrl)
            commands.append(text)
        elif typeCom == "J":
            text, countUrl = commandJ(addr, command, indexMark, countUrl)
            commands.append(text)
        elif typeCom == "fence":
            commands.append(commandFence(addr, command))
        else:
            commands.append(commandUnknown(addr, command))

    for i in range(sizeData // 4):
        if virtualAddr + i * 4 in indexMark:
            textOut.append("\n%08x \t<%s>:\n" % (
                virtualAddr + i * 4, indexMark[virtualAddr + i * 4]))
        textOut.append(commands[i])
    textOut.append("\n")


if(len(sys.argv) == 3):
    try:
        with open(sys.argv[1], 'rb') as inputFile:
            inputList = []
            lines = inputFile.readlines()
            for line in lines:
                inputList += list(line)

    except FileNotFoundError:
        print(f"FileNotFound: {sys.argv[1]}", file=sys.stderr)


    if(chr(inputList[0]) + chr(inputList[1]) + chr(inputList[2]) + chr(inputList[3])  == '\x7fELF'):
        Out = parser(inputList)

        with open(sys.argv[2], 'w') as outputFile:
            for line in Out:
                outputFile.write(line)
    else:
        print("Expect ELF file", file=sys.stderr)

else:
    print(f"Expect 2 argument, actual: {len(sys.argv) - 1}", file=sys.stderr)

