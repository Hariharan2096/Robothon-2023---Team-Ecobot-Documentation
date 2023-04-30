import numpy as np

## Function to convert Roll-Pitch-Yaw values of robot to Rotation Vector

def rpy2rv(roll,pitch,yaw):
  
  alpha = yaw
  beta = pitch
  gamma = roll
  
  ca = np.cos(alpha)
  cb = np.cos(beta)
  cg = np.cos(gamma)
  sa = np.sin(alpha)
  sb = np.sin(beta)
  sg = np.sin(gamma)
  
  r11 = ca*cb
  r12 = ca*sb*sg-sa*cg
  r13 = ca*sb*cg+sa*sg
  r21 = sa*cb
  r22 = sa*sb*sg+ca*cg
  r23 = sa*sb*cg-ca*sg
  r31 = -sb
  r32 = cb*sg
  r33 = cb*cg
  
  angle = np.arccos((r11+r22+r33-1)/2)
  sth = np.sin(angle)
  kx = (r32-r23)/(2*sth)
  ky = (r13-r31)/(2*sth)
  kz = (r21-r12)/(2*sth)
  
  rv = [0.0,0.0,0.0]
  rv[0] = angle*kx
  rv[1] = angle*ky
  rv[2] = angle*kz
  
  return rv