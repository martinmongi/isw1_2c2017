require './object'

class Reporter

  def detail(account)
	  @accounts.transactions.inject([]) { |lines, transaction |
      lines << transaction.detail
    }
  end


end