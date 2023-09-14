from microbit import *
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
import gc
from utime import ticks_ms
from sys import exit

initialize()
clear_oled()
avmmp_record = [[]for j in range(0, 2)]
avg_bpm = 0
index = 0
avg_pulse = 0
trigging = False
current_time = 0
ref_time = 0
beat_boolean = False
bpm = 0
first = True
avg_bpm_boolean = False
c_bp = 0
num_bpm = 0
distance_55 = []
min_55 = 0
receive = False
def main_function():
    global c_bp
    loop = 0
    max_bp = 0
    min_bp = 1023
    max_flag = True
    min_flag = True
    amp_bp = 0
    avmp_bp = []
    global avg_pulse
    num_pulse = 0
    val_bp = 0
    global trigging
    global avmmp_record
    global index
    start = False
    avmmp = 0
    clear_oled()
    while True:
        val_bp = int((pin1.read_analog()*0.258) - 24)
        signal = 0
        if val_bp>140 and start == False:
            start = True
        elif val_bp<50 and start == True:
            return None
        for i in range(10):
            signal = pin0.read_analog() + signal
            c_bp = signal/10
        if max_flag:
            if (c_bp > max_bp):
                max_bp = c_bp
            else:
                if (max_bp-c_bp) > 10:
                    fmax_bp = max_bp
                    max_flag = False
        if min_flag:
            if (c_bp < min_bp):
                min_bp = c_bp
            else:
                if (c_bp-min_bp) > 10:
                    fmin_bp = min_bp
                    min_flag = False
        if not(max_flag) and not(min_flag):
            amp_bp = max_bp - min_bp
            avmp_bp.append(amp_bp)
            if loop == 0:
                avmmp = mean(avmp_bp)
                avmp_bp.pop(0)
                # Delete unexpected noise and peak appearing during the curve
                if index>0 and 1.7*avmmp_record[0][index-1] < avmmp:
                    continue
                # Automatically the data to find the numerical solution
                elif start == True:
                    avmmp_record[0].append(avmmp)
                    avmmp_record[1].append(val_bp)
                    index += 1
                    print("avmmp = {} pressure = {}".format(avmmp, val_bp))
                    add_text(0, 2, str(avmmp))
            add_text(0, 1, "magP: "+str(avmmp)+"      ")
            max_bp = 0
            min_bp = 1023
            max_flag = True
            min_flag = True
        print((c_bp,))
        loop = loop + 1
        if ((loop % 10) == 0):
            add_text(0, 0, "BP: "+str(val_bp)+"      ")
            loop = 0
        # Feature#1 Automatic heartrate sensing coding
        # Finding the moving average
        if num_pulse <49 :
            num_pulse +=1
            avg_pulse += c_bp
        elif num_pulse == 49 :
            avg_pulse +=c_bp
            avg_pulse = avg_pulse/50
            num_pulse = 1000
            # After achieving the first average, activate the measuring bpm calculation
            trigging = True
        else :
            # print("changing the avg_pulse")
            # Calculating the moving average, which will be assigned to the threshold_on
            avg_pulse = ((49*avg_pulse)+c_bp)//50
        counting_beat()
        sleep(1)
    return None
def counting_beat():
    global current_time, ref_time, beat_boolean, bpm, first, avg_bpm_boolean, num_bpm
    global avg_bpm
    if trigging == True:
        # Achieve the threshold_on
        threshold_on = avg_pulse
        print("The threshold_on is ", threshold_on)
        # Detect the pulse
        if beat_boolean == False and c_bp>threshold_on:
            avg_bpm_boolean = True
            bpm = bpm + 1
            print("bpm = ", bpm)
            # print("Before, beat_boolean is ", beat_boolean)
            beat_boolean = True
            add_text(0,3,"PeeP")
            if first:
                # record the time stamp of the first beat
                ref_time = ticks_ms()
                first = False
            if bpm%5==0 :
                # record the time stamp of the fifth beat
                current_time = ticks_ms()
                first = True
                #print("We sensed it!!!, beat_boolean is ", beat_boolean)
        # Pulse move downn to be below threshold_on, which will be ready to be detected the next pulse
        if beat_boolean == True and c_bp < threshold_on:
            beat_boolean = False
            add_text(0 , 3, "    ")
            # For every five pulses, we aim to calculate the bpm
        if bpm%5 == 0 and avg_bpm_boolean == True:
            avg_bpm_boolean = False
            # Feature#2 Automic Errors and Exceptions Handling
            try :
                truebpm = (5*60000)//(current_time-ref_time)
                print("ref_time = ", ref_time, "current_time = ", current_time)
                print("True_bpm = ", truebpm)
            except ZeroDivisionError :
                return None
            # filter the faulty beat that may be detected
            if truebpm > 40 and truebpm<140:
                num_bpm+=1
                if num_bpm==1:
                    avg_bpm = truebpm
                else:
                    avg_bpm = (((num_bpm-1)*avg_bpm)+truebpm)//num_bpm
                print("avg_bpm = ",avg_bpm)

