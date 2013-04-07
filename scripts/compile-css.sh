#!/bin/bash
# Statically compile project LESS files as CSS

CMD=lessc

pushd deploystream/static

mkdir -p css
$CMD less/site.less > css/site.css
$CMD less/site.less --compress > css/site.min.css
$CMD less/responsive.less > css/responsive.css
$CMD less/responsive.less --compress > css/responsive.min.css

popd
