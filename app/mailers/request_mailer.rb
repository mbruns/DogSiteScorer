class RequestMailer < ActionMailer::Base
  default :from => "meike-bruns@hotmail.de"

  def request_mail(user,id, request)
    @answer = "localhost:3000/requests/#{request}"
    attachments["#{id}.txt"] = File.read("/home/meike/DoGSiteScorer/tmp/cache/#{id}")
    mail(:to => user, :subject => "Answering your Request")
  end
end
