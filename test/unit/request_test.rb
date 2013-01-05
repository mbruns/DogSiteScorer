# == Schema Information
#
# Table name: requests
#
#  id         :integer         not null, primary key
#  pdb        :string(255)
#  email      :string(255)
#  created_at :datetime
#  updated_at :datetime
#

require 'test_helper'

class RequestTest < ActiveSupport::TestCase
  # Replace this with your real tests.
  test "the truth" do
    assert true
  end
end
