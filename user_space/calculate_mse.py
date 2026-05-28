#!/usr/bin/env python
# CSE331 Phase 2 - MSE Calculator (Python 2.3 compatible)
#
# Usage:
#   python calculate_mse.py <defaultsched|custom> <test_N> <repetitions_M>
#
# Example:
#   python calculate_mse.py defaultsched   1 10
#   python calculate_mse.py custom 1 10

import sys
import os
import math

# ---------------------------------------------------------------
# Test Case 1: u1(1 proc), u2(2 procs) -> 3 total processes
#   Default:    each process gets 1/3 = 33.33%
#   Fair Share: u1 gets 50% (1 user, 1 proc)
#               u2 gets 50% split by 2 procs = 25% each
# ---------------------------------------------------------------
TEST_CASES = {
    1: {
        "processes": ["u1p1", "u2p1", "u2p2"],
        "expected": {
            "defaultsched":   {"u1p1": 33.33, "u2p1": 33.33, "u2p2": 33.33},
            "custom": {"u1p1": 50.00, "u2p1": 25.00, "u2p2": 25.00},
        }
    },
}


def parse_top_file(filepath, process_names):
    # Linux 2.4 top -b column layout:
    # PID USER PRI NI SIZE RSS SHARE STAT %CPU %MEM TIME COMMAND
    #  0   1    2   3   4   5    6    7    8    9   10    11
    samples = {}
    for name in process_names:
        samples[name] = []

    f = open(filepath, "r")
    for line in f:
        parts = line.split()
        if len(parts) < 9:
            continue
        cmd = parts[-1]
        if cmd in process_names:
            try:
                cpu = float(parts[8])
                samples[cmd].append(cpu)
            except (ValueError, IndexError):
                pass
    f.close()
    return samples


def calc_mse(observed, predicted):
    if not observed:
        return None
    total = 0.0
    for y in observed:
        total += (y - predicted) ** 2
    return total / len(observed)


def mean(lst):
    return sum(lst) / float(len(lst))


def analyze(scheduler, test_n, repetitions):
    if test_n not in TEST_CASES:
        print "Unknown test case: %d" % test_n
        sys.exit(1)

    tc       = TEST_CASES[test_n]
    procs    = tc["processes"]
    expected = tc["expected"][scheduler]

    print "=" * 58
    print "Scheduler : %s" % scheduler.upper()
    print "Test case : %d" % test_n
    exp_str = "  ".join("%s=%.1f%%" % (p, expected[p]) for p in procs)
    print "Expected  : %s" % exp_str
    print "=" * 58

    session_mses = []
    missing = []

    for m in range(1, repetitions + 1):
        fname = "%sN%dtest%d.txt" % (scheduler, test_n, m)
        if not os.path.exists(fname):
            missing.append(fname)
            continue

        samples   = parse_top_file(fname, procs)
        proc_mses = []

        print "\nSession %2d  (%s)" % (m, fname)
        print "  %-8s %6s %8s %10s %10s" % ("Process", "n", "mean%", "predicted%", "MSE")
        print "  " + "-" * 46

        for proc in procs:
            obs = samples[proc]
            if not obs:
                print "  %-8s  no samples found" % proc
                continue
            pred = expected[proc]
            err  = calc_mse(obs, pred)
            proc_mses.append(err)
            print "  %-8s %6d %8.2f %10.2f %10.4f" % (
                proc, len(obs), mean(obs), pred, err)

        if proc_mses:
            avg = mean(proc_mses)
            session_mses.append(avg)
            print "  %-8s %6s %8s %10s %10.4f  <-- session avg" % (
                "AVG", "", "", "", avg)

    if missing:
        print "\n[!] Missing files (skipped): %s" % ", ".join(missing)

    print "\n" + "=" * 58
    if session_mses:
        overall = mean(session_mses)
        rmse    = math.sqrt(overall)
        print "Sessions analyzed : %d" % len(session_mses)
        print "Overall MSE       : %.4f" % overall
        print "RMSE              : %.4f  (+/- %.2f%% avg error)" % (rmse, rmse)
    else:
        print "No data to analyze. Run run_tests.sh first."
    print "=" * 58
    print ""


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: python calculate_mse.py <defaultsched|custom> <test_N> <repetitions_M>"
        sys.exit(1)

    sched = sys.argv[1]
    n     = int(sys.argv[2])
    m     = int(sys.argv[3])

    if sched not in ("defaultsched", "custom"):
        print "Scheduler must be 'defaultsched' or 'custom'"
        sys.exit(1)

    analyze(sched, n, m)
