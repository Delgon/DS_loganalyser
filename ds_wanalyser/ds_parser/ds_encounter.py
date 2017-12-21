#!/usr/bin/env python
# encoding: utf-8


class Encounter:
    def __init__(self, id):
        self.encounterid = 0
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def get_events_info(self):
        return 'Infos sur les données : %s event dans le combat' % self.events.__len__()