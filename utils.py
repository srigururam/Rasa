from difflib import SequenceMatcher

import stardog

conn_details = {
    'endpoint': 'http://localhost:5820',
    'username': 'admin',
    'password': 'admin'
}

approved_string_list = ["Customer", "units", "maximum", "minimum", "rep_contacted", "total_approved_claims_count",
                        "total_rejected_claims_count"]

synonyms_json = \
    {
        "Customer": {"Doctor"},
        "units": {"Sales"},
        "maximum": {"max", "most", "greatest", "largest"},
        "minimum": {"min", "lowest", "least"},
        "rep_contacted": {"has been contacted by rep", "contacted rep"},
        "total_approved_claims_count": {"total claims approved", "total approved claims", "approved claims"},
        "total_rejected_claims_count": {"total claims rejected", "total rejected claims", "rejected claims"}
    }


def approved_string_finder(entity_string, isName=False):
    """

    :param isName:
    :param entity_string:
    :return:
    """
    try:
        for each_approved_string in approved_string_list:
            # initialise
            max_value_1 = 0
            approved_candidate_1 = ""
            max_value_2 = 0
            approved_candidate_2 = ""

            # process
            match_indicator = SequenceMatcher(None, each_approved_string, entity_string).ratio()
            print(each_approved_string, entity_string, match_indicator)
            if match_indicator > max_value_1:
                max_value_1 = match_indicator
                approved_candidate_1 = each_approved_string
            if match_indicator > 0.75:
                return each_approved_string

            # If matching is insufficient
            for each_string in synonyms_json:
                for each_synonym in synonyms_json[each_string]:
                    match_indicator_2 = SequenceMatcher(None, each_synonym, entity_string).ratio()
                    print(each_synonym, entity_string, match_indicator_2)
                    if match_indicator_2 > max_value_2:
                        max_value_2 = match_indicator_2
                        approved_candidate_2 = each_string
                    if match_indicator_2 > 0.75:
                        return each_string

            # When nothing is returned
            if max_value_1 > max_value_2 and max_value_1 > 0.5:
                return approved_candidate_1
            elif max_value_2 > max_value_1 and max_value_2 > 0.5:
                return approved_candidate_2
    except Exception:
        raise Exception


def get_list_of_names():
    """

    :return:
    """
    try:
        with stardog.Connection('customer_360_closed', **conn_details) as conn:
            customer_name_query = "select ?name where\
                                {\
                                ?cust_id :full_name ?name\
                                }"
            results = conn.select(customer_name_query)
            list_of_names = []
            for each in results['results']['bindings']:
                list_of_names.append(each['name']['value'])
            return list_of_names

    except Exception:
        raise Exception


def approved_name_string_finder(name):
    """

    :param name:
    :return:
    """
    try:
        name_list = get_list_of_names()
        # print("name_list", name_list)
        max_value = 0
        max_matched_string = ""
        for each_name_in_list in name_list:
            match_indicator = SequenceMatcher(None, each_name_in_list, name).ratio()
            # print(name , each_name_in_list, match_indicator)
            if match_indicator > max_value:
                max_value = match_indicator
                max_matched_string = each_name_in_list
            if match_indicator > 0.75:
                return each_name_in_list
        print(name, max_matched_string, max_value)
        return max_matched_string
    except Exception:
        raise Exception


def get_id_for_customer_name(name):
    try:
        with stardog.Connection('customer_360_closed', **conn_details) as conn:
            query = "select ?cust_id where\
                    {\
                    ?cust_id :full_name \"" + name + "\"\
                    }"
            print("#######\n"+query+"\n")
            results = conn.select(query)
            print("get_id",results)
            return_string = results['results']['bindings'][0]['cust_id']['value']
            return_string = return_string.split("/")[-1]
            return return_string
    except Exception:
        raise Exception
