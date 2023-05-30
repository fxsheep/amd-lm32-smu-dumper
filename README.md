# amd-lm32-smu-dumper
Quick &amp; Dirty tool to dump LM32-based AMD SMU bootrom on patched SMU FW

## Dependency
`libpci-dev`

## Build
smurw - the PCI address space bridging tool, needs to be built:

`
gcc smurw.c -o smurw -lpci
`

## Run

`
sudo python3 dump_rom.py
`

Dumping should finish in a few minutes, result is written to `rom_dump_0x0.bin`.  
SMU FW will be interrupted and stop working until next boot, so it's advised to reboot the platform as soon as possible.

## Tested on

A4-6210  

## Thanks to

jevinskie for [amd-lm32-smu-exploit](https://github.com/jevinskie/amd-lm32-smu-exploit)  

[smutool](https://github.com/zamaudio/smutool)  
