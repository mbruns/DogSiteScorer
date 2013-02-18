class RequestsController < ApplicationController

  def show
    @request = Request.find(params[:id])
    File.read("/home/meike/DoGSiteScorer/results/results_1346845200.html")=~ /.*?(<td id="content">.*?)<div id="footer">/m
    @text = $1.html_safe
#    render :text => "<pre>#{@text}</pre>", :layout => 'application.html.erb'
#    render :text => "<pre>#{File.read("/home/meike/DoGSiteScorer/tmp/cache/#{@request.pdb}")}</pre>" 
     render :file =>"/home/meike/DoGSiteScorer/results/results_1346845200.html"
 
  end
  
#  def P0
#  render :file =>"/home/meike/DoGSiteScorer/results/results_3DFR_1346059454_P0.html"
#  end

end
