class Notification
  attr_reader :id, :account_id, :to, :body, :state, :receipt

  def initialize(id:, account_id:, to:, body:, state: :pending, receipt: nil)
    @id, @account_id, @to, @body, @state, @receipt = id, account_id, to, body, state, receipt
  end

  def delivered?
    state == :delivered
  end

  def deliver_now(gateway:)
    @receipt = gateway.deliver(to: to, body: body)
    @state = :delivered
    receipt
  end
end
