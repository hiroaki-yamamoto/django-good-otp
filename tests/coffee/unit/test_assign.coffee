describe "Secret key assignment test", ->
  documentMock = undefined
  windowMock = undefined

  querySelectorStub = undefined
  generateOTPSecret = undefined
  generateOTPSecretReturnValue = undefined
  input = undefined
  img = undefined
  select = undefined

  beforeEach ->
    generateOTPSecretReturnValue = window.generateOTPSecret()
    documentMock = sinon.mock(document)
    windowMock = sinon.mock(window)
    querySelectorStub = documentMock.expects("querySelector").thrice()
    input = {}
    img = {}
    select =
      "selectedIndex": 0
      "options": [
        ("text": "Test")
      ]
    querySelectorStub.onCall(0).returns select
    querySelectorStub.onCall(1).returns input
    querySelectorStub.onCall(2).returns img
    generateOTPSecret = windowMock.expects("generateOTPSecret").once()
    generateOTPSecret.returns generateOTPSecretReturnValue

  afterEach ->
    documentMock.restore()
    windowMock.restore()

  describe "Calling assignOTPSecret, ", ->
    beforeEach ->
      assignOTPSecret "#OTPSelect", "#OTPInput", "#OTPImg", "/qrcode"

    it "The secret key is generated", ->
      expect(generateOTPSecret.calledOnce).is.true
      expect(generateOTPSecret.calledWithExactly()).is.true

    it "The input value should be proper", ->
      expect(input.value).is.equal generateOTPSecretReturnValue

    it "The image url should be proper", ->
      expect(img.src).is.equal(
        "/qrcode/#{input.value}?" +
        "name=#{select.options[select.selectedIndex].text}"
      )
