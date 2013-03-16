// global angular, FeatureListCtrl
'use strict';


// Declare app level module which depends on filters, and services
angular.module('deploystream', [
        'deploystream.filters',
        'deploystream.services',
        'deploystream.directives'
    ])
.config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: '/static/partials/home.html'
        });
        $routeProvider.when('/features', {
            templateUrl: '/static/partials/features.html',
            controller: FeatureListCtrl
        });
    }]
);
