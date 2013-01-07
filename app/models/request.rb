# == Schema Information
#
# Table name: requests
#
#  id         :integer         not null, primary key
#  pdb        :string(255)
#  created_at :datetime
#  updated_at :datetime
#

class Request < ActiveRecord::Base
  attr_accessible :pdb
end
