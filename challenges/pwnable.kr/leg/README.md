# `leg` Solution

The three addresses are collected from the given [leg.asm](leg.asm) and summed. It must be thought about the `arm`'s `pc` value (the register has address of 2 instructions ahead). Even if you miss the right value you can try every sum from  `108400` to `10840c` with `0x4` step.

# Notes

    0x00008cdc+8
    0x00008d10+32
    0x00008d80+68

    wget http://ftp.linux.org.uk/pub/linux/arm/fedora/qemu/zImage-versatile-2.6.24-rc7.armv5tel http://cdot.senecac.on.ca/arm/arm1.xml http://cdot.senecac.on.ca/arm/arm1.img.gz

    0x00008ce4 + 0x00008d08 + 4 + 0x00008d80 = 108400


