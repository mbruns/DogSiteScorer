class RequestsController < ApplicationController

  def show
    @request = Request.find(params[:id])
#    render :text => "<pre>#{File.read("/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}")}</pre>" 
     render :file =>"/home/meike/DoGSiteScorer/results/results_3DFR_1346059454_P0.html"
 
  end

end
