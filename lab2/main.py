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
        tact += 100  # write in mem
        tact += CACHE_LINE_SIZE // 2  # transfer line
        tact += 1  # response
    tact += 100  # write in cache
    tact += CACHE_LINE_SIZE // 2
    tact += 1  # response

    tact += bytes + 1  # transfer byte + response

    cache[indexBlock][CACHE_WAY - 1] = [1, 0, 0] + adr
    timeLRU(indexBlock, CACHE_WAY - 1)


def writeLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += bytes
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
        tact += 100  # write in mem
        tact += CACHE_LINE_SIZE // 2  # transfer line
        tact += 1  # response

    tact += 100  # write in cache
    tact += CACHE_LINE_SIZE // 2  # transfer line
    tact += 1  # response

    tact += 1  # response

    cache[indexBlock][CACHE_WAY - 1] = [1, 0, 1] + adr
    timeLRU(indexBlock, CACHE_WAY - 1)


cache = []
flag = 3

for i in range(CACHE_LINE_COUNT // CACHE_WAY):
    block = []
    for j in range(CACHE_WAY):
        block.append([0] * (CACHE_TAG_LEN + flag))
    cache.append(block)

hit = 0
miss = 0
requests = 0
tact = 0

M = 64
N = 60
K = 32

curAddr = 0

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

            pb += N
            tact += 7

        writeLRU(c[pc + x], 2)

    pa += K
    pc += N
    tact += 2

print(f"LRU:\thit perc. {round(hit / requests * 1000000) / 10000}%\ttime: {tact}")


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


def readPLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += 1
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
                tact += 100  # write in mem
                tact += CACHE_LINE_SIZE // 2  # transfer line
                tact += 1  # response

            tact += 100  # write in cache
            tact += CACHE_LINE_SIZE // 2
            tact += 1  # response

            tact += 1 + bytes  # response + bytes

            cache[indexBlock][i] = [1, 1, 0] + adr
            timePLRU(indexBlock, i)
            return


def writePLRU(adr, bytes):
    global hit, miss, requests, tact
    requests += 1
    tact += bytes

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
                tact += 100  # write in mem
                tact += CACHE_LINE_SIZE // 2  # transfer line
                tact += 1  # response
            tact += 100  # write in cache
            tact += CACHE_LINE_SIZE // 2  # transfer line
            tact += 1  # response

            tact += 1  # response

            cache[indexBlock][i] = [1, 1, 1] + adr
            timePLRU(indexBlock, i)
            return


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

M = 64
N = 60
K = 32

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

            pb += N
            tact += 7

        writePLRU(c[pc + x], 2)

    pa += K
    pc += N
    tact += 2

print(f"pLRU:\thit perc. {round(hit / requests * 1000000) / 10000}%\ttime: {tact}")
