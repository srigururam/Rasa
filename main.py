import stardog
import json
import play
import random
import string
import utils


conn_details = {
    'endpoint': 'http://localhost:5820',
    'username': 'admin',
    'password': 'admin'
}


def generate_query_and_fetch_results(subject, attribute, aggregate_boolean=False, aggregate_string=None):
    try:
        with stardog.Connection('customer_360_closed', **conn_details) as conn:
            a = subject
            b = attribute
            c = False
            filter = ""
            if c:
                d = input("Enter Filter: ")
                # e= input("Enter no. of results required: ")
                filter = "FILTER(?end" + d + " || regex(str(?end),\"" + d[1:] + "\", \"i\" ))"
                # filter = "FILTER(?end" + d + ")"

            order_by_string = ""
            if aggregate_boolean:
                if aggregate_string == 'maximum':
                    order_by_string = 'order by desc(?end) LIMIT 1'
            if aggregate_string == 'minimum':
                order_by_string = 'order by ?end LIMIT 1'
            query_depth = play.get_query_depth(a, b)
            query = 'PATHS START ?start {?start rdf:type :' + a + '.} END ?end VIA'
            via_query = '?start rdf:type :' + a + '.\n ' \
                                                  '?start :' + b + ' ?end.\n'
            if query_depth > 0:
                for i in range(0, query_depth):
                    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
                    rand_use = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
                    via_query = via_query.replace(':' + b, '?' + rand)
                    via_query = via_query.replace('?end', '?' + rand_use)
                    new_line = '?' + rand_use + ' :' + b + '?end.\n'
                    via_query = via_query + new_line
            via_query = via_query + filter
            query = query + '{' + via_query + '}'
            query = query + order_by_string
            print("############### FINAL ################")
            print(query)
            results = conn.paths(query)
            f = open("newfile", "w")
            f.write(str(results))

            return_list = []
            var_list = []
            for each_var in results['head']['vars']:
                if each_var not in var_list:
                    var_list.append(each_var)
            for each in results['results']['bindings']:
                if 'start' in each:
                    # print(each['start'])
                    two_query = 'select ?name where {:' + each['start']['value'].split('/')[-1] + ' rdf:type ?o.\n\
                    :' + each['start']['value'].split('/')[-1] + ' :full_name ?name.}'
                    # print(two_query)
                    r = conn.select(two_query)
                    # print(r)
                    if len(r['results']['bindings']) > 0 and 'name' in r['results']['bindings'][0]:
                        if r['results']['bindings'][0]['name']['value'] not in return_list:
                            return_list.append(r['results']['bindings'][0]['name']['value'].replace(",", ""))
            if len(return_list) == 1:
                return return_list[0]
            f = open("oldfile", "w")
            f.write(str(return_list))
        return str(return_list).replace("[", "").replace("]", "")
    except Exception:
        raise Exception


def generate_query_and_fetch_results_v1(subject, attribute, aggregate_boolean=False, aggregate_string=None, is_name = False):
    try:
        with stardog.Connection('customer_360_closed', **conn_details) as conn:
            a = subject
            b = attribute
            cust_id = utils.get_id_for_customer_name(subject)
            query_depth = play.get_query_depth(cust_id, attribute)
            print("depth", query_depth)
    except Exception:
        raise Exception