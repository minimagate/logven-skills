class DeliveryJob
  def initialize(gateway:)
    @gateway = gateway
  end

  def perform(notification)
    notification.deliver_now(gateway: @gateway)
  end
end
