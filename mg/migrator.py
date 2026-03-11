from .connexion import dbConnect
from .utils import getArgumentParser, migratorInfoDir
import os

class migrator:
    
    def __init__(self, config):
        self.config = config
        self.con = dbConnect(config['database'])
        self.info = self.migratorInfo()
    
    def run(self):
        print("run")
        
    def migratorInfo(self):
        path = self.config["path"]["migrator"]
        lsdir = os.listdir(path)        
        
        infoDir = [migratorInfoDir(fl) for fl in lsdir]
        
        return infoDir
    
    def execute(self, path, cursor):        
        script = self.getScript(path)

        if script:
            cursor.execute(script)
            self.con.commit()
            cursor.close()
        else:
            print("Aucune requête SQL à exécuter.")


    def getScript(self, path):
        with open(path, "r") as f:
            lines = f.readlines()

        # enlever les commentaires
        sql_lines = [line for line in lines if not line.strip().startswith("--")]

        return "".join(sql_lines).strip()
    
    def exit(self):
        self.con.close()
        