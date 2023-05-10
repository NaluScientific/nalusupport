---
title: Firmware Downloads
permalink: /firmware/
layout: single
---


{% assign firmware_versions = site.data.firmware_versions | sort %}

{% assign naluscope_cols = "Version;Download" | split: ";" %}
{% assign naludaq_rs_cols = "Version;Download" | split: ";" %}






## NaluScope

{% for key in firmware_versions %}
{% assign name = key[0] %}
{% assign value = key[1] %}

{% capture board %}
{% include version_table.html versions=value cols=naluscope_cols %}
{% endcapture %}
{% include accordion.html name=name content=board %}
{% capture older %}
{% endcapture %}
{% endfor %}


{% include accordion_enable.html %}
