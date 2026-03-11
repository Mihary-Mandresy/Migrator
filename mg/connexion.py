import psycopg2

def dbConnect(config):
    return psycopg2.connect(dsn=makeDns(config))
        
def makeDns(obj : dict) :
    dns = ""
    all_items = obj.items()
    for key, value in all_items:
        dns += f"{key}={value} "
    return dns