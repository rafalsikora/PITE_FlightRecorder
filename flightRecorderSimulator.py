#!/usr/bin/python
import MainWindow
import AirportsList


# reading list of airports from the file
airportstuple = AirportsList.readairportslist()

# running program main window (GUI)
MainWindow.open(airportstuple)
