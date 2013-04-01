// global Feature
'use strict';

/* Controllers */


function FeatureListCtrl($scope, Feature) {
    $scope.features = [];

    Feature.query('', function (features) {
        $scope.features = features;
    });
}
//FeatureListCtrl.$inject = [];
