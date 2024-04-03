# MEM_SIZE = 2 ** 16 # 2 ** ADDR_LEN
# ADDR_LEN = 16
# CACHE_WAY = 4
# CACHE_TAG_LEN = 6  # addr - index - offset
# CACHE_IDX_LEN = 5 # log(CACHE_SETS_COUNT)
# CACHE_OFFSET_LEN = 5 # log(CACHE_LINE_SIZE)
# CACHE_SIZE = 2 ** 12 # CACHE_LINE_COUNT * CACHE_LINE_SIZE
# CACHE_LINE_SIZE = 2 ** 5
# CACHE_LINE_COUNT = 2 ** 7  # CACHE_WAY * CACHE_SETS_COUNT
# CACHE_SETS_COUNT = 2 ** 5

MEM_SIZE = 2 ** 20
ADDR_LEN = 20  # log(mem_size)
CACHE_WAY = 4  # count_line / count_sets
CACHE_TAG_LEN = 10  # addr - index - offset
CACHE_IDX_LEN = 4
CACHE_OFFSET_LEN = 6
CACHE_SIZE = 2 ** 12
CACHE_LINE_SIZE = 2 ** 6  # 2^len_offset
CACHE_LINE_COUNT = 2 ** 6  # cache_size / cache_line_size
CACHE_SETS_COUNT = 2 ** 4  # 2^index_len

def timeLRU(indexBlock, indexLine):
    block = cache[indexBlock]
    for line in block:
        line[1] += 1
    block[indexLine][1] = 0
    block.sort(key=lambda x: x[1])
    for i in range(CACHE_WAY):
        block[i][1] = i


def timePLRU(indexBlock, indexLine):
    block = cache[indexBlock]
    count = 0
    for line in block:
        if (line[1] == 1):
            count += 1
    if count == CACHE_WAY:
        for line in block:
            line[1] = 0
    block[indexLine][1] = 1

def timeRound_Robin(indexBlock):
    block = cache[indexBlock]
    tent = block[0]
    block[0] = block[1]
    block[1] = block[2]
    block[2] = block[3]
    block[3] = tent



def readLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += 1  # addr, command
    tag = adr[:CACHE_TAG_LEN]
    index = adr[CACHE_TAG_LEN:CACHE_IDX_LEN + CACHE_TAG_LEN]
    index = list(map(str, index))
    indexBlock = int("".join(index), 2)

    for indexLine in range(CACHE_WAY):
        line = cache[indexBlock][indexLine]
        if (line[0] == 1 and tag == line[flag:CACHE_TAG_LEN + flag]):
            tact += 7 + bytes  # hit + response + bytes
            hit += 1

            timeLRU(indexBlock, indexLine)
            return

    # read from mem
    tact += 4  # miss
    if (cache[indexBlock][CACHE_WAY - 1][2] == 1):
        tact += 1  # command
        tact += 100  # write in mem
        tact += CACHE_LINE_SIZE // 4  # transfer line
        tact += 1  # response

    tact += 1  # command
    tact += 100  # write in cache
    tact += CACHE_LINE_SIZE // 4
    tact += 1  # response

    tact += bytes + 1  # transfer byte + response

    cache[indexBlock][CACHE_WAY - 1] = [1, 0, 0] + adr
    timeLRU(indexBlock, CACHE_WAY - 1)


def readPLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += 1  # addr, command
    tag = adr[:CACHE_TAG_LEN]
    index = adr[CACHE_TAG_LEN:CACHE_IDX_LEN + CACHE_TAG_LEN]
    index = list(map(str, index))
    indexBlock = int("".join(index), 2)

    for indexLine in range(CACHE_WAY):
        line = cache[indexBlock][indexLine]
        if (line[0] == 1 and tag == line[flag:CACHE_TAG_LEN + flag]):
            tact += 7 + bytes  # hit + response + bytes

            hit += 1
            cache[indexBlock][indexLine][1] = 1
            timePLRU(indexBlock, indexLine)
            return

    # read from mem
    tact += 4  # miss
    for i in range(CACHE_WAY):
        if (cache[indexBlock][i][1] == 0):
            if (cache[indexBlock][i][2] == 1):
                tact += 1  # command
                tact += 100  # write in mem
                tact += CACHE_LINE_SIZE // 4  # transfer line
                tact += 1  # response

            tact += 1  # command
            tact += 100  # write in cache
            tact += CACHE_LINE_SIZE // 4
            tact += 1  # response

            tact += 1 + bytes  # response + bytes

            cache[indexBlock][i] = [1, 1, 0] + adr
            timePLRU(indexBlock, i)
            return

