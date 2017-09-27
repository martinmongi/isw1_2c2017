require './object'

class Transaction

  def self.register_for_on(amount, account)
    transaction = self.new(amount)
    account.register(transaction)
    transaction
  end

  def value
    self.should_implement
  end

  def affectBalance(balance)
  	self.should_implement
  end

  def affectTransferBalance(balance)
  	self.should_implement
  end

  def datail
  	self.should_implement
  end


end