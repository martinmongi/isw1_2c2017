require './transaction'

class CertificateOfDeposit < Transaction

  def initialize(capital,days,tna)
    @capital = capital
    @days = days
    @tna = tna
  end

  def self.register_for_on(capital,days,tna,account)
    transaction = self.new(capital, days, tna)
    account.register(transaction)
    transaction
  end

  def affectBalance(balance)
  	balance - @capital
  end

  def investmentValue
    @capital
  end

  def investmentEarnings
    @capital*(@tna/360)*@days
  end

  def detail
    "Plazo fijo por #{@capital} durante #{@days} dias a una tna de #{@tna}"
  end

end