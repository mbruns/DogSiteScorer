module SessionsHelper
def current_session
  session[:session_id] ||= Session.create.id
  Session.find session[:session_id]
end

end
