from mccontroller import MCController

def stone_path_loop(mc: MCController):
    mc.command("time set day")
    mc.command("weather clear")
    mc.command("tp @p -185.5 68 77.5 -90.0 40.0")
    for _ in range(3):
        mc.forward(5)
        mc.turn("left")
        mc.forward()
        mc.jump_up(7)
        mc.turn("left")
        mc.forward(4)
        mc.turn("left")
        mc.jump_down(4)
        mc.turn("right")
        mc.jump_down(3)
        mc.turn("left")
        mc.forward(3)
        mc.turn("left")
        mc.forward(2)
        mc.right()

def block_ring(mc: MCController):
    mc.command("time set day")
    mc.command("weather clear")
    mc.command("tp @p -194.5 64 67.5 -180.0 40.0")
    mc.command("fill -196 64 68 -186 66 58 air")
    mc.forward(3)
    mc.turn("around")
    mc.command("clear")
    mc.command("give @p stone")

    for _ in range(3):
        mc.back()
        mc.center()
        for _ in range(3):
            mc.back()
            mc.click("right")
        mc.left()
        mc.forward(2)
        mc.turn("right")
    mc.back()
    mc.center()
    for _ in range(3):
        mc.back()
        mc.click("right")

    mc.forward()
    mc.jump_up()
    mc.forward()
    mc.left()

if __name__ == "__main__":
    mc = MCController()
    #stone_path_loop(mc)
    #block_ring(mc)
    print("Complete")
