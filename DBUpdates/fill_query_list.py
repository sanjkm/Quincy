# fill_query_list.py
# Lists the query conditions for all queries to be executed

# 2/15/2018
# Queries to generate record deletion
# Opens the inputted file which contains full query parameters on each line
# The specifics of each query are collated, put into a dictionary, and each
# dictionary is appended to query_list, which is returned

def fill_query_list (filename):
    delim1, delim2 = ';', ','
    query_list = []
    with open(filename, 'r') as f:
        for line in f:
            query_dict = {}
            conditions = (line.strip()).split(delim1)
            for query in conditions:
                field, value = query.split(delim2)
                query_dict[field] = value
            query_list.append(query_dict)
    f.close()

    return query_list
