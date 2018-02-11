#!/bin/bash
rm current_unpaid_invoices.csv 
rm unpaid_invoice_summary.csv
# python move_paid_csv.py
python format_paid_csv.py
python update_paid_invoices.py
echo "Unpaid invoice file attached. Regards, Sanjay" | mutt -s "Quincy unpaid invoice file" \
taylor@liquiditybook.com scottie@mtcqs.com -c sanjay.menon@gmail.com \
-a unpaid_invoice_summary.csv
