// global describe, beforeEach, inject, it, expect
// global FeatureListCtrl
'use strict';

/* jasmine specs for controllers go here */

describe('Feature list controller', function () {
    var scope, ctrl;

    beforeEach(inject(function ($rootScope, $controller) {
        scope = $rootScope.$new();
        ctrl = $controller(FeatureListCtrl, {$scope: scope});
    }));


    it('should add features to the scope', function () {
        //spec body
        expect(scope.features.length).toBe(2);
    });
});
