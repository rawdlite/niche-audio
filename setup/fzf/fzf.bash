alias vf='vim $(fzf --preview "batcat --color=always {}" --preview-window "~3")'
alias vfi='vim $(fzf --height 40% --layout reverse --info inline --border --preview "batcat --color=always {}" --preview-window "~3" --bind "ctrl-u:preview-page-up,ctrl-d:preview-page-down,ctrl-b:preview-half-page-up,ctrl-f:preview-half-page-down")'
#fzf --height 40% --layout reverse --info inline --border \
#    --preview 'file {}' --preview-window up,1,border-horizontal \
#    --bind 'ctrl-/:change-preview-window(50%|hidden|)' \
#    --color 'fg:#bbccdd,fg+:#ddeeff,bg:#334455,preview-bg:#223344,border:#778899'
export FZF_DEFAULT_COMMAND='fdfind --type file'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
# Setup fzf
# ---------
if [[ ! "$PATH" == */usr/local/bin* ]]; then
  PATH="${PATH:+${PATH}:}/usr/local/bin"
fi

eval "$(fzf --bash)"
f() {
    # Store the program
    program="$1"

    # Remove first argument off the list
    shift

    # Store option flags with separating spaces, or just set as single space
    options="$@"
    if [ -z "${options}" ]; then
        options=" "
    else
        options=" $options "
    fi

    # Store the arguments from fzf
    arguments="$(fzf --multi)"

    # If no arguments passed (e.g. if Esc pressed), return to terminal
    if [ -z "${arguments}" ]; then
        return 1
    fi

    # We want the command to show up in our bash history, so write the shell's
    # active history to ~/.bash_history. Then we'll also add the command from
    # fzf, then we'll load it all back into the shell's active history
    history -w

    # ADD A REPEATABLE COMMAND TO THE BASH HISTORY ############################
    # Store the arguments in a temporary file for sanitising before being
    # entered into bash history
    : > /tmp/fzf_tmp
    for file in "${arguments[@]}"; do
        echo "$file" >> /tmp/fzf_tmp
    done

    # Put all input arguments on one line and sanitise the command by putting
    # single quotes around each argument, also first put an extra single quote
    # next to any pre-existing single quotes in the raw argument
    sed -i "s/'/''/g; s/.*/'&'/g; s/\n//g" /tmp/fzf_tmp

    # If the program is on the GUI list, add a '&' to the command history
    if [[ "$program" =~ ^(nautilus|zathura|evince|vlc|eog|kolourpaint)$ ]]; then
        sed -i '${s/$/ \&/}' /tmp/fzf_tmp
    fi

    # Grab the sanitised arguments
    arguments="$(cat /tmp/fzf_tmp)"

    # Add the command with the sanitised arguments to our .bash_history
    echo $program$options$arguments >> ~/.bash_history

    # Reload the ~/.bash_history into the shell's active history
    history -r

    # EXECUTE THE LAST COMMAND IN ~/.bash_history #############################
    fc -s -1

    # Clean up temporary variables
    rm /tmp/fzf_tmp
}
