import docker
import base64
import os
from io import BytesIO
import shutil
from lxml import etree
import re
import base64
import json
import requests
import zlib

class PkaHelper:

    def __init__(self, container_name="hi8", image_name="jaja:3.0.0"):

        self.work_dir = os.getcwd()+"\\files"
        try:
            os.makedirs("files")
        except:
            pass
        do_native = os.name=="nt"
        if(not do_native):
            try:
                self.client = docker.from_env()
                self.container = self._get_or_create_container(container_name, image_name)
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Alert")
                msg.setText("Can't work nativly, need docker to work, make sure docker is installed and the deamon is running")
                msg.setIcon(QMessageBox.Information)
                msg.addButton(QMessageBox.Ok)
                msg.exec()

            if(self.container.status != "running"):
                self.container.start()
        

    def _get_or_create_container(self, container_name, image_name):
        random = str(random.randint(0, 1000000))
        container_name = "pkahelper"+random
       # if not self.client.images.list(image_name):
        #    self.client.images.build(path="pka2xmldocker/.", tag=image_name)

        volumes = {self.work_dir: {'bind': "/workspace/files", 'mode': 'rw'}}

        if not self.client.containers.list(all=True, filters={"name": container_name}):
            return self.client.containers.run(
                "quentinn42/pka2xml",
                name=container_name,
                detach=True,
                tty=True,
                stdin_open=True,
                volumes=volumes,
            )

        return self.client.containers.get(container_name)

    def _pka2xml(self, url, source,result, mode,fp=None,native=False):
        if not native:
            self.container.start()
        if mode == "-d":
            shutil.copy(url,(self.work_dir+"\\"+source))
        else:
            with open(self.work_dir+"\\"+source, 'wb') as f: 
                f.write(url)
        print("is native: "+str(native))
        if native:
            import sys
            p = ""
            if hasattr(sys, '_MEIPASS'):
                p = sys._MEIPASS
            else:
                p = os.getcwd()
            os.system(f"{p}\\PkaHelper.exe {mode} files/{source} files/{result}")
        else:
            self.container.exec_run(f"pka2xml {mode} files/{source} files/{result}",tty=True)
        
        if mode == "-d":
            with open(self.work_dir+"\\"+result, 'rb') as f: 
                return f.read()
        if mode == "-e":
            shutil.copy(self.work_dir+"\\"+result, fp)

           
        
    def _pka2xmlInMemory(self, data, source,result, mode):
        self.container.start()
        
        with open(self.work_dir+"\\"+source, 'wb') as f: 
            f.write(data)

        self.container.exec_run(f"pka2xml {mode} files/{source} files/{result}",tty=True)

        with open(self.work_dir+"\\"+result, 'rb') as f: 
            return f.read()
            

    def decrypt(self, data_binary:str,fileEnding:str):
        xml_unfiltered = None
        do_native = os.name=="nt"
        xml_unfiltered = self._pka2xml(data_binary, f"file.{fileEnding}", "decrypted.xml", "-d",None,do_native).decode("utf-8")
        rew_text,self.rep = self.extract_from_text(xml_unfiltered, r'<ACTIVITY .*>', '<ACTIVITY>')
        return etree.fromstring(rew_text)

    def encrypt(self, xml_data:str, fileEnding:str,fp):
        xml = self.insert_into_text(xml_data, r'<ACTIVITY>', self.rep)
        do_native = os.name=="nt"
        return self._pka2xml(xml[0].encode(), "decrypted.xml", f"file.{(fileEnding.split('.')[-1])}", "-e",fp,do_native)
        
    def extract_from_text(self,text, pattern, replacement):
        def replacer(match):
            replaced.append(match.group(0))
            return replacement

        replaced = []
        new_text = re.sub(pattern, replacer, text)
        return new_text, replaced

    def insert_into_text(self,text, pattern, replacement):
        def replacer(match):
            replaced.append(match.group(0))
            r = replacement.pop(0)
            return r

        replaced = []
        new_text = re.sub(pattern, replacer, text)
        return new_text, replaced

    def to_base64(self,file):
        with open(file, 'rb') as f:
            encoded = base64.b64encode(f.read())
            return encoded.decode('utf-8')

    def b64_to_blob(self,base64, type='application/octet-stream'):
        base64_bytes = base64.encode('utf-8')
        blob = base64_bytes.decode('base64')
        return blob

    def load_file(self,file):
        with open(file, 'r') as f:
            content = f.read()
            return content

  


def load_bytes_from_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
      
def save_bytes_to_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)
