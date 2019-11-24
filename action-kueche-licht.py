#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io
import websockets
from websocket import create_connection

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()
        
def msg_kueche_tisch_licht_an(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:00_0_005=1")
    ws.close()
    
    if len(intentMessage.slots.kueche_tisch_licht_an) > 0:
        house_room = intentMessage.kueche_tisch_licht_an.first().value # We extract the value from the slot "house_room"
        result_sentence = "Tisch Licht in {} angeschaltet".format(str(kueche_tisch_licht_an))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Kuechen Tisch Licht an"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    

def msg_kueche_tisch_licht_aus(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:00_0_005=0")
    ws.close()

    if len(intentMessage.slots.kueche_tisch_licht_aus) > 0:
        house_room = intentMessage.slots.kueche_tisch_licht_aus.first().value # We extract the value from the slot "house_room"
        result_sentence = "Tisch Licht in {} ausgeschaltet".format(str(kueche_tisch_licht_aus))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Kuechen Tisch Licht aus"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("cetax:kueche_tisch_licht_an", msg_kueche_tisch_licht_an)
        h.subscribe_intent("cetax:kueche_tisch_licht_aus", msg_kueche_tisch_licht_aus)
        h.start()
