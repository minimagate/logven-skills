require "minitest/autorun"
require "refund_endpoint"
require "invoice_repository"

class RefundTest < Minitest::Test
  def test_refund
    invoice = Invoice.new(id: 5, account_id: 1, amount: "20.00", currency: "USD", charge_id: "charge-a")
    gateway = Object.new
    def gateway.refund(charge_id:, cents:); raise unless cents == 2000; end
    permissions = Object.new
    def permissions.can_refund?(actor, account_id); true; end
    endpoint = RefundEndpoint.new(repository: InvoiceRepository.new([invoice]), gateway: gateway, permissions: permissions)
    assert_equal({status: 202}, endpoint.create(account_id: 1, actor: :operator, invoice_id: 5))
  end
end
