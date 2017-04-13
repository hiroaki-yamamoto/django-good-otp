g = require "gulp"
toolbox = require "hyamamoto-job-toolbox"
sp = require "simple-process"
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
  sp.pyvenv "coverage erase"
g.task "python.tox.front", ["python.cov.erase", "python.tox.only"], ->
  covData = []
  for pyversion in [27, 36]
    do (pyversion) ->
      for djversion in [110, 111]
        do (djversion) ->
          covData.push "py#{pyversion}-dj#{djversion}.coverage"
  sp.pyvenv([
    "coverage combine #{covData.join ' '}"
    "coverage report -m"
  ], [], undefined, {
    "stdio": ["inherit", "inherit", "pipe"]
  })

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
