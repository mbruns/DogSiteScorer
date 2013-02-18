require 'net/http'

class HomeController < ApplicationController

  def index
  @title = "Start"
  end

  def id

  
  
    #test: wurde PDB_ID bzw. Datei angegeben? 
    if params[:ID].blank? && params[:upload].blank?
      flash[:notice] = "Du musst eine PDB-ID eingeben!"
      return redirect_to :action => 'index'
    end
    
    #test: beide ausgefüllt?
    
    #create timestamp
    @timestamp = Time.now.utc.iso8601.gsub(/\W/, '')
    session[:time] = @timestamp

    #case 1: PDB-ID submitted:
    #fill variables
    if not params[:ID].blank? then
      @id = params[:ID]
      session[:ID] = @id.to_param
      @request = Request.create(:pdb => @id+ "_#{@timestamp}.pdb")
      session[:request] = @request.id
    #download pdb file
      Net::HTTP.start("www.rcsb.org") { |http|
        resp = http.get("/pdb/files/#{@id}.pdb")
        #existing -> write to file
        if resp.is_a?(Net::HTTPSuccess) then
          File.open("tmp/cache/#{@id}_#{@timestamp}.pdb", "wb") { |file|
            file.write(resp.body)}
        #not existing -> back to index page
        else
          flash[:notice] = "diese PDB-ID gibts nicht. Versuchs noch mal!"
          return redirect_to :action => 'index'
        end
      }
    end
    
    #case 2: file submitted
    if not params[:upload].blank? then
      #fill variables
      @id = params[:upload].original_filename
      session[:ID] = @id.to_param
      @request = Request.create(:pdb => @id+ "_#{@timestamp}.pdb")
      session[:request] = @request.id
      #upload pdb-file
      uploaded_io = params[:upload]
      File.open("tmp/cache/#{@id}_#{@timestamp}.pdb", 'w') do |file|
       file.write(uploaded_io.read)
      end
    end


      
      #bearbeite PDB-File:
      #ermittle chains
      File.readlines("tmp/cache/#{@id}_#{@timestamp}.pdb").each do |line|  
        if line =~ /^COMPND   3 CHAIN:(.*)/ then
          @chains = $1.split(/(,|;)/)
          break
        end
      end
      @chains.keep_if {|v| v =~ /[A-Z]/}    
  end

  def wait
  
    #variablen füllen aus session
    @id = session[:ID]
    @session = session[:session_id]
    @request = session[:request]
    @info = "weil Du keine adresse angegeben hast, musst Du leider warten!"
    @timestamp = session[:time]
    #variablen füllen aus params
    @chain = params[:chain]
    @pocLev = params[:granularity]
    #bzw z.T. erstmal hardgecodet:
    @scoreType = 0
    @gridSpacing = 0.6 #gitterweiter 0.4 -1.5
    @lig_id = -1 #liganden laden? entweder hochladen (auch fürs protein!) = 0, = 1, wenn parsen (system pdb2molecule pdb_timestamp.pdb pdb_timestamp.mol2, 


    #als mail verschicken?
    if not params[:mail].empty?      
      @address = params[:mail]
      @info = "wir schicken auch eine mail an #{@address}"
      session[:mail] = @address
    end


#    #tool aufrufen
#    fork do
#      system ("ruby lib/tasks/sleep.rb #{@id}")
#    end
    
    if not @chain.is_a? Integer then
      @chainId = @chain
      @chain = 1
    end  #chains: .pdbs für jede anlegen mit checkpdb.py 
    
    #chain id ist bei chains 0 all egal
    puts "python lib/tasks/main.py #{@id} #{@chain} #{@pocLev} #{@scoreType} #{@gridSpacing} #{@timestamp} #{@chainId} #{@lig_id}"
    fork do
      system ("python lib/tasks/DoGSiteScorer.py #{@id} #{@chain} #{@pocLev} #{@scoreType} #{@gridSpacing} #{@timestamp} #{@chainId}  #{@lig_id}")
    end

#das soll erstmal draussen bleiben. brauch ich glaub ich nicht
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
