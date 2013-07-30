/* global angular */
'use strict';

/* Directives */


angular.module('deploystream.directives', [])
.directive('appVersion', ['version', function (version) {
    return function ($scope, $element) {
        $element.text(version);
    };
}]);
// .directive('featureHealth', function() {
// });
