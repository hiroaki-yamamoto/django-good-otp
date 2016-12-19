helper = require "hyamamoto-job-toolbox"

module.exports =
    "basePath": "./"
    "quiet": true
    "frameworks": ["mocha", "chai", "sinon"]
    "reporters": ["progress", "coverage"]
    "colors": true
    "logLevel": "INFO"
    "autoWatch": false
    "singleRun": helper.isProduction
    "port": 9876
    "preprocessors":
      "django_otp/**/coffee/**/*.coffee": ["coffee", "coverage"]
      "tests/**/coffee/unit/**/*.coffee": ["coffee"]
    "coffeePreprocessor":
      "options":
        "sourceMap": true
    "coverageReporter":
      "type": 'html'
      "dir": "browser_coverage"
    "browsers": ["Chrome", "Firefox", "PhantomJS"]
    "plugins": [
      "karma-coverage"
      "karma-mocha"
      "karma-chai-plugins"
      "karma-chrome-launcher"
      "karma-coffee-preprocessor"
      "karma-firefox-launcher"
      "karma-phantomjs-launcher"
      "karma-sinon"
    ]
