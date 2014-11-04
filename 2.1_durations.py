#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

PREFIX = '2.1-20140929114702-results'

for i in range(1, 17):
    j = json.loads(open('%s-%d.json' % (PREFIX, i)).read())
    print '\n\nResults %d:' % (i)
    duration = 0
    for d in j:
        try:
            duration += d['stats']['duration']
            print '%s: %d' % (d['stats']['application'], d['stats']['duration'] / 60000)
        except:
            pass
    print 'Total duration: %d' % (duration / 60000)

