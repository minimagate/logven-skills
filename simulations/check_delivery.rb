# Evaluator-only checks. Run after the candidate has finished, outside its workspace.
require "minitest/autorun"
$LOAD_PATH.unshift(File.join(ARGV.shift || abort("workspace required"), "lib"))
require "notification"
require "delivery_job"
require "gateway"

class DeliveryContractTest < Minitest::Test
  def notification(id: 7, account_id: 1)
    Notification.new(id: id, account_id: account_id, to: "ops@example.test", body: "Ready")
  end

  def test_repeated_jobs_do_not_resend
    gateway, message = Gateway.new, notification
    2.times { DeliveryJob.new(gateway: gateway).perform(message) }
    assert_equal 1, gateway.messages.length
    assert message.delivered?
  end

  def test_response_lost_after_provider_acceptance_is_retryable_without_resend
    gateway, message = Gateway.new, notification
    gateway.timeout_after = true
    assert_raises(IOError) { message.deliver_now(gateway: gateway) }
    refute message.delivered?
    message.deliver_now(gateway: gateway)
    assert_equal 1, gateway.messages.length
    assert_equal "receipt-1", message.receipt
    assert message.delivered?
  end

  def test_failure_before_acceptance_does_not_mark_delivered
    gateway, message = Gateway.new, notification
    gateway.timeout_before = true
    assert_raises(IOError) { message.deliver_now(gateway: gateway) }
    refute message.delivered?
    assert_empty gateway.messages
    message.deliver_now(gateway: gateway)
    assert_equal 1, gateway.messages.length
  end

  def test_rehydrated_object_reuses_the_same_logical_delivery
    gateway = Gateway.new
    first, rehydrated = notification, notification
    first.deliver_now(gateway: gateway)
    rehydrated.deliver_now(gateway: gateway)
    assert_equal 1, gateway.messages.length
    assert_equal first.receipt, rehydrated.receipt
  end

  def test_same_local_identifier_in_two_accounts_is_not_one_delivery
    gateway = Gateway.new
    notification(account_id: 1).deliver_now(gateway: gateway)
    notification(account_id: 2).deliver_now(gateway: gateway)
    assert_equal 2, gateway.messages.length
  end

  def test_distinct_notifications_are_distinct_deliveries
    gateway = Gateway.new
    notification(id: 7).deliver_now(gateway: gateway)
    notification(id: 8).deliver_now(gateway: gateway)
    assert_equal 2, gateway.messages.length
  end
end
