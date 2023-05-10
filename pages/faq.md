---
layout: default
title: FAQ
permalink: /faq/
nav_order: 4
---

Our FAQ/Troubleshooting page is a compilation of the most commonly asked questions and issues that our customers have encountered while using our products.
We have provided detailed solutions and step-by-step instructions for each problem, so that our customers can get back to their research as quickly as possible.

## General Questions

### How Do I Request Support?

Please [email us](/contact/) to request support.

### How Do I Update My Software?

**Windows**

1. First, uninstall your current version of the software.
2. Visit the [Software](/software/) page and download the latest installer.
3. Run the installer.

**Linux**

1. Visit the [Software](/software/) page and download the latest `.tar.gz` file.
2. Older versions may be deleted if desired.


## Troubleshooting

Below are some solutions to issues you may encounter when using Nalu Scientific products.
If the solutions below are not working or your problem is not listed, please [contact us](/contact/) to request support.

### Naluscope

Below are some solutions to issues you may encounter when using Naluscope. More troubleshooting support can be found in the [Naluscope Manual](/documentation/).

<div class="notice--info" markdown="1">
Any driver issues can usually be solved by downloading these drivers:

- [VCP](https://ftdichip.com/drivers/vcp-drivers/)
- [D2XX](https://ftdichip.com/drivers/d2xx-drivers/)
- [D3XX (for USB 3.0)](https://ftdichip.com/drivers/d3xx-drivers/)
</div>

#### Board Not Detected

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

#### Cannot Startup Board

If the board does not start up, here are some things to try:

* Power cycle the board.
* Make sure the correct port and board model are selected in the startup dialog.
* Make sure the board is powered on and connected with a working cable.
* Make sure the software and firmware are up to date.


#### Cannot Capture Events

If the board suddenly stops sending back data after previously working, here are some things to try:

* Make sure the board still has power and hasn't accidentally been disconnected.
* In the *Settings* menu, select *Reset* and then *Reinitialize*.
* Close and reopen NaluScope, then start up the board again.

These steps may also help if calibrations cannot be generated.

#### (Linux) Black Screen on Startup

This could be due to incompatible or improperly links to the graphics driver between
Linux distributions. This can be solved by deleting `libstdc++.so.6` in the `nalu` folder,
allowing the system to fall back on its own `libstdc++.so`.
