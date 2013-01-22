class RequestsController < ApplicationController

  def show
    @request = Request.find(params[:id])
    render :text => "<pre>#{File.read("/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}")}</pre>"
 
  end

end
