require './transaction'

class TransferDeposit < Transaction

  def initialize(value)
    @value = value
  end

  def self.register_transfer(transfer, account)
    transaction = self.register_for_on(transfer.value, account)
    @transfer = transfer
    transaction
  end

  def affectBalance(balance)
  	return balance + self.value
  end

  def transfer
    @transfer
  end

  def detail
    "Transferencia por #{@value}"
  end

  def value
    @value
  end

end

