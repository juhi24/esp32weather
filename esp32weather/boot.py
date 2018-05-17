def connect():
    import network
    from config import wlan_ssid, wlan_pass
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to ' + wlan_ssid)
        sta_if.active(True)
        sta_if.connect(wlan_ssid, wlan_pass)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


connect()