/* smutool  Tool for SMU
 * Copyright (C) 2015  Damien Zammit <damien@zamaudio.com>
 * Copyright (C) 2023  Sheep Sun <sunxiaoyang2003@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * See <http://www.gnu.org/licenses/>. 
 */

#include <stdio.h>
#include <inttypes.h>
#include <pci/pci.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/io.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
	uint32_t fd_mem;
	struct pci_access *pacc;
	struct pci_dev *nb;
	if (iopl(3)) {
		perror("iopl");
		fprintf(stderr, "You need to be root\n");
		exit(1);
	}

        if ((fd_mem = open("/dev/mem", O_RDWR)) < 0) {
                perror("Can not open /dev/mem");
                exit(1);
        }

	pacc = pci_alloc();
	pacc->method = PCI_ACCESS_I386_TYPE1;
	pci_init(pacc);
	pci_scan_bus(pacc);
	nb = pci_get_dev(pacc, 0, 0, 0x0, 0);
	pci_fill_info(nb, PCI_FILL_IDENT | PCI_FILL_BASES | PCI_FILL_SIZES | PCI_FILL_CLASS);
	
	uint32_t addr, data;
	if (argc == 2) {
		sscanf(argv[1], "%x", &addr);
		pci_write_long(nb, 0xb8, addr);
		data = pci_read_long(nb, 0xbc);
		printf("0x%08x\n", data);
	} else if (argc == 3) {
		sscanf(argv[1], "%x", &addr);
		sscanf(argv[2], "%x", &data);
		pci_write_long(nb, 0xb8, addr);
		pci_write_long(nb, 0xbc, data);
	} else {
		printf("Wrong args\n");
	}

//	fprintf(stderr, "exiting\n");
	pci_cleanup(pacc);
	return 0;
}
