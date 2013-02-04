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
  
    #variablen füllen
    @id = session[:ID]
    @session = session[:session_id]
    @request = session[:request]
    @info = "weil Du keine adresse angegeben hast, musst Du leider warten!"
#    @ready = false

    #als mail verschicken?
    if not params[:mail].empty?      
      @address = params[:mail]
      @info = "wir schicken auch eine mail an #{@address}"
      session[:mail] = @address
    end

    #tool aufrufen
    fork do
      system ("ruby lib/tasks/sleep.rb #{@id}")
#      @ready = true
    end

#    if $?.exitstatus != 0 then
#      flash.now[:alert] = 'Problem im tool. geh dich irgendwo beschweren!'
#    end


    
  end 
  
  def results
    @id = session[:ID]
    @request = session[:request]
    @address = session[:mail]
    
    #mail senden
    if @address
      message = RequestMailer.request_mail(@address, @id, @request)
      message.deliver
    end
    
    redirect_to :action=>"show", :id=>"#{@request}", :controller=>"requests"
  end

end
