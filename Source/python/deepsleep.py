import machine

rtc = machine.RTC()


def set_awake_time_and_put_to_deepsleep(time_in_s):
    # configure RTC.ALARM0 to be able to wake the device
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, time_in_s * 1000)

    # put the device to sleep
    machine.deepsleep()
