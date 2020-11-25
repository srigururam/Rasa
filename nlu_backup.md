import os
## intent:user_defined
- Show me the [customer](subject) who sold [maximum](aggregates) [units](attributes)
- Display the [customer](subject) with [minimum](aggregates) [units](attributes)
- Show all the [customers](subject)
- Display the [customer](subject) with [highest](aggregates) [sales](attributes)
- Display all [customer](subject) with [min](aggregates) [sales](attributes) 
- Find [doctors](subject) with [max](aggregates) [sales](attributes)
- Find [Customers](subject) who [has been contacted by rep](attributes)
- Find [doctors](subject) who [has been contacted by rep](attributes) at [maximum](aggregates)
- Find [Doctors](subject) with [lowest](aggregates) [approved claims](attributes)
- Show [Customers]{"entity": "subject"} with [least]{"entity":"aggregates"} [rejected claims]{"entity":"attributes"}
- Find [city](attributes) of [128 PEDIATRICS ASSOCIATES](name)
- Find number of [approved claims](attributes) of [BARNETT MEDICAL ASSOCIATES](name)

## lookup:subject
C:\Users\gurus\Documents\rasa\data\lookup_tables\subject.txt

## lookup:name
C:\Users\gurus\Documents\rasa\data\lookup_tables\name.txt

## lookup:attributes
C:\Users\gurus\Documents\rasa\data\lookup_tables\attributes.txt

## lookup:aggregates
C:\Users\gurus\Documents\rasa\data\lookup_tables\aggregates.txt
