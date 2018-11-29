#!/bin/bash
echo "================================== start =================================="

echo "select the source of git list"
echo "[1] from data base        [2] from .txt file"
read -p ">>> " source_choice

if test $source_choice -eq 1; then
    mode="default"

    echo "input the minimum of the stars"
    read -p ">>> " min

    echo "input the maximum of the stars"
    read -p ">>> " max


    echo "select the downloading path"
    echo "[1] default(./repository)       [2] specified path"
    read -p ">>> " download_path_choice

    if test $download_path_choice -eq 1; then
        echo "start downloading..."
        nohup python3 -u run.py mode:$mode stars:$min-$max download-path:default > ./log/download.log 2>&1 &

    elif test $download_path_choice -eq 2; then
        echo "Specify the downloading path"
        read -p ">>> " download_path
        echo "start downloading..."
        nohup python3 -u run.py mode:$mode stars:$min-$max download-path:$download_path > ./log/download.log 2>&1 &

    else
        echo "Error: invalid choice"
        exit
    fi

elif test $source_choice -eq 2; then
    mode="ff"

    echo "Specify the git list file path: "
    read -p ">>> " git_list_path
    echo "select the downloading path"
    echo "[1] default(./repository)       [2] specified path"
    read -p ">>> " download_path_choice

    if test $download_path_choice -eq 1; then
        echo "start downloading..."
        nohup python3 -u run.py mode:$mode data-path:$git_list_path download-path:default > ./log/download.log 2>&1 &

    elif test $download_path_choice -eq 2; then
        echo "Specify the downloading path"
        read -p ">>> " download_path
        echo "start downloading..."
        nohup python3 -u run.py mode:$mode data-path:$git_list_path download-path:$download_path > ./log/download.log 2>&1 &

    else
        echo "Error: invalid choice"
        exit
    fi

else
    echo "Error: invalid choice"
    exit
fi