// global angular
'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('deploystream.services', ['ngResource'])
    .value('version', '0.1')
    .factory('Feature', function ($resource) {
        return $resource(
            '/features/:featureId',
            {},
            {
                query: {
                    method: 'GET',
                    params: {featureId: ''},
                    isArray: true
                }
            });
    })
    .factory('User', function($resource) {
        return $resource(
            '/users/me/',
            {},
            {
                query: {
                    method: 'GET'
                }
            });
    });
