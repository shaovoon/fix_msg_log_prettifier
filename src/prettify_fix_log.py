#!/usr/bin/python

import string
import sys
import getopt
import datetime
import xml.etree.ElementTree as ET

def parse_xml(file, dict, msg_dict):
    print "Parsing file: %s" % file
    tree = ET.parse(file)
    root = tree.getroot()
    fields = root.findall("fields")[0].findall('field')
    for field in fields:
        dict[int(field.attrib['number'])] = field.attrib['name']
    msgs = root.findall("messages")[0].findall('message')
    for msg in msgs:
        msg_dict[msg.attrib['msgtype']] = msg.attrib['name']

def prettify(src_file, dest_file, dict, msg_dict):
    with open(dest_file, 'wb') as fo:
        with open(src_file, 'rb') as f:
            line_num = 0
            while True:
                line_num+=1
                s = f.readline()
                if len(s) == 0: break
                columns = s.split(chr(1))
                for column in columns:
                    values = column.split('=')
                    if len(values) > 1:
                        try:
                            key = int(values[0])
                            tag_name = dict[key]
                            if key == 35:
                                try:
                                    msg_name = msg_dict[values[1]]
                                    fo.write("%s(%d)=%s(%s)|" % (tag_name, key, msg_name, values[1]))
                                except KeyError:
                                    print("msg_name KeyError: %d, value: %s, line_num: %d: tag 35 do not have %s msg listed" % (key, values[1], line_num, values[1]))
                                    fo.write("%s(%d)=%s|" % (tag_name, key, values[1]))
                            else:
                                fo.write("%s(%d)=%s|" % (tag_name, key, values[1]))
                        except ValueError:
                            fo.write("%s|" % column)
                        except KeyError:
                            fo.write("%s=%s|" % (values[0], values[1]))
                            print("tag_name KeyError: %d, value: %s, line_num: %d" % (key, values[1], line_num))
                fo.write("\n")

def usage():
    print "Usage: prettify_fix_log.py [-h] <path to FIXT11.xml> <path to FIX50SP2.xml> <src log file> <output prettified log file>"
    print "Option -h: display usage"

# python prettify_fix_log.py FIXT11.xml FIX50SP2.xml log.txt log2.txt

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", [])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    for option in opts:
        if option[0] == '-h':
            usage()
            sys.exit(2)

    if len(args) < 4:
        print "Not enough arguments.\n"
        usage()
        sys.exit(2)

dict = {}
msg_dict = {}

xml_file1 = args[0]
xml_file2 = args[1]
src_log = args[2]
output_log = args[3]

parse_xml(xml_file1, dict, msg_dict)
parse_xml(xml_file2, dict, msg_dict)
prettify(src_log, output_log, dict, msg_dict)