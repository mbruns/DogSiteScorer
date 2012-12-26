# Load the rails application
require File.expand_path('../application', __FILE__)

ENV['RAILS_ENV'] = 'development' #dazugetan, um mailer hinzukriegen!!

# Initialize the rails application
DoGSiteScorer::Application.initialize!
