#!/bin/sh

printf 'Content-Type: image/png\n\n'
sudo fbcat | convert ppm:- png:-
