---
title: Firmware Downloads
permalink: /firmware/
layout: single
---

{% assign naluscope = site.data.firmware_versions.naluscope %}
{% assign naludaq_rs = site.data.firmware_versions.naludaq_rs %}

{% assign naluscope_cols = "Version;Download;Manual" | split: ";" %}
{% assign naludaq_rs_cols = "Version;Download" | split: ";" %}






## NaluScope

{% capture latest %}
{% include version_table.html versions=naluscope.latest cols=naluscope_cols %}
{% endcapture %}
{% include accordion.html name="Latest Version" content=latest expand=true %}


{% capture older %}
{% include version_table.html versions=naluscope.older cols=naluscope_cols %}
{% endcapture %}
{% include accordion.html name="Older Versions" content=older %}




## Backend Server

Python bindings for the backend are also available on [PyPI](https://pypi.org/project/naludaq-rs/):

```bash
>> pip install naludaq_rs
```

{% capture latest %}
{% include version_table.html versions=naludaq_rs.latest cols=naludaq_rs_cols %}
{% endcapture %}
{% include accordion.html name="Latest Version" content=latest expand=true %}

{% capture older %}
{% include version_table.html versions=naludaq_rs.older cols=naludaq_rs_cols %}
{% endcapture %}
{% include accordion.html name="Older Versions" content=older expand=true %}


{% include accordion_enable.html %}
