require './object'

class Reporter

  def self.detail(account)
    @lines = account.transactions.inject([]) { |lines, transaction |
      lines << transaction.detail
    }
  end


end