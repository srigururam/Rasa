import stardog
import json
import random
import string

try:
    conn_details = {
        'endpoint': 'http://localhost:5820',
        'username': 'admin',
        'password': 'admin'
    }
    def get_query_depth(a,b):
        with stardog.Connection('customer_360_closed', **conn_details) as conn:
            # a = input("Find: ")
            # b = input("with: ")
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
            bool_result = False
            query_depth = 0
            initial_query = '?s rdf:type :' + a + '.\n ' \
                                                  '?s :' + b + ' ?' + rand + '.\n'
            while bool_result is False and query_depth<20:
                # print(initial_query)
                execute_string = "ask where {" + initial_query + "}"
                print("Execute String\n", execute_string)
                bool_result = conn.ask(execute_string)
                print(bool_result)
                if not bool_result:
                    query_depth += 1
                    random_rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
                    if b in initial_query:
                        print("B is in initial query")
                        initial_query = str(initial_query).replace(':'+b, '?' + random_rand)
                    new_rand = random_rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                    additional_query = '\n?' + rand + ' :' + b + ' ?' + new_rand+'.'
                    print("Additional Query", additional_query)
                    initial_query = initial_query + additional_query
                    print('############## Query Appended ###################')
                    print(initial_query)
                    execute_string = "ask where {" + initial_query + "}"
                    print("Execute String2\n", execute_string)
                    bool_result = conn.ask(execute_string)
                    rand = new_rand
                else:
                    break

        # print(initial_query)
            print(bool_result)
            print(query_depth)
        return query_depth

except:
    raise
