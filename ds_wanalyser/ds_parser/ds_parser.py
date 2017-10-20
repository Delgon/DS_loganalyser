import csv


class Report:
    def __init__(self):
        self.encounter = []


class Encounter:
    def __init__(self):
        self.encounterid = 0


list_event_unknow_a_gerer = ['COMBAT_LOG_VERSION', 'CHALLENGE_MODE_END', 'CHALLENGE_MODE_START',
                             'COMBATANT_INFO', 'SPELL_HEAL_ABSORBED']

_DEFAULT_SPELLINFO_RESOURCE_AMOUNTDAMAGE = ['RANGE_DAMAGE', 'DAMAGE_SPLIT', 'SPELL_DAMAGE', 'SPELL_PERIODIC_DAMAGE']
_DEFAULT_SPELLINFO_RESOURCE_AMOUNTHEAL = ['SPELL_PERIODIC_HEAL', 'SPELL_HEAL']
_DEFAULT_SPELLINFO_RESOURCE_AMOUNTDRAIN = ['SPELL_DRAIN']
_DEFAULT_SPELLINFO_RESOURCE_AMOUNT = ['SPELL_PERIODIC_ENERGIZE', 'SPELL_ENERGIZE']
_DEFAULT_SPELLINFO_RESOURCE = ['SPELL_CAST_SUCCESS'] + _DEFAULT_SPELLINFO_RESOURCE_AMOUNT \
                              + _DEFAULT_SPELLINFO_RESOURCE_AMOUNTDRAIN + _DEFAULT_SPELLINFO_RESOURCE_AMOUNTHEAL \
                              + _DEFAULT_SPELLINFO_RESOURCE_AMOUNTDAMAGE

_DEFAULT_SPELLINFO_MISSTYPE = ['SPELL_MISSED', 'SPELL_PERIODIC_MISSED', 'RANGE_MISSED']

_DEFAULT_SPELLINFO_EXTRASPELL_AURATYPE = ['SPELL_DISPEL', 'SPELL_STOLEN', 'SPELL_AURA_BROKEN_SPELL']
_DEFAULT_SPELLINFO_EXTRASPELL = ['SPELL_INTERRUPT'] + _DEFAULT_SPELLINFO_EXTRASPELL_AURATYPE

_DEFAULT_SPELLINFO_AURATYPE_EFFECTS = ['SPELL_AURA_REMOVED_DOSE', 'SPELL_AURA_APPLIED_DOSE',
                                       'SPELL_AURA_APPLIED', 'SPELL_AURA_REFRESH', 'SPELL_AURA_REMOVED',
                                       'SPELL_AURA_BROKEN']
_DEFAULT_SPELLINFO_FAILEDTYPE = ['SPELL_CAST_FAILED']
_DEFAULT_SPELLINFO_ABSORB = ['SPELL_ABSORBED']  # si sourceGUID == 'Player-xxxxxx'
_DEFAULT_SPELLINFO = ['SPELL_CAST_START', 'SPELL_SUMMON', 'SPELL_CREATE', 'SPELL_INSTAKILL', 'SPELL_RESURRECT'] \
                     + _DEFAULT_SPELLINFO_ABSORB + _DEFAULT_SPELLINFO_FAILEDTYPE + _DEFAULT_SPELLINFO_AURATYPE_EFFECTS \
                     + _DEFAULT_SPELLINFO_EXTRASPELL + _DEFAULT_SPELLINFO_MISSTYPE + _DEFAULT_SPELLINFO_RESOURCE

_DEFAULT_RESOURCE_ENV_AMOUNTDAMAGE = ['ENVIRONMENTAL_DAMAGE']
_DEFAULT_RESOURCE_AMOUNTDAMAGE = ['SWING_DAMAGE', 'SWING_DAMAGE_LANDED']
_DEFAULT_RESOURCE = _DEFAULT_RESOURCE_AMOUNTDAMAGE + _DEFAULT_RESOURCE_ENV_AMOUNTDAMAGE

_DEFAULT_ABSORB = ['SPELL_ABSORBED']
_DEFAULT_MISSTYPE = ['SWING_MISSED']
_DEFAULT_SPELLNAME = ['ENCHANT_APPLIED', 'ENCHANT_REMOVED']
_DEFAULT = ['UNIT_DIED', 'PARTY_KILL', 'UNIT_DESTROYED'] + _DEFAULT_SPELLNAME + _DEFAULT_RESOURCE + _DEFAULT_MISSTYPE \
           + _DEFAULT_ABSORB + _DEFAULT_SPELLINFO

