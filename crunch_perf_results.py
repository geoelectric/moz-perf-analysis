#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import glob
import json
from math import sqrt
import re
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from scipy.stats import norm, t


VC = 'startup > moz-app-visually-complete'


def add_application_to_results(results, app_result_set,
                               app_pattern=None, test_pattern=None,
                               first_repetition=None, last_repetition=None):
    app_name = app_result_set['stats']['application'].strip()
    if app_pattern and not re.search(app_pattern, app_name):
        return

    if not app_result_set.get('passes'):
        return

    app_results = results.get(app_name, {})

    tests_added = 0
    for test_result_set in app_result_set['passes']:
        if add_test_to_results(app_results, test_result_set, test_pattern,
                               first_repetition, last_repetition):
            tests_added += 1

    if tests_added > 0:
        results[app_name] = app_results


def add_test_to_results(app_results, test_result_set,
                        test_pattern=None,
                        first_repetition=None, last_repetition=None):
    test_name = test_result_set['title'].strip()
    if test_pattern and not re.search(test_pattern, test_name):
        return False

    if not test_result_set.get('mozPerfDurations'):
        return False

    test_results = app_results.get(test_name, {'durations': []})

    # TODO: use slices
    durations_added = 0
    for index, duration in enumerate(test_result_set['mozPerfDurations'],
                                     start=1):
        if first_repetition and index < first_repetition:
            continue
        if last_repetition and index > last_repetition:
            break
        test_results['durations'].append(duration)
        durations_added += 1

    if durations_added:
        app_results[test_name] = test_results
        return True
    else:
        return False


def add_result_set(result_set, results,
                   app_pattern=None, test_pattern=None,
                   first_repetition=None, last_repetition=None):
    for app_result_set in result_set:
        add_application_to_results(results, app_result_set,
                                   app_pattern, test_pattern,
                                   first_repetition, last_repetition)


def get_stats(values, intervals=True):
    stats = {}

    values_array = np.array(values, dtype=np.float64)

    stats['min'] = np.asscalar(np.amin(values_array))
    stats['max'] = np.asscalar(np.amax(values_array))
    stats['mean'] = np.asscalar(np.mean(values_array))
    stats['median'] = np.asscalar(np.median(values_array))

    if values_array.size > 1:
        stats['std_dev'] = np.asscalar(np.std(values_array, ddof=1))
    else:
        stats['std_dev'] = 0

    if intervals:
        stats['intervals'] = []
        loc = stats['mean']
        scale = stats['std_dev'] / sqrt(values_array.size)

        for alpha in (.95, .99, .90, .85, .80, .50):
            if values_array.size > 30:
                interval = norm.interval(alpha, loc=loc, scale=scale)
            else:
                interval = t.interval(alpha, values_array.size - 1, loc, scale)
            stats['intervals'].append(
                {'confidence': alpha, 'interval': interval})

    return stats


def add_stats_to_results(results):
    for app in results:
        for test in results[app]:
            stats = get_stats(results[app][test]['durations'])
            results[app][test]['stats'] = stats


def add_stats_to_pivot(pivot):
    for app in pivot:
        for test in pivot[app]:
            for stat in pivot[app][test]:
                stats = get_stats(pivot[app][test][stat]['values'],
                                  intervals=True)
                pivot[app][test][stat]['stats'] = stats


def add_stats_pivot_to_crunched_results(crunched_results):
    # pivot -> app -> test -> stat[]
    pivot = {}
    for run_num, run_results in enumerate(crunched_results['runs']):
        # print 'Run %d:' % (run_num)
        for app in run_results:
            if app not in pivot:
                pivot[app] = {}

            for test in run_results[app]:
                if test not in pivot[app]:
                    pivot[app][test] = {}

                for stat in run_results[app][test]['stats']:
                    if stat == 'intervals':
                        continue
                    if stat not in pivot[app][test]:
                        pivot[app][test][stat] = {'values': []}

                    pivot[app][test][stat]['values'].append(
                        run_results[app][test]['stats'][stat])

                    # print '  Added %s.%s.%s' % (app, test, stat)

    add_stats_to_pivot(pivot)
    crunched_results['pivot'] = pivot


