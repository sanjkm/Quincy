# fill_query_list.py
# Lists the query conditions for all queries to be executed

# 2/15/2018
# Queries to generate record deletion for the beginning of 2018
# 1) BTIG-Conventus 2) DINO 3) RAJA
def fill_query_list ():
    query_list = []
    
    query_list.append({'Table':'line_item',
                  'BillingCode':"'BTIG'",
                       'Attributable':"'CONVENTUS'"})
    query_list.append({'Table':'invoices',
                       'BillingCode':"'BTIG'",
                       'Attributable':"'CONVENTUS'",
                       'Status':"'Unpaid'"})
            
    query_list.append({'Table':'line_item',
                       'BillingCode':"'DINO'"})
    query_list.append({'Table':'invoices',
                       'BillingCode':"'DINO'",
                       'YEAR(Invoice_Date)':'2018'})
    query_list.append({'Table':'line_item',
                       'BillingCode':"'RAJA'"})
    query_list.append({'Table':'invoices',
                       'BillingCode':"'RAJA'",
                       'Status':"'Unpaid'"})
    return query_list
