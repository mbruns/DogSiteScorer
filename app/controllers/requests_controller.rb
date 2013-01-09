class RequestsController < ApplicationController

  def show
    @request = Request.find(params[:id])
    #@file = "/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}"
    @ready = false
    if @ready == true
      render :text => "<pre>#{File.read("/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}")}</pre>"
    end
 
  end

end
