require './summarizing_account'

class ReceptiveAccount < SummarizingAccount

  def initialize
    @transactions = []
  end

  def register(transaction)
    @transactions << transaction
  end

  def balance
    @transactions.inject(0) { |balance,transaction | transaction.affectBalance(balance) }
  end

  def account_tree(level, accountNames)
    name =  " "*level + accountNames[self]
    [name]
  end

  def reverse_account_tree(level, accountNames)
    name =  " "*level + accountNames[self]
    [name]
  end

  def balanceTransfer
    @transactions.inject(0) { |balance,transaction | transaction.affectTransferBalance(balance) }
  end

  def registers(transaction)
    @transactions.include? (transaction)
  end

  def manages(account)
    self == account
  end

  def transactions
    @transactions.clone
  end

end