import time
from datetime import * 

p = datetime(2004,2,2,12,23,34)
r = p + timedelta(seconds = 12)
p=p.time()
r=r.time()
if r>=p:
    print type(r)