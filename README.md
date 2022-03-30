# hibp_magic.py

HaveIBeenPwned API Magic - Quick and dirty HIBP API v3 interface
  
This script is a quick and dirty tool for consuming the Have I Been Pwned API from the terminal.
You will need a HIBP API Key, [get yours here.](https://haveibeenpwned.com/API/Key)
This script is based on the V3 API Documentation, [you can check that here.](https://haveibeenpwned.com/API/v3).
Feel free to send pull requests, issues or functionality ideas :)

## Requirements

The script heavily relies on the python Requests library for POST and GET REST API interfacing.
```text
pip install requests
```

## Usage

```text
usage: hibp_magic.py [-h] [--apikey APIKEY] [--retry] [--debug] (--file FILE | --email EMAIL | --info INFO)

options:
-h, --help       show this help message and exit
--apikey APIKEY  API Key, leave blank to use default
--retry          Retry query with delay if request limit is reached
--debug
operation:
--file FILE      Process a bunch of emails from file, newline separated pls
--email EMAIL    Process a single email instead
--info INFO      Print information about related breaches (comma separated)
```

## License

[http://www.gnu.org/licenses/gpl-3.0.html](http://www.gnu.org/licenses/gpl-3.0.html)

```text
    hibp_magic - Quick and dirty HaveIBeenPwned API v3 interface
    Copyright (C) 2022 cjcase

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/
```

