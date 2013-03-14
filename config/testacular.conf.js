// global JASMINE, JASMINE_ADAPTER
basePath = '../deploystream/static';

files = [
    JASMINE,
    JASMINE_ADAPTER,
    'lib/angular/angular.js',
    'lib/angular/angular-*.js',
    'test/lib/angular/angular-mocks.js',
    'js/**/*.js',
    'test/unit/**/*.js'
];

autoWatch = true;

browsers = ['Chrome'];
reporters = ['junit', 'progress'];

junitReporter = {
    outputFile: '../../reports/junit.xml',
    suite: 'unit'
};
