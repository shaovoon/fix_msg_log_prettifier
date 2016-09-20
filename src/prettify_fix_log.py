#!/usr/bin/python

# Python Script to Prettify FIX Protocol Message Logs with Information
# ====================================================================
# Author: Wong Shao Voon
# Version 1.0.0 
# Copyright 2016
# No warranty implied or expressed

import string
import sys
import getopt
import datetime
import xml.etree.ElementTree as ET

def parse_xml(file, dict, msg_dict, field_enum_dict):
    print "Parsing file: %s" % file
    tree = ET.parse(file)
    root = tree.getroot()
    fields = root.findall("fields")[0].findall('field')
    for field in fields:
        dict[int(field.attrib['number'])] = field.attrib['name']
        values = field.findall("value")
        enum_dict = {}
        for value in values:
            enum_dict[value.attrib['enum']] = value.attrib['description']
        if len(enum_dict) > 0:
            field_enum_dict[int(field.attrib['number'])] = enum_dict
        
    msgs = root.findall("messages")[0].findall('message')
    for msg in msgs:
        msg_dict[msg.attrib['msgtype']] = msg.attrib['name']

def prettify(src_file, dest_file, dict, msg_dict, field_enum_dict, parse_enum):
    with open(dest_file, 'wb') as fo:
        with open(src_file, 'rb') as f:
            line_num = 0
            while True:
                line_num+=1
                s = f.readline()
                if len(s) == 0: break
                columns = s.split(chr(1))
                if len(columns) == 1:
                    columns = s.split('|')
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
                            elif parse_enum and field_enum_dict.has_key(key):
                                enum_dict = field_enum_dict[key]
                                if enum_dict.has_key(values[1]):
                                    fo.write("%s(%d)=%s(%s)|" % (tag_name, key, enum_dict[values[1]], values[1]))
                                else:
                                    fo.write("%s(%d)=%s|" % (tag_name, key, values[1]))
                                    print("enum KeyError: %d, value: %s, line_num: %d: tag %d does not have this enum value in dictionary: %s" % (key, values[1], line_num, key, values[1]))
                            else:
                                fo.write("%s(%d)=%s|" % (tag_name, key, values[1]))
                        except ValueError:
                            fo.write("%s|" % column)
                        except KeyError:
                            fo.write("%s=%s|" % (values[0], values[1]))
                            print("tag_name KeyError: %d, value: %s, line_num: %d" % (key, values[1], line_num))
                fo.write("\n")

def usage():
    print "Usage: prettify_fix_log.py [-h][-e] <src log file> <output prettified log file> <path to FIX50SP2.xml> <optional path to FIXT11.xml>"
    print "Option -h: display usage"
    print "Option -e: convert enum to description"

# python prettify_fix_log.py log.txt log2.txt FIX50SP2.xml FIXT11.xml

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he", [])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    parse_enum = False
    for option in opts:
        if option[0] == '-h':
            usage()
            sys.exit(2)
        if option[0] == '-e':
            parse_enum = True
            
    print("parse_enum:%s" % parse_enum)

    if len(args) < 3:
        print "Not enough arguments.\n"
        usage()
        sys.exit(2)

    dict = {}
    msg_dict = {}
    field_enum_dict = {}

    src_log = args[0]
    output_log = args[1]

    xml_file1 = args[2]
    parse_xml(xml_file1, dict, msg_dict, field_enum_dict)

    if len(args) == 4:
        xml_file2 = args[3]
        parse_xml(xml_file2, dict, msg_dict, field_enum_dict)
        
    prettify(src_log, output_log, dict, msg_dict, field_enum_dict, parse_enum)