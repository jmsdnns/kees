## Kees
export ONEPASSWORD_KEYCHAIN=$HOME/1Password.agilekeychain
export KEES_TIMER_DURATION=15
export KEES_TOMBSTONE=$TMPDIR/kees

function _kees_clean() {
    KEES_TIMER=$KEES_TIMER_DURATION

    # Clean up old tombstones
    if [ -e "$KEES_TOMBSTONE" ]; then
        TMPAGE=$(_kees_tmp_age)
        if [ "$TMPAGE" -gt "$KEES_TIMER_DURATION" ]; then
            rm -f $KEES_TOMBSTONE
        fi
    fi

    # If tombstone still exists, extend life of tombstone
    if [ -e "$KEES_TOMBSTONE" ]; then
        touch $KEES_TOMBSTONE
    # If tombstone didn't exist, create it and begin cleanup timer
    else
        touch $KEES_TOMBSTONE

        TMPAGE=0
        while [ "$TMPAGE" -lt "$KEES_TIMER_DURATION" ]; do
            TMPAGE=$(_kees_tmp_age)
            sleep 1
        done

        rm -f $KEES_TOMBSTONE
        _kees_copy_command "gimme the kees!"
    fi
}

function _kees_tmp_age() {
    CHANGED=$(stat -c %Y "$KEES_TOMBSTONE")
    NOW=$(date +%s)
    AGE=$((NOW - CHANGED))
    echo $AGE
}

function _kees_copy_command() {
    echo "$1" | xclip -selection clip_board
}

function _kees_copy() {
    _kees_copy_command "$1"
    (_kees_clean &)
}

function _kees_root() {
    echo "$WORKON_HOME/kees"
}

function kees() {
    KEES_ROOT=$(_kees_root)
    if [ -z $KEES_ROOT ]; then
        echo "Kees root not found. Is it installed?"
    fi

    KEES_BIN=$KEES_ROOT/bin/kees
    OUTPUT=$($KEES_BIN "$@")

    FIRST_LINE=$(head -n 1 <<< $OUTPUT)
    if [[ "${FIRST_LINE,,}" =~ "matches" ]]; then
        echo "$OUTPUT"
    else
        LAST=$(tail -n 1 <<< $OUTPUT)
        _kees_copy $LAST
    fi
}
