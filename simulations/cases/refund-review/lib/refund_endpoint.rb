class RefundEndpoint
  def initialize(repository:, gateway:, permissions:)
    @repository, @gateway, @permissions = repository, gateway, permissions
  end

  def create(account_id:, actor:, invoice_id:)
    raise SecurityError, "denied" unless @permissions.can_refund?(actor, account_id)
    invoice = @repository.find(invoice_id)
    cents = (invoice.amount.to_f * 100).to_i
    @gateway.refund(charge_id: invoice.charge_id, cents: cents)
    {status: 202}
  rescue IOError
    {status: 202}
  end
end
