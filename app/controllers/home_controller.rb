require 'net/http'

class HomeController < ApplicationController
  def index
  end

  def id
    @id = params[:ID]
    session[:ID] = @id.to_param
    @request = Request.create(:pdb => @id)
    session[:request] = @request.id
  #download PDB file
    Net::HTTP.start("www.rcsb.org") { |http|
      resp = http.get("/pdb/files/#{@id}.pdb")
      File.open("tmp/cache/#{@id}", "wb") { |file|
        file.write(resp.body)
      }
    }
  end

  def wait
    @address = params[:mail]
    @id = session[:ID]
    @session = session[:session_id]
    @request = session[:request]
    @info = "weil Du keine adresse angegeben hast, musst Du leider warten!"
    if @address != nil
      @info = "wir schicken auch eine mail an #{@address}"
      message = RequestMailer.request_mail(@address, @id, @request)
      message.deliver
    end
  end

end
