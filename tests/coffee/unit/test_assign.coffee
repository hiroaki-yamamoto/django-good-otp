describe "Secret key assignment test", ->
  input = undefined
  img = undefined
  name = undefined
  generateOTPSecretReturnValue = undefined
  windowMock = undefined

  beforeEach ->
    generateOTPSecretReturnValue = window.generateOTPSecret()
    windowMock = sinon.mock(window)
    input = {}
    img = {}
    name = "Test Name"

  afterEach ->
    windowMock.restore()

  describe "Calling assignOTPSecret without issuer_name, ", ->
    generateOTPSecret = undefined
    beforeEach ->
      generateOTPSecret = windowMock.expects("generateOTPSecret").once()
      generateOTPSecret.returns generateOTPSecretReturnValue
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
    generateOTPSecret = undefined
    issuer_name = "hi"
    qs = undefined
    beforeEach ->
      generateOTPSecret = windowMock.expects("generateOTPSecret").once()
      generateOTPSecret.returns generateOTPSecretReturnValue
      qs = [
        "name=#{encodeURIComponent name}",
        "issuer_name=#{encodeURIComponent issuer_name}"
      ]
      assignOTPSecret name, input, img, "/qrcode", issuer_name
      windowMock.verify()

    it "The image url should be proper", ->
      expect(img.src).is.equal(
        "/qrcode/#{input.value}?#{qs.join '&'}"
      )

  describe "Calling assignOTPSecret once with gen_new is false", ->
    issuer_name = "hi"
    generateOTPSecret = undefined
    beforeEach ->
      generateOTPSecret = windowMock.expects("generateOTPSecret").once()
      assignOTPSecret name, input, img, "/qrcode", issuer_name, false

    it "generateOTPSecret should be called once", ->
      generateOTPSecret.verify()

  describe "Calling assignOTPSecret once with gen_new is false", ->
    issuer_name = "hi"
    generateOTPSecret = undefined
    beforeEach ->
      assignOTPSecret name, input, img, "/qrcode", issuer_name, false
      generateOTPSecret = windowMock.expects("generateOTPSecret").never()
      assignOTPSecret name, input, img, "/qrcode", issuer_name, false

    it "generateOTPSecret shouldn't be called", ->
      generateOTPSecret.verify()
