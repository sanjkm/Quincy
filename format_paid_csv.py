# format_paid_csv.py
# Takes the csv of the paid line item file, and
# formats it such that the databases can update status
# Format change is changing the date in the first column to
# MySQL preferred yyyy-mm-dd
# New file saved in current directory

from datetime import datetime

def convert_date_format (curr_date_str):
    date_val = (datetime.strptime (curr_date_str, '%Y-%m-%d')).date()
    month_str = str(date_val.month)
    if len(month_str) == 1:
        month_str = '0' + month_str
    day_str = str(date_val.day)
    if len(day_str) == 1:
        day_str = '0' + day_str
    sep = '-'
    return (str(date_val.year) + sep + month_str + sep + day_str)


def gen_new_file (old_dir, new_dir, filename, separator):

    f_out = open (new_dir + filename, 'w')

    with open (old_dir + filename, 'r') as f:
        init_line = 1
        for line in f:
            x1 = line.rstrip()
            x_data = x1.split(separator)
            if init_line == 1:
                f_out.write (str(x_data[0]) + separator) # not a date
            else:
                f_out.write (convert_date_format(x_data[0]) + separator)
                    
            for vals in x_data[1:-1]:
                f_out.write (str(vals) + separator)
            f_out.write (str(x_data[-1]) + '\n')
            init_line = 0
        f_out.close()
    f.close()

def main():
    old_dir = "/home/smenon/Desktop/Windows-Share/"
    new_dir = "" # saving to this directory

    filename = "LB_paid.csv"
    separator = ','

    gen_new_file (old_dir, new_dir, filename, separator)

main()
    
