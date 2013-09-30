'''
Created on Sep 29, 2013

@author: aaponte
'''

if __name__ == '__main__':
    pass

import sc2reader
from sc2reader.engine.plugins import SelectionTracker, APMTracker

sc2reader.engine.register_plugin(APMTracker())
replay = sc2reader.load_replay('MyReplay.SC2Replay', load_map=True)

tracker = APMTracker()

for human in replay.humans:
    print("The APM for", human, "is", human.avg_apm, " ")
    print("The EPM for", human, "is", human.avg_epm, " ")
    print("The SPM for", human, "is", human.avg_spm, " ")
    
