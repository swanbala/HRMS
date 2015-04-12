
def level(value):
    if value==0:
        return "Administrator"
    elif value==1:
        return "general manager"
    elif value==2:
        return "manager"
    elif value==3:
        return "group leader"
    elif value==4:
        return "employee"
    else:
        return "employee under probation"