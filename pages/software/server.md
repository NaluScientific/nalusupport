---
title: Standalone Server
parent: Software Downloads
product: backend
permalink: /software/server/
layout: software
nav_order: 2
---

The standalone server is a separate distributable which can be run separately from NaluScope. It is used in combination with NaluScope for high-speed data acquisition from the hardware. The server comes bundled with NaluScope and using the standalone version is optional. However, using the standalone server offers more flexibility in terms of hardware setup, as it can be run on a separate machine from NaluScope.

## Installation

There is no installer for the server; it may be placed in any suitable folder. For convenience, it is recommended to download the executable to a folder where acquisitions will be stored.

### Python Package

Python 3.7+ bindings for running the standalone server are available on [PyPI](https://pypi.org/project/naludaq-rs/):

```
>> pip install naludaq_rs
```

### Usage

If the standalone server is to be used on the same machine as NaluScope, you may simply double-click the executable or run it from the command line with no additional arguments. The server will be hosted on `127.0.0.1` (loopback) at port `7878` by default; these are the values you should use for the server address field in NaluScope.

If the standalone server is to be used on a separate machine, you must specify the appropriate IP address to host the server on. The address must be visible over the network to the machine running NaluScope. The port may be specified as well, but it is recommended to use the default port of `7878`.


**Command Line Usage:**
```sh
server_{version}.exe [OPTIONS]
```

Options:
```
  -a, --addr <ADDR>        The address to host the server at. Expected format is "{HOST}:{PORT}" [default: 127.0.0.1:7878]
  -o, --output <OUTPUT>    The output directory for acquisitions
  -d, --debug              Show debug messages
      --api                Open an interactive API in the system browser
      --log-dir <LOG_DIR>  The directory to store log files in
  -h, --help               Print help information
  -V, --version            Print version information
```
