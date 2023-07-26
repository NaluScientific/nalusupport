---
title: Nalu Exporter
parent: Software Downloads
permalink: /software/naluexporter/
product: naluexporter
layout: software
nav_order: 2
---

Nalu Exporter is a new lightweight command-line tool for interacting with acquisitions captured with [NaluScope](/software/naluscope). Its primary functionality is exporting acquisitions to CSV, facilitating analysis, processing, and data sharing.

There is no installer for this tool; it may be placed in any suitable folder. For convenience, it is recommended to download the executable to a folder where acquisitions or CSV files will be stored.

## Usage

The Nalu Exporter tool is run from the command prompt (Windows). To open the command prompt, press the Windows key and type `cmd`. The command prompt will open; navigate to the folder where the Nalu Exporter executable is located. For example, if the executable is located in `C:\Users\John\Downloads`, type `cd C:\Users\John\Downloads` and press Enter.


### Export Data
To export data to CSV:

```
naluexporter export PATH/TO/ACQUISITION --output PATH/TO/OUTPUT/DIR -p
```

The `-p`/`--pedestals` flag indicates the data should be exported with pedestals correction. It may be omitted if uncorrected data is desired, or if the acquisition does not contain pedestals.

The `-o`/`--output` indicates the output directory for CSV files. If omitted, the current working directory will be used. One or more CSV files will be created in the output directory, one for each set of 500 events.

### List Acquisitions
To list acquisitions in a directory:

```
naluexporter list DIRECTORY
```

The `DIRECTORY` argument is optional; if omitted, the current working directory will be used. The command will display a table of acquisitions in the directory along with some relevant information.
