#!/bin/bash
# Dynamically compile site.less when LESS files in 'less' folder change

recess less/site.less:css/site.css --watch less/
