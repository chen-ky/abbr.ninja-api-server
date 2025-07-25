#!/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import app_info
import api_server
import os
import sentry_sdk

import sys

# def app(*args, **kwargs):
#     import sys
#     # sys.argv = ['--gunicorn']
#     sys.argv = []
#     for k in kwargs:
#         sys.argv.append("--" + k)
#         sys.argv.append(kwargs[k])
#     # print(sys.argv)
#     # print(kwargs)
#     # print(args)
#     return main()


def main():
    if "SENTRY_DSN" in os.environ:
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN").strip(),
            send_default_pii=False,
            traces_sample_rate=1.0,
            profile_session_sample_rate=1.0,
            profile_lifecycle="trace",
        )
        print("Sentry SDK initialised")

    print(f"Starting API server v{app_info.VERSION}...")

    application = api_server.app
    return application


if "__main__" == __name__:
    from cheroot.wsgi import Server as CherryPyServer
    host = '127.0.0.1'
    port = 8080
    server = CherryPyServer((host, port), main())
    try:
        server.safe_start()
    except KeyboardInterrupt:
        server.stop()
