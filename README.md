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

`update_qs_docs_ver.py` is used to update the Quickstart documentation, it will download the Quickstart guide (Google Doc), convert it to PDF, and upload to the google drive.
To be able to do this the script will ask for access.
The script require you to have a file `credentials.json` in the same folder as the script. Credentials file can be obtained from [https://console.cloud.google.com/apis/credentials] and then rename the file to `credentials.json`. The Google Drive API must be enabled for the corresponding project in the Google Cloud Console to successfully authorize access to Google Drive. 

### WSL

If the `BROWSER` environment variable is not configured in the WSL environment, you may encounter the following error when executing `update_qs_docs_ver.py`:

```sh
webbrowser.Error: could not locate runnable browser
```

To avoid this error, the ```BROWSER``` environment variable can be set to a browser available on Windows. The following command can be used to set the default browser used by WSL for the duration of its shell session:

```sh
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
```

To set the default browser across shell sessions, the following commands can be used:

```sh
echo 'export BROWSER="/mnt/c/Windows/System32/cmd.exe /c start"' >> ~/.bashrc
source ~/.bashrc

```