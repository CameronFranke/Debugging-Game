## The script of the game goes in this file.

## Declare characters used by this game. The color argument colorizes the name
## of the character.

init -1 python:
    config.use_cpickle = False

    def hide_all():
        renpy.hide_screen("inner_thought")
        renpy.hide_screen("programmer_options")
        renpy.hide_screen("code")
        renpy.hide_screen("fix_menu")

    def show_all():
        renpy.show_screen("programmer_options")
        renpy.show_screen("inner_thought")

init:
    define e = Character('eileen')
    image bg office = "office.jpg"
    image bg pentagon = "Pentagon.jpg"

screen code:
    vbox:
        pos 375, 25
        frame:
            xmaximum 1500
            ymaximum 800

            viewport:
                draggable False
                mousewheel True
                scrollbars "vertical"
                side_xalign 1

                has vbox
                $show_code()

        frame:
            xsize 1500
            ysize 150

            xmaximum 1500
            ymaximum 150
            viewport:
                draggable False
                mousewheel True
                scrollbars "vertical"
                side_xalign 1
                vbox:
                    text "[errorMsg]" style "my_font"

screen programmer_options:
    vbox:
        pos (25, 25)
        spacing 30
        xsize 300

        image DynamicDisplayable(countdown,length=time_limit)

        vbox:
            spacing 10
            text " Stress Meter" bold True
            bar:
                #base_bar "#DF3238"
                range 100
                value stress
                xfill True

            textbutton "Take a break":
                style "game_button"
                text_style "game_button_text"
                action Function(take_break)

        vbox:
            spacing 10
            text " Options" bold True
            textbutton "Compile":
                style "game_button"
                text_style "game_button_text"
                action [Function(test_code), Function(action_time_penalty, extra_time=7)]
            textbutton "Code":
                style "game_button"
                text_style "game_button_text"
                action [Function(keep_coding), Function(action_time_penalty, extra_time=7)]

screen fix_menu:
     frame:
        xalign 0.0
        yalign 0.75
        vbox:
            $choices = buggyProg[code_section]
            if "fixes" in choices:
                $s = choices["fixes"]
                for i, ch in enumerate(s):
                    $code = ch["option"]
                    textbutton "[code]" style "code_line" text_style "my_font" action [Hide("fix_menu"), Function(action_time_penalty), Return([2,i])]

screen inner_thought:
    vbox:
        pos (40,550)
        xmaximum 350
        text "[current_thought]"

label fix_code:
    $x, code_section = ui.interact()
    show screen fix_menu
    $replace_code()


label view_code:
    hide fix_code
    show screen code
    jump fix_code

label fix_code:
    $x, code_section = ui.interact()
    show screen fix_menu
    $replace_code()


label view_code:
    hide fix_code
    show screen code
    jump fix_code

label start:
    call level1

label level1:
    $load_level()
    $ sound_manager()
    scene bg pentagon
    with dissolve
    e "Welcome to the Debugging Trail"
    e "The world is ending"
    e "It is your job to save the world by creating lifesaving programs"
    e "Like any programmer, you will run into bugs."
    e "It is essential that you fix them for human life to continue"

    scene bg office
    with dissolve
    e "To start coding press the 'Keep Coding' button"
    e "The code you will write will appear on the screen, but be careful because it may contain bugs"
    e "To compile your code press the 'Debug' button. You can do this as many times as you want."
    e "Errors will show in the debug console"
    e "To fix an error, you can click on line of code that you think needs to be fixed and a list of possible code fixes will pop up"
    e "Click the fix that you think is right and it will replace the incorrect code automatically"
    e "Beware: Every action you take will cost you time, and every bug the compiler catches will increase your stress"
    e "If your stress gets to high or you run out of time, you lose..."
    $show_all()
    jump view_code


label transition1:
    $hide_all()

    scene bg pentagon
    with dissolve

    e "Congratulations! you have made the world that much safer with your bug free program"

    e "However, there is still much to be done"

    python:
        global level
        level += 1

    call level2


label level2:
    $load_level()
    scene bg office
    with dissolve

    e "Welcome to level 2"

    e "Get to work!"

    $show_all()

    jump view_code

label transition2:
    $hide_all()

    scene bg pentagon
    with dissolve

    e "Congratulations! you have made the world that much safer with your bug free program"

    e "However, there is still much to be done"

    python:
        global level
        level += 1


    jump level3

label level3:
    $load_level()
    scene bg office
    with dissolve

    e "Welcome to level 3"

    e "Get to work!"

    $show_all()

    jump view_code

label transition3:
    $hide_screens()

    scene bg pentagon
    with dissolve

    e "Congratulations! You beat the game!"

    jump end

label lose:
    $hide_all()
    scene bg pentagon
    with dissolve

    e "Sorry, you lost"

    menu:
        "Play again":
            return

        "quit":
            jump end

    jump end

label end:
    $renpy.full_restart()
