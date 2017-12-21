#!/usr/bin/env python
# encoding: utf-8
import csv

from ds_wanalyser.ds_parser.ds_event import Event
from ds_wanalyser.ds_parser.ds_encounter import Encounter


class Parser:
    def __init__(self, file):
        self.file = open(file, 'r', encoding='utf-8')
        self.csv_reader = csv.reader(self.file)

        self.encounters = {}
        self.in_encounter = False
        self.encounter_id = '000000000'

    def parse(self):
        for row in self.csv_reader:
            event = Event(row)
            data = event.return_data()
            if event.is_encounter():
                if self.in_encounter and event.is_encounter() == 'end':
                    self.in_encounter = False
                    print(self.encounters[self.encounter_id].get_events_info())
                elif not self.in_encounter and event.is_encounter() == 'start':
                    self.in_encounter = True
                    self.encounter_id = data['encounter_id']
                    self.encounters[self.encounter_id] = Encounter(self.encounter_id)

            if self.in_encounter == True:
                self.encounters[self.encounter_id].add_event(data)

    def get_reports(self):
        return self.encounters
