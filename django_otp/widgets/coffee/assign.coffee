window.assignOTPSecret = (
  selectQuerySelector, inputQuerySelector, imgQuerySelector, urlPrefix
) ->
  select = document.querySelector selectQuerySelector
  input = document.querySelector inputQuerySelector
  img = document.querySelector imgQuerySelector
  input.value = generateOTPSecret()
  img.src = "#{urlPrefix}/#{input.value}?" +
            "name=#{select.options[select.selectedIndex].text}"