def cmp(tmp1,tmp0,arr,j):
    if arr[1][j] == tmp1:
        if arr[0][j]<tmp0:
            return True
        else : return False
    elif arr[1][j] < tmp1:
        return True
    else : return False

def sort(arr, index):
    for i in range(1,index):
        j = i-1
        tmp1 = arr[1][i]
        tmp0 = arr[0][i]
        while j>=0 and cmp(tmp1,tmp0, arr, j):
            arr[1][j+1] = arr[1][j]
            arr[0][j+1] = arr[0][j]
            j -= 1
        arr[1][j+1] = tmp1
        arr[0][j+1] = tmp0

def mean(datalist):
    sum = 0
    for i in datalist:
        sum += i
    if len(datalist) > 0:
        return sum/len(datalist)
    else:
        return None

def ui():
    global height, weight, sex, age
    # add_text(0,0,"Input gender")
    # add_text(0,1,"1 for men")
    # add_text(0,2,"0 for women")
    sex = int(input("Please specify your gender : "))
    # clear_oled()
    # add_text(0,0,"Enter height")
    height = float(input("Please enter your height : "))
    while height>2.5:
        clear_oled()
        # add_text(0,0,"Wrong Units")
        # add_text(0,1,str(height) + "m?")
        # add_text(0,2,"Reenter height")
        print("It seems that you enter your height in the wrong unit")
        height = float(input("Please reenter your height : "))
    # clear_oled()
    # add_text(0,0,"Enter weight(kg)")
    weight = float(input("Please enter your weight(kg) : "))
    # clear_oled()
    # add_text(0,0,"Enter age")
    age = int(input("Please enter your age: "))
    if sex == 1 :
        add_text(0,0,"Gender: M")
    else :
        add_text(0,0,"Gender: F")

    add_text(0,2, "Weight: "+str(weight))
    add_text(0,1,"Height:" + str(height))
    add_text(0,3,"Age:" + str(age))
    sleep(3000)
    return None

def cal_bmi(weight, height):
    return weight/(height*height)

add_text(0,0,"Press A")
add_text(0,1,"TO INPUT")
add_text(0,2,"Press B")
add_text(0,3,"To start")
ispress = False
while ispress == False:
    if button_a.is_pressed():
        ispress = True
        receive = True
        ui()
        sure = 0
        clear_oled()
        add_text(0,0,"Press 0 to")
        add_text(0,1,"Reprocess")
        add_text(0,2,"Press 1 to")
        add_text(0,3,"Continue")
        sure = int(input("Press 0 to reprocess, 1 to continue : "))
        while sure == 0:
            ui()
            add_text(0,0,"Press 0 to")
            add_text(0,1,"Reprocess")
            add_text(0,2,"Press 1 to")
            add_text(0,3,"Continue")
            sure = int(input("Press 0 to reprocess, 1 to continue : "))
    elif button_b.is_pressed():
        ispress = True

clear_oled()
add_text(0,0,"start")
gc.collect()
sleep(2000)
main_function()
clear_oled()
gc.collect()
clear_oled()
sleep(1000)
gc.collect()
sleep(1000)

sort(avmmp_record, index)
for i in range(0, index):
    print("{} {}".format(avmmp_record[0][i], avmmp_record[1][i]))

