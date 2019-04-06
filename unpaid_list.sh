#!/bin/bash
read -p "Did you click on the Win7 directory? Won't work if not."
rm current_unpaid_invoices.csv 
rm unpaid_invoice_summary.csv
rm /home/smenon/Desktop/Windows-Share/LB_paid.csv
python move_paid_csv.py
python format_paid_csv.py
python update_paid_invoices.py
echo "Unpaid invoice summary attached. Regards, Sanjay" | mutt -s "Quincy unpaid invoice summary" \
mohammad@liquiditybook.com scottie@mtcqs.com -c sanjay.menon@gmail.com \
-a unpaid_invoice_summary.csv
echo "Unpaid invoice line item file attached. Regards, Sanjay" | mutt -s "Quincy unpaid invoice file" \
mohammad@liquiditybook.com scottie@mtcqs.com -c sanjay.menon@gmail.com \
-a current_unpaid_invoices.csv
