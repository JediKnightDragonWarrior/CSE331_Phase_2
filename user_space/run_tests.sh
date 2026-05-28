#!/bin/bash
# CSE331 Phase 2 - Automated Test Runner
#
# BEFORE running this script, start the test processes once:
#
#   Terminal 1:  su - u1   then:  ./u1p1 &
#   Terminal 2:  su - u2   then:  ./u2p1 & ./u2p2 &
#
# Then run this script from /home/cse331:
#   chmod +x run_tests.sh && ./run_tests.sh

SAMPLES=100      # samples per repetition (top -n)
DELAY=1          # seconds between samples (top -d)
REPETITIONS=10   # repetitions per scheduler (M)
TEST_N=1         # test case number

REQUIRED_PROCS="u1p1 u2p1 u2p2"
SWITCH_CMD="./test_syscall"

# ---------------------------------------------------------------
check_processes() {
    echo "[*] Checking test processes are running..."
    local missing=0
    for proc in $REQUIRED_PROCS; do
        if ! pgrep -x "$proc" > /dev/null 2>&1; then
            echo "    [!] NOT running: $proc"
            missing=1
        else
            echo "    [OK] running: $proc (pid=$(pgrep -x $proc))"
        fi
    done
    if [ $missing -eq 1 ]; then
        echo ""
        echo "ERROR: Start the missing processes first:"
        echo "  Terminal 1: su - u1  then  ./u1p1 &"
        echo "  Terminal 2: su - u2  then  ./u2p1 & ./u2p2 &"
        exit 1
    fi
    echo ""
}

collect() {
    local sched_name=$1   # "default" or "fairshare"
    local sched_flag=$2   # 1 or 2

    echo "================================================"
    echo " Collecting: $sched_name scheduler"
    echo "================================================"

    $SWITCH_CMD $sched_flag
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not switch scheduler to flag $sched_flag"
        exit 1
    fi
    echo "[*] Switched to $sched_name (flag=$sched_flag)"
    sleep 2   # let scheduler settle

    for m in $(seq 1 $REPETITIONS); do
        local outfile="${sched_name}N${TEST_N}test${m}.txt"
        echo -n "    Repetition $m/$REPETITIONS -> $outfile ... "
        top -n $SAMPLES -d $DELAY -b > "$outfile"
        local lines=$(grep -cE "u1p1|u2p1|u2p2" "$outfile" 2>/dev/null || echo 0)
        echo "done ($lines process samples captured)"
    done

    echo ""
}

# ---------------------------------------------------------------
check_processes

collect "defaultsched" 1
collect "custom"       2

# Always end with default scheduler
$SWITCH_CMD 1
echo "[*] Restored default scheduler."
echo ""

# ---------------------------------------------------------------
echo "================================================"
echo " Running MSE analysis..."
echo "================================================"
python calculate_mse.py defaultsched   $TEST_N $REPETITIONS
echo ""
python calculate_mse.py custom $TEST_N $REPETITIONS
