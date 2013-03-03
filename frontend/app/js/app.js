// global angular, FeatureList
'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives'])
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/features', {
        templateUrl: 'partials/partial1.html',
        controller: FeatureList
    });
    $routeProvider.otherwise({
        redirectTo: '/view1'
    });
}]);
