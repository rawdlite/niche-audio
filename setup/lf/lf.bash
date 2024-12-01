export PLAYER=Moode
export OPENER=run-mailcap-rs

lfr () {
        PLAYER=RaspdacEvo lf
}

lfm () {
        cd "$(PLAYER=Moode command lf -print-last-dir "$@")"
}

lfcd () {
    # `command` is needed in case `lfcd` is aliased to `lf`
    cd "$(command lf -print-last-dir "$@")"
}

alias lf=lfcd
