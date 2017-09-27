require './transaction'

class Withdraw < Transaction

  def initialize(value)
    @value = value
  end

  def affectBalance(balance)
  	return balance - self.value
  end
  
  def detail
    "Extraccion por #{@value}"
  end

  def value
    @value
  end
end