// global Feature
'use strict';

/* Controllers */


function FeatureListCtrl($scope, Feature) {
    $scope.features = Feature.query();
}
//FeatureListCtrl.$inject = [];
