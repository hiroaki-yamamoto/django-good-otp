g = require "gulp"
toolbox = require "hyamamoto-job-toolbox"
karmaConf = require "./etc/karma.conf.coffee"
needOneTime = toolbox.helper.isProduction or process.env.node_mode is "init"
karmaConf.singleRun = needOneTime

toolbox.python "", "django_otp", undefined, undefined, undefined, "migrations"
toolbox.karma "", "django_otp", [], [], karmaConf
toolbox.coffee(
  "widgets.", "django_otp", "django_otp/widgets/files", undefined,
  [if needOneTime then "karma.server" else "karma.runner"]
)
g.task "python.cov.erase", ->
  toolbox.virtualenv "coverage erase"
g.task "python.tox.front", ["python.cov.erase", "python.tox.only"], ->
  toolbox.virtualenv([
    "coverage combine python27.coverage python35.coverage"
    "coverage report -m"
  ])

taskDep = if needOneTime then ["python.tox.front", "widgets.coffee"] else []

g.task "default", taskDep, ->
  if not needOneTime
    g.start "karma.server"
    g.watch [
      "tests/**/*.py", "django_otp/**/*.py", "django_otp/widgets/files/*",
      "setup.py", "tox.ini"
    ], ["python.tox.front"]
    g.watch [
      "django_otp/widgets/coffee/**/*.coffee"
      "tests/coffee/**/*.coffee"
    ], ["widgets.coffee"]
