# 作者：黄杰琪
def log_request(req,res):
    with open('vswarch.log',"a")as log:
        print(req.form,req.remote_addr,req.User_agent,file=log)