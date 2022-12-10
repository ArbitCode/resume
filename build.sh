#!/bin/bash
#Based on the build script from my master's thesis at https://github.com/adolfintel/Tesi2/build.sh
SECONDS=0
export LC_ALL=en_US.UTF-8
export TEXMFCNF='.:'
log(){
    echo "[$BASHPID] $1: $2"
}
build(){
    rm -f "$1.pdf"
    log $1 "compiling"
    local PASSES=3
    for i in $(seq $PASSES); do
        if [[ $i -eq $PASSES ]]; then
			latexmk -interaction=nonstopmode -pdf "$1.tex" >/dev/null 2>&1
        else
			latexmk -interaction=nonstopmode -pdf- "$1.tex" >/dev/null 2>&1
        fi
        if [[ $? -ne 0 ]]; then
			log $1 "failed"
            return 1
        fi
        if [[ $i -eq 1 ]]; then
			bibtex $1 >/dev/null 2>&1
        fi
    done
    log $1 "compiled"
    mv -f "$1.pdf" .. >/dev/null 2>&1
	mv -f "$1.tex" .. >/dev/null 2>&1
    return 0
}
command -v latexmk > /dev/null
if [[ $? -ne 0 ]]; then
    echo "Xelatex is missing, texlive-full may not be installed"
    return 1
fi;
command -v bibtex > /dev/null
if [[ $? -ne 0 ]]; then
    echo "Bibtex is missing, texlive-full may not be installed"
    return 1
fi;
echo "$(tput setaf 11)Parallel build started$(tput sgr 0)"
mv -f $1 latex >/dev/null 2>&1
cd latex
build Rajaram_resume &
wait
cd ..
echo "Build completed in $SECONDS seconds"