_ENCOUNTER_END = ['ENCOUNTER_END']
_ENCOUNTER = ['ENCOUNTER_START'] + _ENCOUNTER_END

list_event = list_event_unknow_a_gerer + _ENCOUNTER + _DEFAULT


class Event:
    def __init__(self, row):
        self.row = row
        self.event_data = {
            'timestamp': self.row[0].split('  ')[0],
            'event': self.row[0].split('  ')[1]
        }

        self.encounter_type = False
        if self.event_data['event'] in list_event:
            if self.event_data['event'] in _ENCOUNTER:
                self.event_encounter()
            elif self.event_data['event'] in _DEFAULT:
                self.event_default()
                if self.event_data['event'] in _DEFAULT_SPELLNAME:
                    self.event_spell_name()
                elif self.event_data['event'] in _DEFAULT_MISSTYPE:
                    self.event_miss_type(9)
                elif self.event_data['event'] in [_DEFAULT_ABSORB, _DEFAULT_SPELLINFO_ABSORB]:
                    if self.event_data['sourceGUID'].startswith('Player'):
                        self.event_spell_info()
                        self.event_absorb(12)
                    else:
                        self.event_absorb(9)
                elif self.event_data['event'] in _DEFAULT_RESOURCE:
                    self.event_resource(9)
                    if self.event_data['event'] in _DEFAULT_RESOURCE_AMOUNTDAMAGE:
                        self.event_amount_damage(22)
                    elif self.event_data['event'] in _DEFAULT_RESOURCE_ENV_AMOUNTDAMAGE:
                        self.event_environment(22)
                        self.event_amount_damage(23)
                elif self.event_data['event'] in _DEFAULT_SPELLINFO:
                    self.event_spell_info()
                    if self.event_data['event'] in _DEFAULT_SPELLINFO_FAILEDTYPE:
                        self.event_failed_type(12)
                    elif self.event_data['event'] in _DEFAULT_SPELLINFO_AURATYPE_EFFECTS:
                        self.event_aura_type(12)
                        self.event_effects(13)
                    elif self.event_data['event'] in _DEFAULT_SPELLINFO_MISSTYPE:
                        self.event_miss_type(12)
                    elif self.event_data['event'] in _DEFAULT_SPELLINFO_EXTRASPELL:
                        self.event_extra_spell(12)
                        if self.event_data['event'] in _DEFAULT_SPELLINFO_EXTRASPELL_AURATYPE:
                            self.event_aura_type(16)
                    elif self.event_data['event'] in _DEFAULT_SPELLINFO_RESOURCE:
                        self.event_resource(12)
                        if self.event_data['event'] in _DEFAULT_SPELLINFO_RESOURCE_AMOUNT:
                            self.event_amount(25)
                        elif self.event_data['event'] in _DEFAULT_SPELLINFO_RESOURCE_AMOUNTDRAIN:
                            self.event_amount_drain(25)
                        elif self.event_data['event'] in _DEFAULT_SPELLINFO_RESOURCE_AMOUNTDAMAGE:
                            self.event_amount_damage(25)
        else:
            print('Event inconnu : %s', self.row)

    def return_data(self):
        return self.event_data

    def event_absorb(self, index):
        self.event_data['absorbGUID'] = self.row[index]
        self.event_data['absorbName'] = self.row[index + 1]
        self.event_data['absorbFlags'] = self.row[index + 2]
        self.event_data['absorbRaidFlags'] = self.row[index + 3]
        self.event_data['absorbSpellId'] = self.row[index + 4]
        self.event_data['absorbSpellSchool'] = self.row[index + 5]
        self.event_data['amount'] = self.row[index + 6]

    def event_amount(self, index):
        self.event_data['amount'] = self.row[index]
        self.event_data['powerType'] = self.row[index + 1]

    def event_amount_damage(self, index):
        self.event_data['amount'] = self.row[index]
        self.event_data['overkill'] = self.row[index + 1]
        self.event_data['school'] = self.row[index + 2]
        self.event_data['resisted'] = self.row[index + 3]
        self.event_data['blocked'] = self.row[index + 4]
        self.event_data['absorbed'] = self.row[index + 5]
        self.event_data['critical'] = self.row[index + 6]
        self.event_data['glancing'] = self.row[index + 7]
        self.event_data['crushing'] = self.row[index + 8]

    def event_amount_drain(self, index):
        self.event_data['amount'] = self.row[index]
        self.event_data['powerType'] = self.row[index + 1]
        self.event_data['extraAmount'] = self.row[index + 2]

    def event_amount_heal(self, index):
        self.event_data['amount'] = self.row[index]
        self.event_data['overheal'] = self.row[index + 1]
        self.event_data['absorbed'] = self.row[index + 2]
        self.event_data['critical'] = self.row[index + 3]

    def event_aura_type(self, index):
        self.event_data['auraType']: self.row[index]

    def event_default(self):
        self.event_data['sourceGUID'] = self.row[1]
        self.event_data['sourceName'] = self.row[2]
        self.event_data['sourceFlags'] = self.row[3]
        self.event_data['sourceRaidFlags'] = self.row[4]
        self.event_data['destGUID'] = self.row[5]
        self.event_data['destName'] = self.row[6]
        self.event_data['destFlags'] = self.row[7]
        self.event_data['destRaidFlags'] = self.row[8]

    def event_effects(self, index):
        self.event_data['effects'] = self.row[index:]

    def event_encounter(self):
        if self.event_data['event'] == 'ENCOUNTER_START':
            self.encounter_type = 'start'
            self.event_data['encounter_id'] = self.row[1]
            self.event_data['encounter_name'] = self.row[2]
            self.event_data['difficulty_id'] = self.row[3]
            self.event_data['raidSize'] = self.row[4]
            print('Démarrage du combat (id: %s) contre %s en difficulté %s en %s joueur(s)'
                  % (self.event_data['encounter_id'],
                     self.event_data['encounter_name'],
                     self.event_data['difficulty_id'],
                     self.event_data['raidSize']))
        elif self.event_data['event'] == 'ENCOUNTER_END':
            self.encounter_type = 'end'
            self.event_data['encounter_id'] = self.row[1]
            self.event_data['encounter_name'] = self.row[2]
            self.event_data['difficulty_id'] = self.row[3]
            self.event_data['raidSize'] = self.row[4]
            self.event_data['endStatus'] = self.row[5]
            print('Fin du combat (id: %s) contre %s en difficulté %s en %s joueur(s)'
                  % (self.event_data['encounter_id'],
                     self.event_data['encounter_name'],
                     self.event_data['difficulty_id'],
                     self.event_data['raidSize']))

    def event_environment(self, index):
        self.event_data['environmentalType'] = self.row[index]

    def event_extra_spell(self, index):
        self.event_data['extraSpellId'] = self.row[index]
        self.event_data['extraSpellName'] = self.row[index + 1]
        self.event_data['extraSchool'] = self.row[index + 2]

    def event_failed_type(self, index):
        self.event_data['failedType'] = self.row[index]

    def event_miss_type(self, index):
        self.event_data['missType'] = self.row[index]
        self.event_data['isOffhand'] = self.row[index + 1]
        try:
            self.event_data['amountMissed'] = self.row[index + 2]
        except IndexError:
            self.event_data['amountMissed'] = 0

    def event_resource(self, index):
        self.event_data['resourceActor'] = self.row[index]
        self.event_data['resourceActorUnknown'] = self.row[index + 1]
        self.event_data['hitPoints'] = self.row[index + 2]
        self.event_data['maxHitPoints'] = self.row[index + 3]
        self.event_data['attackPower'] = self.row[index + 4]
        self.event_data['spellPower'] = self.row[index + 5]
        self.event_data['resolve'] = self.row[index + 6]
        self.event_data['resourceType'] = self.row[index + 7]
        self.event_data['resourceAmount'] = self.row[index + 8]
        self.event_data['maxResourceAmount'] = self.row[index + 9]
        self.event_data['xPosition'] = self.row[index + 10]
        self.event_data['yPosition'] = self.row[index + 11]
        self.event_data['itemLevel'] = self.row[index + 12]

    def event_spell_info(self):
        self.event_data['spellID'] = self.row[9]
        self.event_data['spellName'] = self.row[10]
        self.event_data['spellSchool'] = self.row[11]

    def event_spell_name(self):
        self.event_data['spellName'] = self.row[9]
        self.event_data['itemId'] = self.row[10]
        self.event_data['itemName'] = self.row[11]

    def is_encounter(self):
        if self.encounter_type == 'start':
            return 'start'
        elif self.encounter_type == 'end':
            return 'end'
        else:
            return False


class Parser:
    def __init__(self, file):
        self.file = open(file, 'r', encoding='utf-8')
        self.csv_reader = csv.reader(self.file)

        self.reports = []
        self.in_encounter = False

    def parse(self):
        for row in self.csv_reader:
            event = Event(row)
            if event.is_encounter():
                if self.in_encounter and event.is_encounter() == 'end':
                    self.in_encounter = False
                elif not self.in_encounter and event.is_encounter() == 'start':
                    self.in_encounter = True

    def get_reports(self):
        return self.reports
