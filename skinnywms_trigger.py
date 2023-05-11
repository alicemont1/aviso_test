from pyaviso import NotificationManager
 
 
# define function to be called
def do_something(notification):
    print(f"Notification for step {notification['request']['step']} received")
    # now do something useful with it ...
 
 
# define the trigger
trigger = {"type": "function", "function": do_something}
 
# create a event listener request that uses that trigger
# request = {
#     "class": "od",
#     "stream": "oper", "expver": 1, "domain": "g", "step": 1}
request = {
    "class": "od",
    "date": "20190810",
    "destination": "MAES",
    "domain": "g",
    "expver": "0001",
    "step": "1",
    "stream": "enfo",
    "target": "E1",
    "time": "00"
}
listeners = {
    "listeners": [
        {"event": "dissemination", "request": request, "triggers": [trigger]}
    
    ]}
 
# run it
aviso = NotificationManager()
aviso.listen(listeners=listeners)