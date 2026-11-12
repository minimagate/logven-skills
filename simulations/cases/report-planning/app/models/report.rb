class Report < ApplicationRecord
  belongs_to :workspace
  belongs_to :dataset
  # config: {"columns" => [{"name" => "Revenue", "width" => 160}], "filters" => [], "sort" => nil}
  store_accessor :config, :columns, :filters, :sort

  def preview(attributes)
    update!(config: config.merge(attributes))
    dataset.rows
  end

  def copy!
    self.class.create!(workspace: workspace, dataset: dataset, config: config)
  end
end
