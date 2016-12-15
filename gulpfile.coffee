g = require "gulp"
toolbox = require "hyamamoto-job-toolbox"

toolbox.python "", "django_otp"
# toolbox.coffee "", "django_otp", "django_otp/views"

needOneTime = toolbox.helper.isProduction or process.env.node_mode is "init"

taskDep = if needOneTime then ["python.tox.only", "coffee"] else []

g.task "default", taskDep, ->
  if not needOneTime
    g.watch [
      "tests/**/*.py", "django_otp/**/*.py", "setup.py"
    ], ["python.tox.only"]
    # g.watch ["django_otp/**/*.coffee"], ["coffee"]
