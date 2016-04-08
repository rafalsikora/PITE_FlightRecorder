# This class defines the screen which displays
# flight path and parameters of the planes
# during the flight, recorded in black-box

import ROOT
import Coordinates
import array


class DataViewer:

    def __init__(self, data, size=0.5, bkgdfile="util/map.png"):
        self.flightdata = data
        self.numberofgraphs = len(data[0])-3  # assumed that there'are always phi and lambda
        self.scaleFactor = size
        self.mapImage = ROOT.TImage.Open(bkgdfile)
        self.canvasSize = [float(self.mapImage.GetWidth()), float(self.mapImage.GetHeight())]
        self.canvasSize = [int(self.scaleFactor*x) for x in self.canvasSize]
        self.canvasmap = None
        self.canvasgraphs = None
        self.flightpathgraph = None
        self.additionalgraphs = []
        self.createflightpathgraph()
        self.createadditionalgraphs()

    def start(self):
        # drawing canvas with a world and flight path
        self.canvasmap = ROOT.TCanvas("Map", "Map", self.canvasSize[0], self.canvasSize[1])
        self.mapImage.Draw("x")
        p = ROOT.TPad("p", "p", 0, 0, 1, 1)  # Create a transparent pad filling the full canvas
        p.SetFillStyle(4000), p.SetFrameFillStyle(4000)
        p.Draw(), p.cd()
        self.flightpathgraph.Draw("P")
        self.canvasmap.Print('flightPath.png')
        # drawing time dependence of the rest of parameters recorded during the flight
        self.canvasgraphs = ROOT.TCanvas("Parameters", "Parameters", 800, 600*self.numberofgraphs)
        self.canvasgraphs.Divide(1, self.numberofgraphs)
        for i in range(len(self.additionalgraphs)):
            self.canvasgraphs.cd(i+1)
            self.additionalgraphs[i].Draw("AP")
        self.canvasgraphs.Print('flightParameters.png')

    # this method creates graphs of black-box readouts vs. time
    def createadditionalgraphs(self):
        for i in self.flightdata[0].keys():
            if (i != "phi") and (i != "lambda") and (i != "time"):
                x = [el["time"] for el in self.flightdata]
                y = [el[i] for el in self.flightdata]
                graph = ROOT.TGraph(len(x), array.array('f', x), array.array('f', y))
                graph.SetTitle(i)
                graph.GetXaxis().SetTitle("Time [s]")
                self.additionalgraphs.append(graph)

    # this method creates graphs of flight path based on black-box readouts
    def createflightpathgraph(self):
        x = [Coordinates.xy((el["phi"], el["lambda"]))[0] for el in self.flightdata]
        y = [Coordinates.xy((el["phi"], el["lambda"]))[1] for el in self.flightdata]
        assert (len(x) == len(y))
        self.flightpathgraph = ROOT.TGraph(len(x), array.array('f', x), array.array('f', y))
        self.flightpathgraph.SetMarkerStyle(20)
        self.flightpathgraph.SetMarkerSize(0.3)
        self.flightpathgraph.SetMarkerColor(ROOT.kRed)
