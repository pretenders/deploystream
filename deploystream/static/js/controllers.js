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
    var get_branch_data = function (repoBranches, repo) {
        var branches = [];
        var branchData = repoBranches[repo];
        for (var branch in branchData) {
            branches.push({name: branch, data: branchData[branch]});
        }
        return branches;
    };

    Feature.query('', function (features) {
        $scope.features = features;
    });

    Feature.get({featureId: featureId}, function (feature) {
        var repos = [];
        var repoBranches = feature.branches;
        for (var repo in repoBranches) {
            repos.push({name: repo, branches: get_branch_data(repoBranches, repo)});
        }
        $scope.feature = feature;
        $scope.repos = repos;
    });
}


//FeatureListCtrl.$inject = [];
