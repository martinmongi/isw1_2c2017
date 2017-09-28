require './summarizing_account'

class AccountQuerier
  def balance(account)
    account.balance
  end
  
  def balanceTransfer(account)
    process = Proc.new {|transactions| account.transactions.inject(0) { | balance, transaction | transaction.affectTransferBalance(balance)}}
    account.queryTransactions(&process)
  end 

  def investmentNet(account)
    process = Proc.new {|transactions| account.transactions.inject(0) { | balance, transaction | balance + transaction.investmentValue}}
    account.queryTransactions(&process)
  end

  def investmentEarnings(account)
    process = Proc.new {|transactions| account.transactions.inject(0) { | balance, transaction | balance + transaction.investmentEarnings}}
    account.queryTransactions(&process)
  end

  def accountSummaryLines(account)
    process = Proc.new {|transactions| account.transactions.map {|transaction| transaction.detail}}
    account.queryTransactions(&process)
  end

  def accountNetTransfer(account)
    process = Proc.new {|transactions| account.transactions.inject(0) { |sum, transaction | sum + transaction.transferNet }}
    account.queryTransactions(&process)
  end
end