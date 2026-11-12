Invoice = Struct.new(:id, :account_id, :amount, :currency, :charge_id, keyword_init: true)

class InvoiceRepository
  def initialize(invoices)
    @invoices = invoices
  end

  def find(id)
    @invoices.find { |invoice| invoice.id == id } || raise(KeyError, "unknown invoice")
  end
end
