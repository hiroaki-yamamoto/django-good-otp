describe "Secret key assignment test", ->
  input = undefined
  img = undefined
  name = undefined
  generateOTPSecretReturnValue = undefined
  windowMock = undefined
  generateOTPSecret = undefined

  beforeEach ->
    generateOTPSecretReturnValue = window.generateOTPSecret()
    windowMock = sinon.mock(window)
    input = {}
    img = {}
    name = "Test Name"
    generateOTPSecret = windowMock.expects("generateOTPSecret").once()
    generateOTPSecret.returns generateOTPSecretReturnValue

  afterEach ->
    windowMock.restore()

  describe "Calling assignOTPSecret without issuer_name, ", ->
    beforeEach ->
      assignOTPSecret name, input, img, "/qrcode"
      windowMock.verify()

    it "The secret key is generated", ->
      expect(generateOTPSecret.calledOnce).is.true
      expect(generateOTPSecret.calledWithExactly()).is.true

    it "The input value should be proper", ->
      expect(input.value).is.equal generateOTPSecretReturnValue

    it "The image url should be proper", ->
      expect(img.src).is.equal(
        "/qrcode/#{input.value}?" +
        "name=#{encodeURIComponent name}"
      )

  describe "Calling assignOTPSecret with issuer_name, ", ->
    issuer_name = "hi"
    qs = undefined
    beforeEach ->
      qs = [
        "name=#{encodeURIComponent name}",
        "issuer_name=#{encodeURIComponent issuer_name}"
      ]
      assignOTPSecret name, input, img, "/qrcode", issuer_name

    it "The image url should be proper", ->
      expect(img.src).is.equal(
        "/qrcode/#{input.value}?#{qs.join '&'}"
      )
