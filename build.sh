#!/bin/bash
#Based on the build script from my master's thesis at https://github.com/adolfintel/Tesi2/build.sh
SECONDS=0
export LC_ALL=en_US.UTF-8
export TEXMFCNF='.:'
log(){
    echo "[$BASHPID] $1: $2"
}
build(){
    log $1 "compiling"
    mkdir -p .latex
    pdflatex -interaction=nonstopmode -output-directory=.latex "$1.tex" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        log $1 "build failed"
        return 1
    fi
    log $1 "compiled successfully"
    rm -f "./$1.pdf" >/dev/null 2>&1
    mv -f "./.latex/$1.pdf" . >/dev/null 2>&1
    rm -rf ./.latex
    return 0
}
#bash start
command -v pdflatex > /dev/null
if [[ $? -ne 0 ]]; then
    echo "Latexmk is missing, texlive-full may not be installed"
    return 1
fi;
echo "$(tput setaf 11)Build started$(tput sgr 0)"
build Rajaram_resume &
wait
echo "Build completed in $SECONDS seconds"
cp Rajaram_resume.pdf "/Users/arbitcode/Google Drive/My Drive/resume"
echo "Copied file on Goggle Drive at /Users/arbitcode/Google Drive/My Drive/resume"
mv Rajaram_resume.pdf out/Rajaram_resume.pdf
echo "Moved output file to out/Rajaram_resume.pdf"
