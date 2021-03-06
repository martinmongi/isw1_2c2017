require './summarizing_account'

class Portfolio < SummarizingAccount

  def self.create_with(account1,account2)
    portfolio = self.new
    portfolio.add_account(account1)
    portfolio.add_account(account2)
    portfolio
  end

  def self.ACCOUNT_ALREADY_MANAGED
    'Account already managed'
  end

  def initialize
    @accounts = []
  end

  def add_account(account)
    raise self.class.ACCOUNT_ALREADY_MANAGED if self.manages(account)
    @accounts << account
  end

  def account_tree(level, accountNames)
    name =  " "*level + accountNames[self]
    @accounts.inject([name]) { |lines, account |
      lines.concat(account.account_tree(level + 1,accountNames))
      lines
    }
  
  end

  def reverse_account_tree(level, accountNames)
    name =  " "*level + accountNames[self]
    @accounts.inject([name]) { |lines, account |
      lines.insert(0, *account.reverse_account_tree(level + 1,accountNames))
      lines
    }
  
  end

  def balance
    @accounts.inject(0) { |balance,account | balance + account.balance }
  end

  def balanceTransfer
    @transactions.inject(0) { |balance,account | balance +  transaction.balanceTransfer }
  end

  def registers(transaction)
    @accounts.any? { |account| account.registers(transaction) }
  end

  def manages(account)
    self == account or @accounts.any? {|component_account | component_account.manages(account)}
  end

  def transactions
    @accounts.inject([]) { |transactions,account |
      transactions.concat(account.transactions)
      transactions
    }
  end

end