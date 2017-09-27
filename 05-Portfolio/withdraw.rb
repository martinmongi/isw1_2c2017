require './transaction'

class Withdraw < Transaction

  def initialize(value)
    @value = value
  end

  def affectBalance(balance)
  	return balance - self.value
  end
  
  def affectTransferBalance(balance)
  	balance
  end
  
  def detail
    "Extraccion por #{@value}"
  end

  def value
    @value
  end
end