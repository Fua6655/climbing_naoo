import almath


def main(motionProxy, X, Y, Theta):
    # Enable arms control by move algorithm
    motionProxy.setMoveArmsEnabled(True, True)

    # FOOT CONTACT PROTECTION
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    # get robot position before move
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))

    motionProxy.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

    # get robot position after move
    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))

    # compute and print the robot motion
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition

    # return an angle between [-PI, PI]
    robotMove.theta = almath.modulo2PI(robotMove.theta)



