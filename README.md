# inky-dsp (Inky Display)

## Setup

### Enable I2C and SPI

Edit the Raspberry Pi boot configuration on the host:

```bash
$ sudo vi /boot/firmware/config.txt
```

Enable `I2C`:

```
dtparam=i2c_arm=on
```

Ensure `SPI` is enabled without hardware CS:

```
dtparam=spi=on
dtoverlay=spi0-0cs
```

### Set the static IP

```bash
$ sudo nmtui edit "Wired connection 1"
```
