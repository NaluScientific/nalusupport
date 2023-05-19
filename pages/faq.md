---
layout: default
title: FAQ
permalink: /faq/
nav_order: 0
---

Our FAQ/Troubleshooting page is a compilation of the most commonly asked questions and issues that our customers have encountered while using our products.
We have provided detailed solutions and step-by-step instructions for each problem, so that our customers can get back to their research as quickly as possible.

# General Questions

## How Do I Request Support?

Please [email us](/contact/) to request support.

## How Do I Update My Software?

**Windows**

1. First, uninstall your current version of the software.
2. Visit the [Software](/software/) page and download the latest installer.
3. Run the installer.

**Linux**

1. Visit the [Software](/software/) page and download the latest `.tar.gz` file.
2. Older versions may be deleted if desired.


# Troubleshooting

Below are some solutions to issues you may encounter when using Nalu Scientific products.
If the solutions below are not working or your problem is not listed, please [contact us](/contact/) to request support.

## Naluscope

Below are some solutions to issues you may encounter when using Naluscope. More troubleshooting support can be found in the [Naluscope Manual](/boards/) for your board.

<div class="notice--info" markdown="1">
Any driver issues can usually be solved by downloading these drivers:

- [VCP](https://ftdichip.com/drivers/vcp-drivers/)
- [D2XX](https://ftdichip.com/drivers/d2xx-drivers/)
- [D3XX (for USB 3.0)](https://ftdichip.com/drivers/d3xx-drivers/)
</div>

----

### Board Not Detected

If the board does not appear in the list of available ports in the startup dialog, here are some things to try:

* Click the "Refresh" button in the dialog to reload the list of available ports.
* Make sure the board is powered on and connected with a working cable.
* Make sure the board is programmed with the latest firmware.
* Check the Windows Device Manager for driver issues.

If the application is used on Linux, the port's permissions may need to be modified.
First, find which `/dev/ttyUSB<Port Number>` device the board appears as. This can be done by running `ls /dev/ttyUSB*` before and after connecting the board. The new device that appears is the correct port. Then, run the following command to modify the permissions:

```sh
sudo chmod 777 /dev/ttyUSB<Port Number>
```

----

### Cannot Startup Board

If the board does not start up, here are some things to try:

* Power cycle the board.
* Make sure the correct port and board model are selected in the startup dialog.
* Make sure the board is powered on and connected with a working cable.
* Make sure the software and firmware are up to date.

----

### Cannot Capture Events

If the board suddenly stops sending back data after previously working, here are some things to try:

* Make sure the board still has power and hasn't accidentally been disconnected.
* In the *Settings* menu, select *Reset* and then *Reinitialize*.
* Close and reopen NaluScope, then start up the board again.

These steps may also help if calibrations cannot be generated.

---

## Linux Troubleshooting

### Black Screen on Startup

This could be due to incompatible or improperly links to the graphics driver between
Linux distributions. This can be solved by deleting `libstdc++.so.6` in the `nalu` folder,
allowing the system to fall back on its own `libstdc++.so`.

---

### FTDI Devices Not Showing Up
**Problem**: The device is showing up as only UART and not FTDI.

This occurs when a service is converting the FTDI device into a COM PORT (UART).

**Solution**: 
Running the command: `sudo modprobe -r ftdi_sio` will stop the conversion of the FTDI device.
You will have to run this command each time you plug the device/restart the computer.
Consider adding a rule to prevent `ftdi_sio` from running.

---

### Error: DEVICE_NOT_FOUND
**Problem**: Naluscope won't startup with error:
```bash
File "/build/naluscope/build/venvs/gui_build/lib/python3.9/site-packages/ftd2xx/ftd2xx.py", line 133, in call_ft
ftd2xx.ftd2xx.DeviceError: DEVICE_NOT_FOUND
```

This error occurs when naluscope does not have permission to the FTDI device.

**Solution**: 
The permissions can be fixed by:

Determine where the board's USB is mounted to. `lsusb` can be helpful.
`lsusb` will output in the form:

`Bus 002 Device 001: ID xxxx:xxxx (FTDI_DEVICE)`

Use the Bus & Device number to locate where the device is mounted at the directory:

`/dev/bus/usb/002/001` Replace 002 & 001 with your corresponding Bus and Device numbers.

Set permissions for the files with `sudo chmod 777 /dev/bus/usb/path_to_your_usb`

---

### Error: Settings schema
**Problem**: Naluscope crashes when trying to select a project directory. 
```bash
Settings schema 'org.gtk.Settings.FileChooser' does not contain a key named 'show-type-column'
```

This error occurs when you have an older version of GTK installed to your system, and the older schema
does not have the keys needed by FileChooser.
The solution will be following the steps from [here](https://gitlab.com/inkscape/inkscape/-/issues/1616)

**Solution**: 
Download the newer [schema file](https://gitlab.gnome.org/GNOME/gtk/-/blob/c925221aa804aec344bdfec148a17d23299b6c59/gtk/org.gtk.Settings.FileChooser.gschema.xml)
and move the file to 

`/usr/share/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml`

Run `glib-compile-schemas .` in the `/usr/share/glib-2.0/schemas/` directory.

Last use Alt-F2 to run the command `r` to restart the gnome-shell
