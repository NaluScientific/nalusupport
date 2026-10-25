# Nalu Scientific Support Site

## Users

If you notice a problem on this website or would like to request changes, please feel free to either [email us](/contact/) or open an issue on this repository.

If you feel adventurous, you can also make the changes yourself and open a pull request.


# Developers

## Setup

This website is built using [Jekyll](https://jekyllrb.com/) 4.4, a static site generator, on Ruby 3.4 (see `.ruby-version`).

To install Ruby and Bundler, follow the instructions [here](https://jekyllrb.com/docs/installation/). It is highly recommended to run
your development environment on Linux or macOS.

Gem versions are pinned in the committed `Gemfile.lock`. On Windows, add your platform to the lockfile once with
`bundle lock --add-platform x64-mingw-ucrt` before installing.

## Running Locally

To run the website locally, run the following commands in the root directory of this repository:

```sh
bundle install
bundle exec jekyll serve
```

The website will be available at `http://localhost:4000` by default. The `--port` option can be used to specify a different port.

### Docker (no Ruby required)

If you don't have Ruby installed, you can use Docker instead:

```sh
docker build -t nalusupport .
docker run --rm -p 4000:4000 -v "$(pwd):/site" nalusupport
```

The site will be available at `http://localhost:4000`. Note that live reload does not work with Docker volume mounts on Windows — restart the container to pick up changes.

## Build and Deploy

The `Build and Deploy Site` GitHub Actions workflow builds the site on every push and pull request and uploads the built
`_site` and the resolved `Gemfile.lock` as artifacts. Pushes to `main` build from the committed lockfile and deploy to
GitHub Pages.

To upgrade a gem without Ruby installed locally, change the `Gemfile` on a branch, push, and commit the `gemfile-lock`
artifact from the workflow run.


## Update documentation

`update_qs_docs_ver.py` is used to update the Quickstart documentation, it will download the Quickstart guide, convert it to PDF and upload to the google drive.
To be able to do this the script will ask for access.
The script require you to have a file `credentials.json` in the same folder as the script. Credentials file can be obtained from [https://console.cloud.google.com/apis/credentials] and then rename the file to `credentails.json`.