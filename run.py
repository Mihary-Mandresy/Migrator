from mg.migrator import migrator
from mg.utils import getConfig

if __name__ == "__main__":
    m = migrator(config=getConfig())
    m.run()
    m.exit()
    
