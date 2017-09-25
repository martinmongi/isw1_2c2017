require './summarizing_account'

class Portfolio < SummarizingAccount

  def initialize
    @accounts = []
  end

  def self.create_with(account1,account2)
    portfolio = self.new
    portfolio.add_account(account1)
    portfolio.add_account(account2)
    portfolio
  end

  def balance
    @accounts.inject(0) { |balance,accounts | balance+accounts.balance }
  end

  def registers(transaction)
    @accounts.each do |account|
      if (account.registers(transaction))
        return true
      end  
    end
    return false
  end

  def manages(account)
    @accounts.each do |iterateAccount|
      if(account == iterateAccount)
        return true
      end
      if (iterateAccount.manages(account))
        return true
      end  
    end
    return false 
  end

  def self.ACCOUNT_ALREADY_MANAGED
    'Account already managed'
  end

  def transactions
    transactions = []
    @accounts.each do |account|
      transactions.concat(account.transactions)
    end
    transactions.clone
  end

  def add_account(account)
    if (self.manages(account))
      raise Portfolio.ACCOUNT_ALREADY_MANAGED
    end
      @accounts << account
  end
end