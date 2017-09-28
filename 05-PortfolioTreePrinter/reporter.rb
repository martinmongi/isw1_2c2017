require './object'

class Reporter

  def self.detail(account)
    account.transactions.inject([]) { |lines, transaction |
      lines << transaction.detail
    }
  end

  def self.portfolio_tree_of(portfolio,accountNames)
    portfolio.account_tree(0, accountNames)
  end

  def self.reverse_portfolio_tree_of(portfolio,accountNames)
    portfolio.reverse_account_tree(0, accountNames)
  end

end