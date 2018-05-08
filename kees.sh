## Kees
export ONEPASSWORD_KEYCHAIN=$HOME/Dropbox/jmsdnns/1Password.agilekeychain
export KEES_TIMER_DURATION=15
export KEES_TOMBSTONE=$TMPDIR/kees

function _kees_clean() {
    KEES_TIMER=$KEES_TIMER_DURATION

    if [ -e "$KEES_TOMBSTONE" ]; then
        touch $KEES_TOMBSTONE
    else
        touch $KEES_TOMBSTONE
    TMPAGE=0

    while [ "$TMPAGE" -lt "$KEES_TIMER_DURATION" ]; do
        TMPAGE=$(_kees_tmp_age)
        echo $BASHPID     $KEES_TIMER >> word
        echo "  -$TMPAGE" >> word
        sleep 1
    done

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
    command pushd "$HOME/Projects/kees" > /dev/null
    KEES_VENV=$(pipenv --venv)
    command popd > /dev/null
    echo "$KEES_VENV"
}

function kees() {
    KEES_ROOT=$(_kees_root)
    if [ -z $KEES_ROOT ]; then
    echo "Kees root not found. Is it installed?"
    fi

    KEES_BIN=$KEES_ROOT/bin/kees
    PASSWORD=$($KEES_BIN "$@")
    _kees_copy $PASSWORD
}