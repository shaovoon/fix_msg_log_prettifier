# Python Script to Prettify FIX Protocol Message Logs

The Financial Information eXchange (FIX) protocol is an electronic communications protocol initiated in 1992 for international real-time exchange of information related to the securities transactions and markets. The message fields are delimited using the ASCII 01 `<start of header>` character. They are composed of a header, a body, and a trailer. Example of a FIX message: (Pipe character is used to represent SOH character.)

```
8=FIX.4.2|9=178|35=8|<snipped>
```

The key in the key/value pair (separated by `=`) is represented by a number which can be decoded using dictionary XML for easier reading. This Python 2.7 script can replace the numeric key with the actual field name and also replace the numeric `enum` value with actual `enum` description. It is tested with FIX Protocol 5.0 SP2. The script requires at least 3 parameters.

```
python prettify_fix_log.py [-h][-e] <src log file> <output prettified log file> 
<path to FIX50SP2.xml> <path to FIXT11.xml>
Option -h: display usage
Option -e: convert enum to description
```

[Financial Information eXchange - Wikipedia](https://en.wikipedia.org/wiki/Financial_Information_eXchange)


