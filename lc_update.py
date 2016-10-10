#!/usr/bin/python

import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
import urllib
import json
import os

class UpdateEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--tab', action = 'store',
                                     type = 'string', dest = 'what')

    def effect(self):
        f = urllib.urlopen("https://api.github.com/repos/" + \
                           "renaultd/lasercut/git/refs/heads/master")
        j = json.load(f)
        inkex.debug("Most recent SHA : " + j["object"]["sha"])

effect = UpdateEffect()
effect.affect()
