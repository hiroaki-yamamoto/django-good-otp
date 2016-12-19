describe "Generator test", ->
  it "The generated text should be random BASE 32 text.", ->
    expect(generateOTPSecret()).to.match /[A-Z2-7]{16}/
