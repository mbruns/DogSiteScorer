require 'net/http'
module ApplicationHelper

def getHeader(pagetitle, servername)
    
  Net::HTTP.get(URI("http://www.zbh.uni-hamburg.de/template")) =~ /(.*?) <!--###CONTENT###-->/m
  header = $1.html_safe
  header["<!--###TITLE###-->"] = pagetitle
  header["<!--###NAME###-->"] = servername
  
  return header
end

def getFooter()
    
  Net::HTTP.get(URI("http://www.zbh.uni-hamburg.de/template")) =~ /<!--###CONTENT###-->(.*?) /m
  footer = $1.html_safe
  footer.gsub!(/<!--###FOOTER###-->/, "")
  
  return footer
end

end
