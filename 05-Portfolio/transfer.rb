require './transaction'

class Transfer

  def initialize(amount, fromAccount, toAccount)
    @deposit = TransferDeposit.register_for_on(amount, toAccount, self)
  	@withdraw = TransferWithdraw.register_for_on(amount, fromAccount, self)
  	@value = amount
  end

  def self.register(amount, fromAccount, toAccount)
  	transfer = self.new(amount, fromAccount, toAccount)
  	transfer
  end

  def deposit_leg
    @deposit
  end

  def withdraw_leg
    @withdraw
  end

  def value
    @value
  end

end

