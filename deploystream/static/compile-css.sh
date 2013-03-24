#!/bin/bash
# Statically compile project LESS files as CSS

recess less/site.less --compile > css/site.css
recess less/site.less --compile --compress > css/site.min.css
recess less/responsive.less --compile > css/responsive.css
recess less/responsive.less --compile > css/responsive.min.css
