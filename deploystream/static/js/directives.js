/* global angular */
'use strict';

/* Directives */


angular.module('deploystream.directives', [])
.directive('appVersion', ['version', function (version) {
    return function ($scope, $element) {
        $element.text(version);
    };
}])
.directive('featureHealth', function() {
    return function($scope, $element) {
        $scope.$watch('branch', function(branch) {
            var health = branch.health.details;
            console.log($element);
            $($element).popover({
                placement: 'bottom',
                trigger: 'hover',
                html: false,
                content: JSON.stringify(health)
            });
        });
    };
});
