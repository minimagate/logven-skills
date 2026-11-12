require "minitest/autorun"
require "notification"
require "gateway"
require "delivery_job"

class NotificationTest < Minitest::Test
  def test_job_delivers_a_notification
    gateway = Gateway.new
    notification = Notification.new(id: 7, account_id: 1, to: "ops@example.test", body: "Your report is ready")
    DeliveryJob.new(gateway: gateway).perform(notification)
    assert notification.delivered?
    assert_equal "receipt-1", notification.receipt
    assert_equal 1, gateway.messages.length
  end
end
