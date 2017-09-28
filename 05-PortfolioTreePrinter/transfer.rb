require './transaction'
require './transfer_deposit'
require './transfer_withdraw'

class Transfer

  def initialize(amount, fromAccount, toAccount)
    @value = amount
    @deposit = TransferDeposit.register_transfer(self, toAccount)
  	@withdraw = TransferWithdraw.register_transfer(self, fromAccount)
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

