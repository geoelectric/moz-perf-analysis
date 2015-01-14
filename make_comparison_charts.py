#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

import matplotlib.pyplot as plt
import numpy as np

import crunch_perf_results as c


R1_NAME_DEFAULT = '2.1'
R2_NAME_DEFAULT = '2.2'


def draw(app_name, r1, r2, label1, label2, show=True, save=False, save_prefix=''):
    def draw_chart(r, label, color):
        try:
            cr = r['combined'][app_name][c.VC]
            med = cr['stats']['median']
            p = np.percentile(cr['durations'], 95)
            plt.hist(cr['durations'], 32, label='%s (med=%d, p95=%d)' % (
                label, med, p), alpha=.25, color=color)
            plt.xlabel('ms')
            plt.ylabel('# results')
            plt.axvline(x=med, color=color, linewidth=2, linestyle='-')
            plt.axvline(x=p, color=color, linewidth=2, linestyle='--')
        except:
            pass
    
    plt.title(app_name)
    draw_chart(r1, label1, 'blue')
    draw_chart(r2, label2, 'red')
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


def compare(r1_name=R1_NAME_DEFAULT, r2_name=R2_NAME_DEFAULT,
            show=True, save=False, save_prefix=None):
    if save_prefix is None:
        save_prefix = r2_name

    r1 = c.load_and_crunch_result_sets(
        r1_name + '*json', test_pattern=c.VC, first_repetition=2)
    r2 = c.load_and_crunch_result_sets(
        r2_name + '*json', test_pattern=c.VC, first_repetition=2)

    label1 = r1_name.split('-')[0]
    label2 = r2_name.split('-')[0]

    for app_name in get_app_names(r1, r2):
        try:
            print '%s %s: %d data points' % (
                  label1, app_name, len(r1['combined'][app_name][c.VC]['durations']))
        except:
            pass
        try:
            print '%s %s: %d data points' % (
                  label2, app_name, len(r2['combined'][app_name][c.VC]['durations']))
        except:
            pass
        draw(app_name, r1, r2, label1, label2, show, save, save_prefix)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        r1_name = sys.argv[1]
    else:
        r1_name = R1_NAME_DEFAULT

    if len(sys.argv) > 2:
        r2_name = sys.argv[2]
    else:
        r2_name = R2_NAME_DEFAULT

    if len(sys.argv) > 3:
        save_prefix = sys.argv[3]
    else:
        save_prefix = None

    compare(r1_name, r2_name, show=False, save=True, save_prefix=save_prefix)

