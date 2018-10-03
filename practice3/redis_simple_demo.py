import redis
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# set
# r.set('foo','bar')
# get
# foo =  r.get('foo')
# print(foo)

# Append - not exist -> create
# r.append('foo','abcdef')
# r.append('fop','abc')

# Delete
# r.delete('foo')

# Execute command
# ret = r.execute_command('keys','*')
# print(ret)

# check key exist
# check = r.exists('foo')
# print(check)

# delete key after time
# r.set('foo','abc')
# r.expire('foo',5)
# print(r.get('foo'))
# time.sleep(6)
# print(r.get('foo'))
