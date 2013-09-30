# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division

from collections import defaultdict


class APMTracker(object):
    """
    Builds ``player.aps`` and ``player.apm`` dictionaries where an action is
    any Selection, ControlGroup, or Ability event.

    Also provides ``player.avg_apm`` which is defined as the sum of all the
    above actions divided by the number of seconds played by the player (not
    necessarily the whole game) multiplied by 60.

    APM is 0 for games under 1 minute in length.
    """
    name = 'APMTracker'

    def handleInitGame(self, event, replay):
        for human in replay.humans:
            human.apm = defaultdict(int) #actions per minute
            human.aps = defaultdict(int) #actions per second
            human.epm = defaultdict(int) #effective actions per minte
            human.eps = defaultdict(int) #effective actions per second
            human.spm = defaultdict(int) #spam actions per minute
            human.sps = defaultdict(int) #spam actions per second
            human.ipm = defaultdict(int) #ineffective actions per minute
            human.ips = defaultdict(int) #inneffective actions per second
            human.last_event = event;   #The most recent action event
            human.seconds_played = replay.length.seconds

    def handleControlGroupEvent(self, event, replay):
        event.player.aps[event.second] += 1
        event.player.apm[int(event.second/60)] += 1
        if event.player.last_event == event:
            event.player.sps[event.second] += 1
            event.player.spm[int(event.second/60)] += 1
        else:
            event.player.last_event = event
            event.player.eps[event.second] += 1
            event.player.epm[int(event.second/60)] += 1

    def handleSelectionEvent(self, event, replay):
        event.player.aps[event.second] += 1
        event.player.apm[int(event.second/60)] += 1
        if event.player.last_event == event:
            event.player.sps[event.second] += 1
            event.player.spm[int(event.second/60)] += 1
        else:
            event.player.last_event = event
            event.player.eps[event.second] += 1
            event.player.epm[int(event.second/60)] += 1

    def handleAbilityEvent(self, event, replay):
        event.player.aps[event.second] += 1
        event.player.apm[int(event.second/60)] += 1
        if event.player.last_event == event:
            event.player.sps[event.second] += 1
            event.player.spm[int(event.second/60)] += 1
        else:
            event.player.last_event = event
            event.player.eps[event.second] += 1
            event.player.epm[int(event.second/60)] += 1

    def handlePlayerLeaveEvent(self, event, replay):
        event.player.seconds_played = event.second

    def handleEndGame(self, event, replay):
        for human in replay.humans:
            if len(human.apm.keys()) > 0:
                human.avg_apm = sum(human.aps.values())/float(human.seconds_played)*60
            else:
                human.avg_apm = 0
                
            if len(human.epm.keys()) > 0:
                human.avg_epm = sum(human.eps.values())/float(human.seconds_played)*60
            else:
                human.avg_epm = 0
                
            if len(human.spm.keys()) > 0:
                human.avg_spm = sum(human.sps.values())/float(human.seconds_played)*60
            else:
                human.avg_spm = 0
                
            if len(human.ipm.keys()) > 0:
                human.avg_ipm = sum(human.ips.values())/float(human.seconds_played)*60
            else:
                human.avg_ipm = 0
                    
