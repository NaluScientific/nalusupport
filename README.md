# Nalu Scientific Support Site

## Users

If you notice a problem on this website or would like to request changes, please feel free to either [email us](/contact/) or open an issue on this repository.

If you feel adventurous, you can also make the changes yourself and open a pull request.


# Developers

## Setup

This website is built using [Jekyll](https://jekyllrb.com/), a static site generator.

To install Jekyll, follow the instructions [here](https://jekyllrb.com/docs/installation/). It is highly recommended to run
your development environment on Linux or macOS.

## Running Locally

To run the website locally, run the following command in the root directory of this repository:

```sh
bundle exec jekyll serve
```

The website will be available at `http://localhost:4000` by default. The `--port` option can be used to specify a different port.


## Update documentation

`update_qs_docs_ver.py` is used to update the Quickstart documentation, it will download the Quickstart guide, convert it to PDF and upload to the google drive.
To be able to do this the script will ask for access.
The script require you to have a file `credentials.json` in the same folder as the script. Credentials file can be obtained from [https://console.cloud.google.com/apis/credentials] and then rename the file to `credentails.json`.