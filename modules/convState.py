#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class convState:
    def __init__(self):
        self.DEBUG = False
        self.midiTempo = 120
        self.midiResolution = 480
        self.samples = 0

    def getMidiTempo(self):
        return(self.midiTempo)
    
    def setMidiTempo(self, tempo):
        self.midiTempo = tempo

    def getMidiResolution(self):
        return(self.midiResolution)
    
    def setMidiResolution(self, resolution):
        self.midiResolution = resolution

    def getSamples(self):
        return(self.samples)
    
    def setSamples(self, samples):
        self.samples = samples

    def addSamples(self, samples):
        self.samples += samples

    def getDebug(self):
        return self.DEBUG

    def setDebug(self, debug):
        self.DEBUG = debug


def main():
    pass


if __name__ == "__main__":
    main()
