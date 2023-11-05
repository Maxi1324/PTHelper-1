import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from lxml import etree

class Graph():
    def generate_graph(self,xml):
        
      

        G = nx.Graph()

        geraete, links = self.read_data(xml)
        G.add_nodes_from(geraete)

        verbindungen = links
        G.add_edges_from(verbindungen)

        fig, ax = plt.subplots()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_color='black', ax=ax)
        ax.axis('off')
        canvas = FigureCanvas(fig)
        return canvas


    def read_data(self,xml:etree):
        d = self.read_devices(xml)
        l = self.read_links(xml)

        devices = (self.deviceToLable(d[i]) for i in d)
        links = []
        for item in l:
            links.append((self.deviceToLable(d[item["to"]]), self.deviceToLable(d[item["fo"]])))

        return (devices,links)

    def deviceToLable(self,device):
        return device["name"]

    def read_devices(self,xml:etree):
        packettracer = xml.xpath("//PACKETTRACER5")[0]
        devices={}
        for e in packettracer.xpath("./NETWORK/DEVICES/DEVICE/ENGINE"):
            typ = e.xpath("./TYPE")[0].text
            if("Power Distribution Device" != typ):
                devices[e.xpath("./SAVE_REF_ID")[0].text] = {
                "name": e.xpath("./NAME")[0].text,
                "type": typ,
                }
        return devices

    def read_links(self,xml):
        packettracer = xml.xpath("//PACKETTRACER5")[0]
        Links = ({
            "to": i.xpath("./FROM")[0].text,
            "fo": i.xpath("./TO")[0].text,
        }
         for i in packettracer.xpath(".//LINKS/LINK/CABLE"))
        return (Links)