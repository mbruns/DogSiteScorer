require 'net/http'

class HomeController < ApplicationController
  def index
  end

  def id
    #test, ob PDB_ID angegeben wurde
    if params[:ID].empty?
      flash[:notice] = "Du musst eine PDB-ID eingeben!"
      redirect_to :action => 'index'
    end
    #variablen füllen, request in Datenbank speichern
    @id = params[:ID]
    session[:ID] = @id.to_param
    @request = Request.create(:pdb => @id)
    session[:request] = @request.id

    #download PDB file
    #noch nicht vorhanden? -> runterladen 
    if not File.exists?("tmp/cache/#{@id}") then
      Net::HTTP.start("www.rcsb.org") { |http|
        resp = http.get("/pdb/files/#{@id}.pdb")
        #existiert -> in Datei schreiben
        if resp.is_a?(Net::HTTPSuccess) then
          File.open("tmp/cache/#{@id}", "wb") { |file|
            file.write(resp.body)}
        #existiert nicht -> zurück zur Startseite
        else
        flash[:notice] = "diese PDB-ID gibts nicht. Versuchs noch mal!"
        redirect_to :action => 'index'
        end
      }
    end
    
  end

  def wait
  
    #als mail verschicken?
    if not params[:mail].empty?      
      @address = params[:mail]
    end
    
    #variablen füllen
    @id = session[:ID]
    @session = session[:session_id]
    @request = session[:request]
    @info = "weil Du keine adresse angegeben hast, musst Du leider warten!"
    #eingabe ins tool/warten, bis das tool fertig ist
    
    #mail senden
    if @address
      @info = "wir schicken auch eine mail an #{@address}"
      message = RequestMailer.request_mail(@address, @id, @request)
      message.deliver
    end
  end

end
