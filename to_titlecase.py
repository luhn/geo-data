import sys
import csv

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        print 'Usage: to_titlecase.py in.csv'
        sys.exit(0)

    with open(args[1]) as fh:
        reader = csv.reader(fh)
        writer = csv.writer(sys.stdout)
        for row in reader:
            row[1] = row[1].title()
            writer.writerow(row)

