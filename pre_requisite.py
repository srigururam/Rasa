import stardog
import os

conn_details = {
    'endpoint': 'http://localhost:5820',
    'username': 'admin',
    'password': 'admin'
}
with stardog.Connection('customer_360_closed', **conn_details) as conn:
    customer_name_query = "select ?name where\
                        {\
                        ?cust_id :full_name ?name\
                        }"
    results = conn.select(customer_name_query)
    write_string = ""
    list_of_names = []
    for each in results['results']['bindings']:
        write_string = write_string + each['name']['value'] + "\n"
        list_of_names.append(each['name']['value'])
    print(write_string)

    name_file_path = os.path.realpath(os.curdir)+"/data/lookup_tables/name.txt"
    f= open(name_file_path, "w+")
    f.write(write_string)
    f.close()

    nlu_file_path = os.path.realpath(os.curdir)+"/data/nlu.md"
    print("path_name",nlu_file_path)
    # nlu_file_path = "C:/Users/gurus/Documents/rasa/data/nlu.md"
    f1 = open(nlu_file_path, "a+")
    f1.write("## intent:user_defined\n")
    for each_name in list_of_names:
        training_sentence_string = "- Find number of [approved claims](attributes) of ["+each_name+"](name)\n"
        f1.write(training_sentence_string)
    f1.close()
