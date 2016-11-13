
import pprint , json
message = [ "a" , "12345" ]
pprint.pprint( message[0] )

"""
value = 'a'
data  = json.loads( message )
result = {
    'a': lambda x: int(x) * 5,
    'b': lambda x: x + 7,
    'c': lambda x: x - 2
}[value['a']]( 5 )
#(  )

"""