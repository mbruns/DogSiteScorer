require 'net/http'

class HomeController < ApplicationController
  def index
  end

  def id
    @id = params[:ID]
  #download PDB file
    Net::HTTP.start("www.rcsb.org") { |http|
      resp = http.get("/pdb/files/#{@id}.pdb")
      File.open("tmp/cache/#{@id}", "wb") { |file|
        file.write(resp.body)
      }
    }
  end

  def mail
    @address = params[:mail]
    message = RequestMailer.request_mail(@address)
    message.deliver
  end
  
  def wait
  end

end
