# abbr.ninja API Server

This is the API server for the link shortener on [abbr.ninja](https://abbr.ninja/).


[API endpoint documentation](https://api.abbr.ninja/)

Source code for:
* [API documentation](https://github.com/chen-ky/abbr.ninja-api-doc)
* [Frontend](https://github.com/chen-ky/abbr.ninja-web)

## Dependencies
Refer to [requirements.txt](src/requirements.txt).

<!-- ## Generating Documentation

Refer to Slate [documentation](https://github.com/slatedocs/slate/wiki/Using-Slate-Natively)
for dependencies.

```sh
bundle exec middleman build
``` -->

## Building the Container

`podman` was used to run and build the container but this should also work
for `docker`.

1. Populate `config.toml` with your desired settings.
2. Clone from the [API doc repository](https://github.com/chen-ky/abbr.ninja-api-doc) and build the document.
3. Copy the `build` directory from the API doc directory to this directory where the path should be
`./doc/build`.
4. Run `podman build -t <INSERT_CONTAINER_NAME> .` in the root directory of the repository containing the `Dockerfile`.
5. Start your container by `podman run --network <INSERT_CONTAINER_NETWORK_NAME> -p <INSERT_HOST_PORT>:8081 -d -t <INSERT_CONTAINER_NAME>`

You would also need a MariaDB server running and a database named `uri_shortener` created.

## Deployment Recommendation

* A nginx reverse proxy pointed to this server is recommended since this server does not support configuration for TLS/SSL and for higher performance.
[How to Configure a Nginx HTTPs Reverse Proxy on Ubuntu Bionic - Scaleway](https://www.scaleway.com/en/docs/how-to-configure-nginx-reverse-proxy/)

## Donations
Feel free to donate if you find this helpful!

* BTC:
    * [`bc1qww8sktvenl044juafgvt068yah9dxuwrhht4kq`](bitcoin:bc1qww8sktvenl044juafgvt068yah9dxuwrhht4kq?message=abbr.ninja%20Donation)
    * [`16G7WnKzNdYc48NtEeiVuLNeaLcoXBw1K4`](bitcoin:16G7WnKzNdYc48NtEeiVuLNeaLcoXBw1K4?message=abbr.ninja%20Donation)
* ETH:
    * [`0x5d67690768F0Fc4780c578393Ca567e5bCb38378`](ethereum:0x5d67690768F0Fc4780c578393Ca567e5bCb38378)