def crunch_result_sets(result_sets, app_pattern=None, test_pattern=None,
                       first_repetition=None, last_repetition=None):
    crunched_results = {'args': {'app_pattern': app_pattern,
                                 'test_pattern': test_pattern,
                                 'first_repetition': first_repetition,
                                 'last_repetition': last_repetition},
                        'combined': {},
                        'runs': []}

    if app_pattern:
        app_pattern = re.compile(app_pattern, re.IGNORECASE)
    if test_pattern:
        test_pattern = re.compile(test_pattern, re.IGNORECASE)

    for result_set in result_sets:
        results = {}
        add_result_set(result_set, results, app_pattern, test_pattern,
                       first_repetition, last_repetition)
        add_stats_to_results(results)
        crunched_results['runs'].append(results)

        # TODO: make it so it aggregates the last call instead
        add_result_set(result_set, crunched_results['combined'], app_pattern,
                       test_pattern, first_repetition, last_repetition)
    add_stats_to_results(crunched_results['combined'])

    add_stats_pivot_to_crunched_results(crunched_results)

    return crunched_results


def load_result_sets(filenames):
    if isinstance(filenames, basestring):
        filenames = glob.glob(filenames)

    result_sets = []
    for filename in filenames:
        with open(filename) as f:
            results = f.read()
            try:
                result_sets.append(json.loads(results))
            except Exception as e:
                sys.stderr.write('Discarding %s: %s\n' % (filename, str(e)))
    return result_sets


def load_and_crunch_result_sets(filenames, app_pattern=None, test_pattern=None,
                                first_repetition=None, last_repetition=None):
    rs = load_result_sets(filenames)
    return crunch_result_sets(rs, app_pattern, test_pattern, first_repetition, last_repetition)


def plot_app_vc(cr, app, test=VC, stat='mean'):
    loc = plticker.MultipleLocator(base=1.0)
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(loc)
    plt.xlabel('Runs')
    plt.ylabel('Time in ms')
    plt.title('%s, %s, individual %ss vs. %d-count 95%% CI' %
              (app, test, stat, len(cr['combined'][app][VC]['durations'])))

    csi_95 = cr['combined'][app][VC]['stats']['intervals'][0]['interval']
    print csi_95
    ymin = csi_95[0]
    ymax = csi_95[1]
    plt.axhspan(ymin, ymax, facecolor='green')
    plt.plot(cr['pivot'][app][VC][stat]['values'], 'k-o')
    plt.show()
    return plt.gcf()


def plot_results(cr, app, test=VC, run=0):
    loc = plticker.MultipleLocator(base=1.0)
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(loc)
    plt.xlabel('Repetitions')
    plt.ylabel('Time in ms')
    plt.title('%s, %s, %d' % (app, test, run))
    plt.plot(cr['runs'][run][app][VC]['durations'], 'k-o')
    plt.show()
    return plt.gcf()


def main():
    parser = argparse.ArgumentParser(
        description='Get aggregated results for one or more result files')
    parser.add_argument('filenames',
                        metavar='FILE',
                        help='Result file to process', nargs='+')
    parser.add_argument('-a', '--app-pattern',
                        metavar='PATTERN',
                        help='Only include applications whose names contain ' +
                             'this regex (case insensitive)')
    parser.add_argument('-t', '--test-pattern',
                        metavar='PATTERN',
                        help='Only include tests whose names contain this ' +
                             'regex (case insensitive)')
    parser.add_argument('-f', '--first-repetition',
                        metavar='INDEX',
                        help='Only consider results at/after this ' +
                             'repetition (1-based)',
                        type=int)
    parser.add_argument('-l', '--last-repetition',
                        metavar='INDEX',
                        help='Only consider results at/before this ' +
                             'repetition (1-based)',
                        type=int)
    args = parser.parse_args()

    result_sets = load_result_sets(args.filenames)
    combined_results = crunch_result_sets(result_sets, args.app_pattern,
                                          args.test_pattern,
                                          args.first_repetition,
                                          args.last_repetition)
    print json.dumps(combined_results, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
