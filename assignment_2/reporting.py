import csv
from tabulate import tabulate  # pip3 install tabulate
import sys
from datetime import datetime


def create_report(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # ["Function Name", "Num. of Calls", "Total Time (ms)", "Average Time (ms)"]  # next(csv_reader)
        data = [row for row in csv_reader]
        # prepare and clean up data, such that it can be used for tabulate
        runtime_fun = {}
        called_fun = {}
        for line in data:
            runtime_fun[line[0]] = [line[1]]

        for line in data:
            runtime_fun[line[0]].append(line[3])

        for key in runtime_fun:
            fun_name = runtime_fun[key][0]
            called_fun[fun_name] = [0,0]

        for key in runtime_fun:
            fun_name = runtime_fun[key][0]
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            t1 = datetime.strptime(runtime_fun[key][1], date_format)
            t2 = datetime.strptime(runtime_fun[key][2], date_format)
            total_time = (t2 - t1).total_seconds() * 1000  # to get ms
            called_fun[fun_name][1] = total_time
            try:
                called_fun[fun_name][0] += 1
            except:
                called_fun[fun_name][0] = 1

        my_data = []
        for key in called_fun:
            times = called_fun[key][0]
            total_time = called_fun[key][1]
            my_data.append([key, times, total_time, round(total_time/times, 2)])

    my_header = ["Function Name", "Num. of Calls", "Total Time (ms)", "Average Time (ms)"]
    table = tabulate(my_data, my_header, tablefmt="github")
    return table


if __name__ == "__main__":
    # Use: python3 reporting.py trace_file.log
    assert len(sys.argv) == 2, "Usage: python3 reporting.py trace_file.log"
    print(create_report(sys.argv[1]))