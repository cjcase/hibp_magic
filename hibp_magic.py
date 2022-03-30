#!/usr/bin/env python

#
# HaveIBeenPwned API Magic - Quick and dirty
#                                  by cjcase

#    hibp_magic - Quick and dirty HaveIBeenPwned API v3 interface
#    Copyright (C) 2022 cjcase
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/

import requests
import argparse
import time
import sys

# following api rules
user_agent = "hibp_magic.py/v0.2"
api_breach = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"
api_paste = "https://haveibeenpwned.com/api/v3/pasteaccount/{}"
api_breach_info = "https://haveibeenpwned.com/api/v3/breach/{}"
wait_time = 1.5

def insight(code):
    codes = {
    200:"Ok — everything worked and there's a string array of pwned sites for the account",
    400:"Bad request — the account does not comply with an acceptable format (i.e. it's an empty string)",
    401:"Unauthorised — either no API key was provided or it wasn't valid",
    403:"Forbidden — no user agent has been specified in the request",
    404:"Not found — the account could not be found and has therefore not been pwned",
    429:"Too many requests — the rate limit has been exceeded",
    503:"Service unavailable — usually returned by Cloudflare if the underlying service is not available, or you're trying too much"
    }
    return codes[code]


def magic_request(api_arg, request_type, retry=False, debug=False):
    headers = {"User-agent":user_agent, "hibp-api-key":args.apikey}
    url = ""

    if request_type == "breach":
        url = api_breach.format(api_arg)
    elif request_type == "paste":
        url = api_paste.format(api_arg)
    elif request_type == "info":
        url = api_breach_info.format(api_arg)
    else:
        print(f"[e] woah thats not implemented!", file=sys.stderr)

    if debug:
        print(f"[d] url:{url} headers:{headers}", file=sys.stderr)
    
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        print(f"\"{api_arg}\",\"{req.json()}\",\"{request_type}\"")
        return req.json()
    elif req.status_code == 404:
        print(f"\"{api_arg}\",\"not pwned :(\",\"{request_type}\"")
    elif req.status_code == 429 and retry:
        if debug:
            print(f"[d] too many requests({request_type}), waiting and retrying...", file=sys.stderr)
        time.sleep(wait_time)
        magic_request(api_arg, request_type, retry=retry, debug=debug)
    else:
        print(f"[e] oops! {insight(req.status_code)}", file=sys.stderr)


def magic_info(breach, retry=False, debug=False):
    try:
        r = magic_request(email, "breach", retry=retry, debug=debug)
    
    except Exception as e:
        print(f"[e] something sucked: {str(e)}", file=sys.stderr)
    except KeyboardInterrupt:
        print(f"[!] ok ok cancelling, one sec...")


def magic_single(email, retry=False, debug=False):
    try:
        r_breach = magic_request(email, "breach", retry=retry, debug=debug)
        r_paste = magic_request(email, "paste", retry=retry, debug=debug)
        return (r_breach, r_paste)
    except Exception as e:
        print(f"[e] something sucked: {str(e)}", file=sys.stderr)
    except KeyboardInterrupt:
        print(f"[!] ok ok cancelling, one sec...")


def magic(filename, retry=False, debug=False):
    with open(filename) as emails:
        for email in emails:
            email = email[:-1]
            if debug:
                print(f"[d] trying email {email}", file=sys.stderr)
            magic_single(email, retry=retry, debug=debug)
            time.sleep(wait_time)


if __name__ == "__main__":
    banner = """
    HaveIBeenPwned API Magic - Quick and dirty [v0.2]
                                            by cjcase
    """
    parser = argparse.ArgumentParser(description=banner)

    parser.add_argument('--apikey', help="API Key, leave blank to use default", default="")
    parser.add_argument('--retry', help="Retry query with delay if request limit is reached", action="store_true", default=False)
    parser.add_argument('--debug', action="store_true", default=False)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Process a bunch of emails from file, newline separated pls")
    group.add_argument("--email", help="Process a single email instead")
    group.add_argument("--info", help="Print information about related breaches (comma separated)", type=str)
    
    args = parser.parse_args()

    print(banner, file=sys.stderr)
    print("[*] warming up the tubes...", file=sys.stderr)

    if args.file:
        print("[*] parsing file", file=sys.stderr)
        breaches, _ = magic(args.file, retry=args.retry, debug=args.debug)
    elif args.email:
        magic_single(args.email, retry=args.retry, debug=args.debug)
    elif args.info:
        print("[*] fetching info about breaches", file=sys.stderr)
        for name in args.info.split(','):
            r = magic_request(name, "info")
            import json
            print(json.dumps(r, indent=2), file=sys.stderr)
