# lightnvm-hw
A Hello-World for LightNVM, useful tools for both QEMU and real
hardware implementations of the LightNVM (OpenChannel SSD) project.

## config

This folder contains config files for various incarnations of the
lightnvm linux kernel. The naming convnention is config.<sha> where
<sha> is the start of the sha key for the linux-lightnnvm fork of the
main link kernel (https://github.com/OpenChannelSSD/linux). 

There is also a simple build shell script with rules on how to build
the kernel on debian/ubuntu based systems.

## qemu

This folder contains some useful scripts for managing the lighnvm fork
of QEMU to enable testing without physical lightnvm compliant block
devices. The QEMU fork is at
https://github.com/OpenChannelSSD/qemu-nvme. 