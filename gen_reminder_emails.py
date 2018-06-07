# gen_reminder_emails.py
# Generates the monthly reminder emails to the LiquidityBook
# CFO to pay Quincy

import datetime


# num_init_lines is the number of lines before month_name is
# outputted
def genReminderEmail (template_name, output_name, num_init_lines, month_name):
    f_out = open(output_name, 'w')
    with open(template_name, 'r') as f_in:
        line_count = 0
        for line in f_in:
            line_count += 1
            if line_count != num_init_lines:
                f_out.write(line)
            else:
                mod_line = line.rstrip()
                f_out.write(mod_line + ' ' + month_name + ' ')
    f_out.close()
