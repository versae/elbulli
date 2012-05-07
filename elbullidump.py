#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import cgi
import csv
import codecs
import cStringIO
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Taken from http://docs.python.org/library/csv.html#csv-examples
class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Main(object):

    def __init__(self, *args, **kwargs):
        parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS,
                                         description='Path to data files.')
        parser.add_argument('--path', help='Path')
        args = parser.parse_args()
        if not args.path:
            root_dir = sys.argv[1]
        else:
            root_dir = args.path
            if not os.path.isdir(args.path):
                root_dir = os.path.join(PROJECT_ROOT, args.path)
        file_list = []
        file_size = 0
        folder_count = 0
#        print("Root: {0}".format(root_dir))
        writer = UnicodeWriter(sys.stdout)
        headers = set()
        for root, sub_folders, files in os.walk(root_dir):
            folder_count += len(sub_folders)
            for file_name in files:
                if file_name.endswith(".dat"):
                    f = os.path.join(root, file_name)
                    f_data = codecs.open(f, "r", "utf-8-sig")
                    file_lines = f_data.readlines()
                    f_data.close()
                    data = "".join(file_lines)
                    data = data.replace("\r\n", "").replace("\n", "")
                    folder_headers = self.get_headers(file_name, data)
                    headers = headers.union(folder_headers)
                    file_size = file_size + os.path.getsize(f)
                    file_list.append(f)
        headers = list(headers)
        headers.sort()
#        print headers
        writer.writerow(headers)
        for root, sub_folders, files in os.walk(root_dir):
            folder_count += len(sub_folders)
            for file_name in files:
                if file_name.endswith(".dat"):
                    f = os.path.join(root, file_name)
                    f_data = codecs.open(f, "r", "utf-8-sig")
                    file_lines = f_data.readlines()
                    f_data.close()
                    data = "".join(file_lines)
                    data = data.replace("\r\n", "").replace("\n", "")
                    rows = self.get_data_rows(file_name, data, headers)
                    writer.writerows(rows)
                    file_size = file_size + os.path.getsize(f)
                    file_list.append(f)

#        print("Total Size: {0} bytes".format(file_size))
#        print("Total Files: {0}".format(len(file_list)))
#        print("Total Folders: {0}".format(folder_count))

    def get_headers(self, file_name, data):
        query = cgi.parse_qs(data)
        headers = set()
        for key, values in query.iteritems():
            # [100, 999]
            if key[-3:].isdigit():
                prop_name = key[:-3]
            # [10, 99)
            elif key[-2:].isdigit():
                prop_name = key[:-2]
            # [0, 9]
            elif key[-1:].isdigit():
                prop_name = key[:-1]
            else:
                prop_name = key
            headers.add(prop_name)
        return headers

    def get_data_rows(self, file_name, data, headers=None):
        query = cgi.parse_qs(data)
        items = {}
        common_props = {}
        for key, values in query.iteritems():
            prop_id = None
            # [100, 999]
            if key[-3:].isdigit():
                prop_id = key[-3:]
                prop_name = key[:-3]
            # [10, 99)
            elif key[-2:].isdigit():
                prop_id = key[-2:]
                prop_name = key[:-2]
            # [0, 9]
            elif key[-1:].isdigit():
                prop_id = key[-1:]
                prop_name = key[:-1]
            prop_value = u"".join(values)
            if prop_id:
                if prop_id not in items:
                    items[prop_id] = {}
                items[prop_id].update({prop_name: prop_value})
            else:
                common_props[key] = prop_value
        for key, value in items.iteritems():
            items[key].update(common_props)
        rows = []
        if items and not headers:
            headers = items.values()[0]
            rows.append(headers.keys())
        headers_len = len(headers)
        for value_dict in items.values():
            row = [u""] * headers_len
            for i, header in enumerate(headers):
                if header in value_dict:
                    row[i] = value_dict[header]
            rows.append(row)
        return rows


if __name__ == "__main__":
    Main()
