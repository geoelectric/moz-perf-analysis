#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

import matplotlib.pyplot as plt
import numpy as np

import crunch_perf_results as c


R1_DATE_DEFAULT = '2014-10-31'
R2_DATE_DEFAULT = '2014-10-31'


def draw(app_name, r1, r2, show=True, save=False, save_prefix=''):
    plt.title(app_name)

    try:
        cr1 = r1['combined'][app_name][c.VC]
        med1 = cr1['stats']['median']
        p1 = np.percentile(cr1['durations'], 95)
        plt.hist(cr1['durations'], 32, label='2.0 (med=%d, p95=%d)' % (
                 med1, p1), alpha=.25, color='blue')
        plt.xlabel('ms')
        plt.ylabel('# results')
        plt.axvline(x=med1, color='blue', linewidth=2, linestyle='-')
        plt.axvline(x=p1, color='blue', linewidth=2, linestyle='--')
    except:
        pass

    try:
        cr2 = r2['combined'][app_name][c.VC]
        med2 = cr2['stats']['median']
        p2 = np.percentile(cr2['durations'], 95)
        plt.hist(cr2['durations'], 32, label='2.1 (med=%d, p95=%d)' % (
            med2, p2), alpha=.25, color='red')
        plt.xlabel('ms')
        plt.ylabel('# results')
        plt.axvline(x=med2, color='red', linewidth=2, linestyle='-')
        plt.axvline(x=p2, color='red', linewidth=2, linestyle='--')
    except:
        pass

    plt.legend()

    if save:
        if save_prefix != '':
            save_prefix = save_prefix + '_'
        plt.savefig((save_prefix + 'perf_' + app_name + '.png').replace('/', '_'))

    if show:
        plt.show()
    else:
        plt.close()


def get_app_names(r1, r2):
    names = r1['combined'].keys()
    names += r2['combined'].keys()
    names = list(set(names))
    names.sort()
    return names


def compare(r1_date=R1_DATE_DEFAULT, r2_date=R2_DATE_DEFAULT,
            show=True, save=False, save_prefix=None):
    if save_prefix is None:
        save_prefix = r2_date

    r1 = c.load_and_crunch_result_sets(
        '2.0-' + r1_date + '*json', test_pattern=c.VC, first_repetition=2)
    r2 = c.load_and_crunch_result_sets(
        '2.1-' + r2_date + '*json', test_pattern=c.VC, first_repetition=2)

    for name in get_app_names(r1, r2):
        try:
            print '2.0 %s: %d data points' % (name, len(r1['combined'][name][c.VC]['durations']))
        except:
            pass
        try:
            print '2.1 %s: %d data points' % (name, len(r2['combined'][name][c.VC]['durations']))
        except:
            pass
        draw(name, r1, r2, show, save, save_prefix)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        r1_date = sys.argv[1]
    else:
        r1_date = R1_DATE_DEFAULT

    if len(sys.argv) > 2:
        r2_date = sys.argv[2]
    else:
        r2_date = R2_DATE_DEFAULT

    compare(r1_date, r2_date, show=False, save=True)
