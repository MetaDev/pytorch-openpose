## interpolate motion
#TODO interpolate every joint --> interpolation is not necessary, just encode the constraints
for j in range(18):
    joint_pos=[]
    for frame in sj_json:
        joint_pos.append((frame[j][0],frame[j][1]))
    joint_pos=np.array(joint_pos)
    ts=np.arange(len(joint_pos))
    csx = CubicSpline(ts,joint_pos)
    ts_interp=np.arange(0,len(joint_pos),0.1)
    joint_pos_interp=csx(ts)