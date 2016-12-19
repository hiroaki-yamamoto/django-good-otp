window.generateOTPSecret = ->
  map = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
  return (map[Math.floor Math.random() * 32] for num in [0...16]).join ""
