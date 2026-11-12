# Contract double for an external SDK. Do not modify this file.
class Gateway
  attr_reader :messages
  attr_accessor :timeout_before, :timeout_after

  def initialize
    @messages = []
    @receipts = {}
    @lock = Mutex.new
  end

  # Keys are scoped to this provider account, shared by all application accounts.
  # A stable key makes repeated calls return the original receipt without resending.
  # A timeout can happen before acceptance or after acceptance with the response lost.
  def deliver(to:, body:, idempotency_key: nil)
    @lock.synchronize do
      if timeout_before
        self.timeout_before = false
        raise IOError, "connection timed out before acceptance"
      end
      return @receipts[idempotency_key] if idempotency_key && @receipts.key?(idempotency_key)

      receipt = "receipt-#{messages.length + 1}"
      messages << {to: to, body: body, receipt: receipt}
      @receipts[idempotency_key] = receipt if idempotency_key
      if timeout_after
        self.timeout_after = false
        raise IOError, "response lost after acceptance"
      end
      receipt
    end
  end
end
