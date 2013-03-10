// global angular
'use strict';

/* Directives */


angular.module('deploystream.directives', [])
.directive('appVersion', ['version', function (version) {
    return function (scope, elm, attrs) {
        elm.text(version);
    };
}]);
