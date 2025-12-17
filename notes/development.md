# Development

You will need to have a working [Python 3.13](https://www.python.org/downloads/release/python-3132/) installation, [uv](https://docs.astral.sh/uv/), [mkcert](https://github.com/FiloSottile/mkcert), and a POSIX compliant `make`. To optionally build the HTML documentation files you will also need [cmark](https://github.com/commonmark/cmark).

Ensure that you have the pre-commit hook installed:

```shell
make sync-all
uv run --frozen pre-commit install
```

To run the project, use the following commands, which will add a local CA root to your OS and browser certificate store if using Firefox:

```shell
make sync-all
make certs-local
make serve
```

And add the following line to your `/etc/hosts`:

```text
127.0.0.1  localhost.apache.org
```

The website will be available at [https://localhost.apache.org:8080/](https://localhost.apache.org:8080/) using a self-signed certificate.
