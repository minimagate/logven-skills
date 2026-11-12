class Dataset < ApplicationRecord
  belongs_to :workspace
  has_many :fields, dependent: :destroy
  has_many :rows, dependent: :destroy
end

# Field has a stable id plus user-editable name and kind.
# Row#data is JSON with arbitrary user-defined values keyed by field id.
