require 'net/http'

class HomeController < ApplicationController
  def index
  end

  def id
    @id = params[:ID]
    session[:ID] = @id.to_param
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
    @id = session[:ID]
    message = RequestMailer.request_mail(@address, @id)
    message.deliver
  end
  
  def wait
    @id = session[:ID]
    @session = session[:session_id]
  end

end
