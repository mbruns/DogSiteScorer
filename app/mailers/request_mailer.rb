class RequestMailer < ActionMailer::Base
  default :from => "meike-bruns@hotmail.de"

  def request_mail(user)
    attachments['request.txt'] = File.read('/home/meike/DoGSiteScorer/tmp/cache/3T0L')
    mail(:to => user, :subject => "Answering your Request")
  end
end
