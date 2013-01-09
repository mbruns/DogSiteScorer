class RequestsController < ApplicationController

  def show
    @request = Request.find(params[:id])
    #@file = "/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}"
    @ready = true
    if @ready == true
      render :text => File.read("/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}")
    end
  end

end
