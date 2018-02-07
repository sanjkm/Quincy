#!/bin/bash
rm Quincy_invoices.csv
python add_monthly_invoices.py
echo "Current invoice file attached. Regards, Sanjay" | mutt -s "Quincy invoice file" \
taylor@liquiditybook.com scottie@mtcqs.com -a Quincy_invoices.csv
