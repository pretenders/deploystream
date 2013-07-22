// global Feature
'use strict';

/* Controllers */


function FeatureListCtrl($scope, Feature) {
    $scope.features = [];

    Feature.query('', function (features) {
        $scope.features = features;
    });
}


function FeatureDetailCtrl($scope, $routeParams, Feature) {

    var featureId = $routeParams.featureId;

    Feature.query('', function (features) {
        $scope.features = features;
    });

    Feature.get({featureId: featureId}, function (feature) {
        var repos = [];
        $scope.feature = feature;
        $scope.root = 'master';
    });
}


//FeatureListCtrl.$inject = [];
