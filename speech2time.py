####################################################################################################
# function for convert time in natural language string in code of time
# by Pavel Melikhov 2021 v.1.1
# python 3.10.0
#
# !/usr/bin/python3
# -*- coding: UTF-8 -*-
####################################################################################################

import text2num, re


def timeToSlot(hour, minute, out_type):  # Перевод времени в дамаск
    if int(minute) % 15 != 0:  # Округление до заданых значений минут, если оно отличается от [0, 15, 30, 45, 60]
        # min_set = [0, 15, 30, 45, 60]
        min_set = [0, 30, 60]
        # min_set = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        minute = min(min_set, key=lambda x: abs(x - int(minute)))
        if int(minute) == 60:
            hour = int(hour) + 1
            minute = 0
    if out_type == 'damask':
        damasktime = str(int(hour) * 60 + int(minute))
    if out_type == 'time':
        damasktime = f'{int(hour):02d}:{int(minute):02d}'
    return damasktime


def speechToTime(speech, out_type):  # Перевод человеческой речи в цифры, поиск ключевых слов по маскам
    speech = speech.lower()
    nums = text2num.convert(speech, True, ' ').split(' ')
    # if nums[0] == '':
    #     nums.pop(0)
    if len(nums) > 2 and nums[2] == '0':
        nums.pop(2)
    if len(nums) > 2 and nums[1] and int(nums[2]) < 10:
        nums.pop(1)
    if len(nums) >= 2 and nums[0] == '0' and int(nums[1]) > 10:
        nums.pop(0)

    try:
        if re.search(' час |час$|час |на час| час ровно | час дня ', speech, re.IGNORECASE) and nums[0] != '21' and nums[0] == '':
            nums.insert(0, 13)
            try:
                nums.remove('')
            except:
                pass
            if re.search('без ', speech, re.IGNORECASE):
                nums.reverse()
                # print(nums)
        if re.search('(половин(а|у)|пол |половинк(а|у))', speech):  # Половина
            nums.append('30')
            nums[0] = int(nums[0]) - 1
        elif re.search('без ', speech):  # Без (пример: без пятнадцати три)
            nums.reverse()
            nums[0] = int(nums[0]) - 1
            if re.search('четверт', speech):
                nums.append(45)
            else:
                nums[1] = 60 - int(nums[1])
        elif re.search('минут.*(первого|второго|третьего|четвертого|пятого|шестого|седьмого|восьмого|девятого|десятого|одиннадцатого|двенадцатого)', speech):  # Двадцать минут второго
            nums.reverse()
            nums[0] = int(nums[0]) - 1
        elif re.search('четверт', speech):  # Четверть (Пример: четверть четвертого)
            nums.append('15')
            nums[0] = int(nums[0]) - 1
        else:  # Все остальное
            nums[0] = int(nums[0])
        if len(nums) > 2:
            return 0
        if re.search(('утр|до обед|в первой половине'), speech, re.IGNORECASE):
            hour = int(nums[0])
        elif re.search(('после обед|дня|днем|день|второй половин|вечер|после полудн'), speech, re.IGNORECASE):
            if int(nums[0]) != 13:
                hour = (int(nums[0]) + 12)
            else:
                hour = int(nums[0])
        elif int(nums[0]) <= 7:
            hour = (int(nums[0]) + 12)
        else:
            hour = int(nums[0])
        if len(nums) == 1:
            minute = 0
        else:
            minute = nums[1]
        if int(hour) > 24 or int(minute) > 60 or int(hour) < 0 or int(minute) < 0:
            return 0
        return timeToSlot(hour, minute, out_type)
    except ValueError:
        return 0
    except IndexError:
        return 0


def getNormTime(timeinput, out_type):
    if ':' in timeinput:  # Перевод цифрового времени (8:15)
        time_match = re.search('(..:..)|(.:..)', timeinput)
        time = time_match[0].split(':')
        return timeToSlot(time[0], time[1], out_type)
    else:
        return speechToTime(timeinput, out_type)


if __name__ == '__main__':
    # timelist = open('times-06-win.txt', 'r')
    # out_file = open('res_test_damsk.txt', 'w+')

    # for line in timelist:
    #     fields = line.split('\t')
    #     res = getNormTime(fields[1][:-1],'time')
    #     if res != fields[0]:
    #         out_file.write('\"' + fields[1][:-1] + '\",' + fields[0] + "," + res + "\n")

    # timelist.close()
    # out_file.close()
    print(getNormTime('на одиннадцать часов ', 'time'))