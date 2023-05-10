---
title: Firmware Downloads
permalink: /firmware/
layout: single
---

On this page, you will find a comprehensive list of firmware updates organized by product model and version number.

If you have any questions about our firmware, or need assistance with installation, please don't hesitate to [contact us](/contact/). We are always happy to help you get the most out of our products.

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
