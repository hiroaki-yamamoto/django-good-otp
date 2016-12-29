window.assignOTPSecret = (name, input, img, urlPrefix, issuer_name) ->
  input.value = generateOTPSecret()
  qs = ["name=" + encodeURIComponent name]
  if issuer_name
    qs = qs.concat "issuer_name=#{encodeURIComponent issuer_name}"
  img.src = "#{urlPrefix}/#{input.value}?#{qs.join "&"}"
