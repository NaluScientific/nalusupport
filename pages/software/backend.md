---
title: Backend Server
parent: Software Downloads
product: backend
permalink: /software/backend/
layout: software
nav_order: 2
---

The standalone backend is a separate distributable which can be run separately from NaluScope. In combination with NaluScope it can be used as a DAQ for the hardware, while NaluScope acts as the user interface. Installing the backend may be useful for some hardware setups, as it allows for interfacing with NaluScope over a network connection.

## Installation

There is no installer for the backend; it may be placed in any suitable folder. For convenience, it is recommended to download the executable to a folder where acquisitions will be stored.

### Python Package

Python 3.7+ bindings for running the backend are available on [PyPI](https://pypi.org/project/naludaq-rs/):

```
>> pip install naludaq_rs
```
