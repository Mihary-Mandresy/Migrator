from .connexion import dbConnect
from .utils import getArgumentParser, migratorInfoDir
import os

class migrator:
    
    def __init__(self, config):
        self.config = config
        self.con = dbConnect(config['database'])
        self.info = self.migratorInfo()
        self.parser = getArgumentParser()
    
    def run(self):
        
        fileAction = ""
        if (self.parser.m):
            fileAction = "up"
            self.executeAction(fileAction)
        if (self.parser.r):
            fileAction = "down"
            self.executeAction(fileAction)
        if (self.parser.d):
            fileAction = "data"
            self.executeAction(fileAction)
            
        if not fileAction:
            raise Exception("Type d'action inconnue")
        
    def executeAction(self, fileAction):
        infoFiler = self.filtreInfo()

        cursor = self.con.cursor()
        
        for info in infoFiler:
            fileName = os.path.join(f"{info['pos']}_{info['date'].isoformat()}", fileAction + ".sql")
            try:
                filePath = os.path.join(self.config['path']['migrator'], fileName)
                if (os.path.exists(filePath)) :
                    self.execute(filePath, cursor)
                    print(fileName, "-"*15, "Succes")
    
            except Exception as e:
                print(fileName, "-"*15, "Error\n" + str(e))
        
        cursor.close()
                        
        
    def filtreInfo(self):
        withFilter = []
        count = 0
                
        for a in range(0, len(self.info)):
            if (count < self.parser.limite) :
                if (self.info[a]['pos'] >= self.parser.pos):
                    withFilter.append(self.info[a])
                count += 1
            else:
                break
        
        return withFilter
    
    def migratorInfo(self):
        path = self.config["path"]["migrator"]
        lsdir = os.listdir(path)
                            
        infoDir = [migratorInfoDir(fl) for fl in lsdir if "T" in fl]
        infoDir.sort(key=lambda x: x['date'])
        return infoDir
    
    def execute(self, path, cursor):        
        script = self.getScript(path)

        if script:
            cursor.execute(script)
            
        self.con.commit()

    def getScript(self, path):
        with open(path, "r") as f:
            lines = f.readlines()

        # enlever les commentaires
        sql_lines = [line for line in lines if not line.strip().startswith("--")]

        return "".join(sql_lines).strip()
    
    def exit(self):
        self.con.close()
        