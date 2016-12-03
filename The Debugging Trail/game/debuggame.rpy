init python:
    import json
    import time
    global level
    global buggyProg
    global current_thought
    global program
    current_thought = ""

    level = 1
    code_section = 0
    f = renpy.file("BuggyProgram.json")
    program = json.load(f)

    global errorMsgs
    f = renpy.file("ErrorMessages.json")
    errorMsgs = json.load(f)
    errorMsgs = errorMsgs["error_msg"]

    global stress
    global time_limit
    global the_time
    global time_penalty
    global lines_per_section
    global section_count
    global remaining
    global status
    global errorMsg
    global last_test_section_id 
    last_test_section_id = 1
    status = ""
    errorMsg = ""
    remaining = 0

    lines_per_section = 4
    section_count = 1
    time_penalty = 0
    time_limit = 0 ## in seconds
    stress = 0
    base_stress_modifier = 5
    stress_per_bug = 10
    break_modifier = 35 ## amount of stress removed by taking a break
    break_duration = 30 ## time penalty in seconds
    action_duration = 1 ## time that an action takes in seconds


    def load_level():
        global level
        global buggyProg
        global section_count
        global code_section
        global stress
        global time_limit
        global remaining
        global status
        global errorMsg
        global musicFlag
        musicFlag = 0
        errorMsg = ""
        status = "playing"
        buggyProg = program["program" + str(level)]
        section_count = 1
        code_section = 0
        stress = 0
        time_limit += (960 - remaining)


    def modify_stress():
        global stress
        stress = stress + base_stress_modifier
        if stress > 100:
            stress = 100
        check_wl_status
        sound_manager()
        if stress > 70:
            set_inner_thought("You are stressed! Take a break before you go crazy!")


    def sound_manager():
        global musicFlag
        if stress < 30:
            if musicFlag != 1:
                renpy.music.stop(fadeout=.6)
                renpy.music.play("Stress Level 1.wav", fadein=.3)
                musicFlag = 1

        if stress >= 30 and stress < 60:
            if musicFlag != 2:
                renpy.music.stop(fadeout=.6)
                renpy.music.play("Stress Level 2.wav", fadein=.3)
                musicFlag = 2

        if stress >= 60 and stress < 85:
            if musicFlag != 3:
                renpy.music.stop(fadeout=.6)
                renpy.music.play("Stress Level 3.wav", fadein=.3)
                musicFlag = 3

        if stress >= 85:
            if musicFlag != 4:
                renpy.music.stop(fadeout=.6)
                renpy.music.play("Stress Level 4.wav", fadein=.3)
                musicFlag = 4

    def countdown(st, at, length=0.0):
            global time_penalty
            global remaining
            remaining = length - st - time_penalty
            min = int(remaining/60)
            sec = int(remaining % 60)

            secstr = str(sec)
            if sec <= 9:
                secstr = "0" + secstr
            timestr = str(min) + ":" + secstr

            if remaining > 2.0:
                return Text(timestr, color="#fff", size=72), 1
            elif remaining > 0.0:
                return Text(timestr, color="#f00", size=72), 1
            else:
                check_wl_status()
                return anim.Blink(Text(timestr, color="#f00", size=72)), None

    def keep_coding():
        global section_count
        global last_test_section_id 
        section_count += 1
        thought = ""
        if section_count - last_test_section_id >= 2:
            thought += "Don't forget to test your code as you go! "
        if stress > 70:
            thought += ("You are stressed! Take a break before you go crazy! ")
        if thought != "":
            set_inner_thought(thought)
        
    def take_break():
        global stress
        global time_penalty
        global current_thought 
        stress = stress - break_modifier
        time_penalty += break_duration
        if stress < 0:
            stress = 0
        sound_manager()
        if stress < 70: 
            if "You are stressed! Take a break before you go crazy! " in current_thought: 
                set_inner_thought("")
        

    def action_time_penalty(extra_time=0):
        global time_penalty
        time_penalty += (action_duration + extra_time)

        global stress
        stress += 2

        sound_manager()
        check_wl_status()

    def replace_code():
        sound_manager()
        if stress > 70:
            set_inner_thought("You are stressed! Take a break before you go crazy! ")
        if "fixes" in  buggyProg[code_section]:

            x = 0
            while x != 2:
                x, fixid = ui.interact()

            oldCode = str(buggyProg[code_section]["code"])
            olderr = str(buggyProg[code_section]["err_msg"])

            if olderr is not None and olderr != "None":        ## casting to int fixes read error after
                olderr = int(olderr)                            ## a round of ressignment
            else: olderr = None

            temp = buggyProg[code_section]["fixes"][fixid]["err_msg"]
            if temp is not None and temp != "None":
                temp = int(temp)
            else: temp = None

            buggyProg[code_section]["code"] = buggyProg[code_section]["fixes"][fixid]["option"]
            buggyProg[code_section]["err_msg"] = temp

            buggyProg[code_section]["fixes"][fixid]["option"] = oldCode
            buggyProg[code_section]["fixes"][fixid]["err_msg"] = olderr

        else:
            modify_stress()
        ## after a code change it is possible that win conditions have been met

    def test_code():
        global errorMsg
        global last_test_section_id 
        last_test_section_id = section_count

        errorIndices = []
        for line in buggyProg[0: (section_count * lines_per_section)]:
            if "err_msg" in line:
                errorIndices.append(line["err_msg"])
        create_error_msg(errorIndices)

        check_wl_status()
        if stress > 70:
            set_inner_thought("You are stressed! Take a break before you go crazy! ")
        


    def create_error_msg(indices):
        global errorMsg
        global errorMsgs
        global stress
        global current_thought
        errorMsg = ""
        current_thought = ""

        for i in indices:
            if i != None:
                temp = errorMsgs[i]
                delayIndex = 0
                if "delayed" in temp:
                    delayIndex = ""
                    readFlag = False

                    for x in temp:
                        if x == "[":
                            readFlag = True
                            continue
                        if x == "]":
                            break
                        if readFlag:
                            delayIndex += x

                    temp = temp.replace("[" + delayIndex + "]" ,"")
                    if delayIndex == "":
                        delayIndex = len(buggyProg)
                    else:
                        delayIndex = int(delayIndex)

                if "delayed" not in temp:
                    if "thought" in temp:
                        set_inner_thought(temp)
                        continue
                    errorMsg += temp + "\n"
                    stress += stress_per_bug                ## stress is modified here because there is already a loop checking None vs error indices

                elif "delayed" in temp:
                    if delayIndex <= (section_count * lines_per_section):
                        temp = temp.replace("delayed", "")
                        if "thought" in temp:
                            set_inner_thought(temp)
                            continue
                        errorMsg += temp + "\n"

        if errorMsg == "":
            errorMsg = "No compile time errors"

    def set_inner_thought(string):
        global current_thought
        current_thought = string.replace("thought : ", "")

    def check_wl_status():
        sound_manager()
        global remaining
        global status

        status = "playing"
        if section_count*lines_per_section >= len(buggyProg):
            tag = True
            for line in buggyProg:
                if "err_msg" in line and line["err_msg"] != "None" and line["err_msg"] != None:
                    tag = False
            if tag:
                status = "win"
                renpy.jump("transition{}".format(level))


        if stress >= 100 or remaining <= 0:
            status = "lose"
            renpy.jump("lose")

    def show_code():
        tabStops = 0
        for i, section in enumerate(buggyProg[0: section_count * lines_per_section]):
            code = section["code"]

            temp = 0
            if code == "}":
                temp = 1
            num = str(i)
            if i <= 9: num = "  " + num
            code = (num + ".  " + "    "*(tabStops - temp)) + code
            ui.textbutton(code, style="code_line", text_style="my_font", action=[Function(action_time_penalty), Return([1,i])])
            tabStops += (code.count("{{"))
            tabStops -= (code.count("}"))


        for x in range(tabStops):
            pad = ""
            if i + x + 1 <= 9: pad = "  "
            line = pad + str(i + x + 1) + ". " + "    "*(tabStops - (x+1)) + "}"
            ui.textbutton(line, style="code_line", text_style="my_font", action=[Function(modify_stress), Function(action_time_penalty)])
