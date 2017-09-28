require './transaction'

class CertificateOfDeposit < Transaction

  def initialize(capital,days,tna)
    @value = capital
    @days = days
    @tna = tna
  end

  def self.register_for_on(capital,days,tna,account)
    transaction = self.new(capital, days, tna)
    account.register(transaction)
    transaction
  end

  def affectBalance(balance)
  	balance - @value
  end

  def investmentValue
    @value
  end

  def investmentEarnings
    @value*(@tna/360)*@days
  end

  def detail
    "Plazo fijo por #{@value} durante #{@days} dias a una tna de #{@tna}"
  end

end