def readRound_Robin(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += 1  # addr, command
    tag = adr[:CACHE_TAG_LEN]
    index = adr[CACHE_TAG_LEN:CACHE_IDX_LEN + CACHE_TAG_LEN]
    index = list(map(str, index))
    indexBlock = int("".join(index), 2)

    for indexLine in range(CACHE_WAY):
        line = cache[indexBlock][indexLine]
        if (line[0] == 1 and tag == line[flag:CACHE_TAG_LEN + flag]):
            tact += 7 + bytes  # hit + response + bytes

            hit += 1
            return

    # read from mem
    tact += 4  # miss
    if (cache[indexBlock][0][1] == 1):
        tact += 1  # command
        tact += 100  # write in mem
        tact += CACHE_LINE_SIZE // 4  # transfer line
        tact += 1  # response

    tact += 1  # command
    tact += 100  # write in cache
    tact += CACHE_LINE_SIZE // 4
    tact += 1  # response

    tact += bytes + 1  # transfer byte + response

    cache[indexBlock][0] = [1, 0] + adr
    timeRound_Robin(indexBlock)

def writeLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += bytes + 1  # # addr, command , bytes
    tag = adr[:CACHE_TAG_LEN]
    index = adr[CACHE_TAG_LEN:CACHE_IDX_LEN + CACHE_TAG_LEN]
    index = list(map(str, index))
    indexBlock = int("".join(index), 2)

    for indexLine in range(CACHE_WAY):
        line = cache[indexBlock][indexLine]
        if (line[0] == 1 and tag == line[flag:CACHE_TAG_LEN + flag]):
            # replace line
            tact += 7  # hit + response
            hit += 1
            cache[indexBlock][indexLine] = [1, 0, 1] + adr
            timeLRU(indexBlock, indexLine)
            return

    tact += 4  # miss

    if (cache[indexBlock][CACHE_WAY - 1][2] == 1):
        tact += 1  # command
        tact += 100  # write in mem
        tact += CACHE_LINE_SIZE // 4  # transfer line
        tact += 1  # response

    tact += 1  # command
    tact += 100  # write in cache
    tact += CACHE_LINE_SIZE // 4  # transfer line
    tact += 1  # response

    tact += 1  # response

    cache[indexBlock][CACHE_WAY - 1] = [1, 0, 1] + adr
    timeLRU(indexBlock, CACHE_WAY - 1)


def writePLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += bytes + 1 # # addr, command, bytes

    tag = adr[:CACHE_TAG_LEN]
    index = adr[CACHE_TAG_LEN:CACHE_IDX_LEN + CACHE_TAG_LEN]
    index = list(map(str, index))
    indexBlock = int("".join(index), 2)

    for indexLine in range(CACHE_WAY):
        line = cache[indexBlock][indexLine]
        if (line[0] == 1 and tag == line[flag:CACHE_TAG_LEN + flag]):
            # replace line
            tact += 7  # hit + response
            hit += 1
            cache[indexBlock][indexLine] = [1, 1, 1] + adr
            timePLRU(indexBlock, indexLine)
            return

    tact += 4  # miss

    for i in range(CACHE_WAY):
        if (cache[indexBlock][i][1] == 0):
            if (cache[indexBlock][i][2] == 1):
                tact += 1 # command
                tact += 100  # write in mem
                tact += CACHE_LINE_SIZE // 4  # transfer line
                tact += 1  # response
            tact += 1 # command
            tact += 100  # write in cache
            tact += CACHE_LINE_SIZE // 4  # transfer line
            tact += 1  # response

            tact += 1  # response

            cache[indexBlock][i] = [1, 1, 1] + adr
            timePLRU(indexBlock, i)
            return

def writeRound_Robin(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += bytes + 1  # # addr, command , bytes
    tag = adr[:CACHE_TAG_LEN]
    index = adr[CACHE_TAG_LEN:CACHE_IDX_LEN + CACHE_TAG_LEN]
    index = list(map(str, index))
    indexBlock = int("".join(index), 2)

    for indexLine in range(CACHE_WAY):
        line = cache[indexBlock][indexLine]
        if (line[0] == 1 and tag == line[flag:CACHE_TAG_LEN + flag]):
            # replace line
            tact += 7  # hit + response
            hit += 1
            cache[indexBlock][indexLine] = [1, 1] + adr
            return

    tact += 4  # miss
    if (cache[indexBlock][0][1] == 1):
        tact += 1  # command
        tact += 100  # write in mem
        tact += CACHE_LINE_SIZE // 4  # transfer line
        tact += 1  # response

    tact += 1  # command
    tact += 100  # write in cache
    tact += CACHE_LINE_SIZE // 4  # transfer line
    tact += 1  # response

    tact += 1  # response

    cache[indexBlock][0] = [1, 1] + adr
    timeRound_Robin(indexBlock)


cache = []
flag = 3

for i in range(CACHE_LINE_COUNT // CACHE_WAY):
    block = []
    for j in range(CACHE_WAY):
        block.append([0] * (ADDR_LEN + flag))
    cache.append(block)

curAddr = 0

M = 64
N = 60
K = 32

a = []
b = []
c = []
for i in range(M * K):
    addAddr = (ADDR_LEN - len(bin(curAddr)[2:])) * [0] + list(bin(curAddr)[2:])
    a.append(addAddr)
    curAddr += 1

for i in range(N * K):
    addAddr = (ADDR_LEN - len(bin(curAddr)[2:])) * [0] + list(bin(curAddr)[2:])
    b.append(addAddr)
    curAddr += 2

for i in range(M * N):
    addAddr = (ADDR_LEN - len(bin(curAddr)[2:])) * [0] + list(bin(curAddr)[2:])
    c.append(addAddr)
    curAddr += 4

hit = 0
miss = 0
requests = 0
tact = 0

pa = 0
pc = 0

for y in range(M):
    tact += 1

    for x in range(N):
        tact += 1
        pb = 0
        tact += 2  # initial pb, s

        for k in range(K):
            tact += 1
            readLRU(a[pa + k], 1)
            readLRU(b[pb + x], 1)
            tact += 2  # read 2
            pb += N
            tact += 7

        writeLRU(c[pc + x], 2)
        tact += 1  # write 1

    pa += K
    pc += N
    tact += 2

print(f"LRU:\thit perc. {round(hit / requests * 1000000) / 10000}%\ttime: {tact}")

cache = []
flag = 3

for i in range(CACHE_LINE_COUNT // CACHE_WAY):
    block = []
    for j in range(CACHE_WAY):
        block.append([0] * (ADDR_LEN + flag))
    cache.append(block)

hit = 0
miss = 0
requests = 0
tact = 0

pa = 0
pc = 0

for y in range(M):
    tact += 1

    for x in range(N):
        tact += 1
        pb = 0
        tact += 2  # initial pb, s

        for k in range(K):
            tact += 1
            readPLRU(a[pa + k], 1)
            readPLRU(b[pb + x], 1)

            tact += 2

            pb += N
            tact += 7

        writePLRU(c[pc + x], 2)
        tact += 1

    pa += K
    pc += N
    tact += 2

print(f"pLRU:\thit perc. {round(hit / requests * 1000000) / 10000}%\ttime: {tact}")

cache = []
flag = 2

for i in range(CACHE_LINE_COUNT // CACHE_WAY):
    block = []
    for j in range(CACHE_WAY):
        block.append([0] * (ADDR_LEN + flag))
    cache.append(block)

hit = 0
miss = 0
requests = 0
tact = 0

pa = 0
pc = 0

for y in range(M):
    tact += 1 # new iter

    for x in range(N):
        tact += 1 # new iter
        pb = 0
        tact += 2  # initial pb, s

        for k in range(K):
            tact += 1 # new iter
            readRound_Robin(a[pa + k], 1)
            readRound_Robin(b[pb + x], 1)
            tact += 2 # funcs read

            pb += N
            tact += 7 # sum and mult

        writeRound_Robin(c[pc + x], 2)
        tact += 1 # func write

    pa += K
    pc += N
    tact += 2 # sum

print(f"RR:\thit perc. {round(hit / requests * 1000000) / 10000}%\ttime: {tact}")

