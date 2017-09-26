require './transaction'

class Withdraw < Transaction

  def initialize(value)
    @value = value
  end

  def affectBalance(balance)
  	balance - self.value
  end

  def value
    @value
  end
end