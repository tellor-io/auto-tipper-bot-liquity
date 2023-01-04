import datetime
# import csv

def write_to_report_file(*args):
    current_time = datetime.datetime.now()
    with open("simplereport.txt", "a") as f:
        f.write("file: " + str(args[0]) + "  time: " + str(current_time) + "\n")