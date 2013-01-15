figlet 'mmfinder: bash plugin'
echo
echo ' gl              list directories of the result of mmfinder '
echo ' ol              list of files of the result of mmfinder'
echo
echo ' g 1             go to directory #1 of mmfinder'
echo ' o 1             open a file #1'
echo ' e 1             open file #1 in emacsclient'
echo ' r 1             run (execute) file #1'
echo ' n 1             open in nautilus file #1'
echo
echo ' starting... [OK]'
echo
## see files
function ol(){
    cat ~/.mmfinder-paths-to-open
}

function gl(){
    cat ~/.mmfinder-paths
}

## functions
function g(){
    path=`grep "#${1}$" ~/.mmfinder-paths` 
    echo $path
    cd $path
}

function o(){
    path=`grep "#${1}$" ~/.mmfinder-paths-to-open | awk '{ print $1 }'`
    echo $path
    xdg-open $path
}
function e(){
    path=`grep "#${1}$" ~/.mmfinder-paths-to-open | awk '{ print $1 }'`
    echo $path
    emacsclient $path &
}

function r(){
    path=`grep "#${1}$" ~/.mmfinder-paths-to-open | awk '{ print $1 }'`
    echo $path
    exec $path &
}

function n(){
    path=`grep "#${1}$" ~/.mmfinder-paths-to-open | awk '{ print $1 }'`
    echo $path
    nautilus $path &
}





