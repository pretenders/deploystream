// global describe, beforeEach, it, expect, browser
'use strict';

/* http://docs.angularjs.org/guide/dev_guide.e2e-testing */

describe('my app', function () {

    beforeEach(function () {
        browser().navigateTo('/');
    });


    it('should show a login button when location fragment is empty', function () {
        expect(browser().location().url()).toBe("/");
        expect(element('a.btn-primary').text()).toContain('Sign in via Github');
        //element('a.btn-primary').click();
        //expect(browser().location().url()).toBe("/login");
    });

});