# Determine the mean pressure and where it is in the data
avmmp_max = max(avmmp_record[0])
avmmp_max_index = avmmp_record[0].index(avmmp_max)
# Discard the unexpected peak that may be the highest value
while avmmp_max_index < 5 or index-avmmp_max_index < 5:
    print("Adjusting the MBP")
    # Feature#2 : Automatic errors and exceptions handling
    try:
        avmmp_record[0].pop(avmmp_max_index)
        avmmp_record[1].pop(avmmp_max_index)
        avmmp_max = max(avmmp_record[0])
        avmmp_max_index = avmmp_record[0].index(avmmp_max)
        index -= 1
    except IndexError:
        clear_oled()
        add_text(0,0, "Stay relax")
        add_text(0,1, "and remeasure")
        add_text(0,2, "the pressure")
        exit()
    except ValueError:
        clear_oled()
        add_text(0,0, "Stay relax")
        add_text(0,1, "and remeasure")
        add_text(0,2, "the pressure")
        exit()
print("Max is {} at index {} = {}".format(avmmp_max, avmmp_max_index, avmmp_record[1][avmmp_max_index]))
# Create the array to record the distance between mean_pressure and each pressure
for i in range(0, index):
    distance_55.append(round(abs(avmmp_record[0][i] - (0.5*avmmp_max)), 2))
# Find the value having the minimum distance and where it is
min_55 = min(distance_55[0:avmmp_max_index-1])
min_55 = distance_55.index(min_55)
# Determine the systolic pressure
sys_pressure = avmmp_record[1][min_55]
# Use the formula from the medical science to determine the dias_pressure
dias_pressure = (3*avmmp_record[1][avmmp_max_index]-sys_pressure)//2
# Feature#0 automatic pressure sensing
add_text(0, 0, "SYS: "+str(sys_pressure)+"      ")
add_text(0, 1, "DIA: "+str(dias_pressure)+"      ")
# Feature#1 Heart rate display
add_text(0, 2, "BPM = " + str(avg_bpm))

# Features#3 Range test!!!
pulse_pressure = sys_pressure - dias_pressure
if receive == True:
    bmi = cal_bmi(weight,height)
    if avg_bpm>100:
        add_text(0,3,"Alert!!")
        display.scroll("Alert!! Your heart rate is very high")
        display.scroll("You may need to rest")

    if age>=55 and pulse_pressure>60:
        add_text(0,3,"Alert!!")
        display.scroll("Alert!! Too high pulse preasure")
        sleep(2000)
    elif pulse_pressure>55:
        add_text(0,3,"Alert!!")
        display.scroll("Alert!! Too high pulse preasure")
        sleep(2000)
    if sex == 1:
        if age>=55:
            if bmi>=25 and sys_pressure>165 or dias_pressure>100:
                display.scroll("Alert!!! Too high pressure")
                add_text(0,3,"Alert!!")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
            elif sys_pressure>160 or dias_pressure>95:
                add_text(0,3,"Alert!!")
                display.scroll("Alert!!! Too high pressure")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
        else :
            if bmi>=25 and sys_pressure>145 or dias_pressure>90:
                display.scroll("Alert!!! Too high pressure")
                add_text(0,3,"Alert!!")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
            elif sys_pressure>140 or dias_pressure>90:
                add_text(0,3,"Alert!!")
                display.scroll("Alert!!! Too high pressure")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
    else :
        if age>=55:
            if bmi>=25 and sys_pressure>155 or dias_pressure>100:
                display.scroll("Alert!!! Too high pressure")
                add_text(0,3,"Alert!!")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
            elif sys_pressure>150 or dias_pressure>95:
                add_text(0,3,"Alert!!")
                display.scroll("Alert!!! Too high pressure")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
        else :
            if bmi>=25 and sys_pressure>140 or dias_pressure>90:
                display.scroll("Alert!!! Too high pressure")
                add_text(0,3,"Alert!!")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
            elif sys_pressure>135 or dias_pressure>85:
                add_text(0,3,"Alert!!")
                display.scroll("Alert!!! Too high pressure")
                sleep(2000)
                display.scroll("Have a rest around 10 minutes")
                sleep(2000)
else:
    if sys_pressure>140 or dias_pressure>90:
        add_text(0,3,"Alert!!")
        display.scroll("Alert!!! Too high pressure")
        sleep(2000)
        display.scroll("Have a rest around 10 minutes")
        sleep(2000)
        add_text(0,3,"Alert!!")
    if avg_bpm>100:
        add_text(0,3,"Alert!!")
        display.scroll("Alert!! Your heart rate is very high")
        display.scroll("You may need to rest")
    if pulse_pressure>5+5:
        add_text(0,3,"Alert!!")
        display.scroll("Alert!! Too high pulse preasure")
        sleep(2000)

