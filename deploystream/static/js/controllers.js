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

function ProfileCtrl($scope, User) {

    // Hard code the available Oauths for now
    var oauths = ['github'];
    $scope.oauth_info = [];

    User.query('', function(user) {
        $scope.user = user;

        // Figure out which oauths we've got and which are missing.
        // Add any to $scope.oauth_info. Missing ones will have a username of
        // null.
        for (var i = 0; i < oauths.length; i++) {
           var oauth = oauths[i];
           var username = null;

           for (var j = 0; j < $scope.user.oauth_keys.length; j++) {
                var user_oauth_key = $scope.user.oauth_keys[j];
                if (user_oauth_key['service'] == oauth){
                    username = user_oauth_key['service_username'];
                    break;
                }
           }

           $scope.oauth_info.push({'service': oauth, 'username': username});

        }

    });

}
