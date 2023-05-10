---
title: Firmware Downloads
permalink: /firmware/
layout: single
---


{% assign firmware_versions = site.data.firmware_versions | sort %}

{% assign cols = "Version;Download" | split: ";" %}

{% for key in firmware_versions %}
{% assign name = key[0] %}
{% assign value = key[1] %}

{% capture board %}
{% include version_table.html versions=value cols=cols %}
{% endcapture %}
{% include accordion.html name=name content=board %}
{% capture older %}
{% endcapture %}
{% endfor %}


{% include accordion_enable.html %}
