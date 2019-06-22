# Original 1
x = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(x)
# Rotate 90deg 2
print(np.flip(np.transpose(x),1))
# Rotate 90deg - Flip UD 3
print(np.flip(np.flip(np.transpose(x),1),0))
# Rotate 90deg - Flip LR 4 
print(np.transpose(x))
# Rotate 180deg 5
print(np.flip(np.flip(x,0),1))
# Rotate 180deg - Flip UD 6 
print(np.flip(x,1))
# Rotate 180deg - Flip LR 7
print(np.flip(x,0))
# Rotate 270deg 8 
print(np.flip(np.transpose(x),0))
# Rotate 270deg - FLip UD - Satisfied
print(np.transpose(x))
# Rotate 270deg - FLip LR - Satisfied
print(np.flip(np.flip(np.transpose(x),0),1))
# Flip Top Bottom - Satisfied
print(np.flip(x,0))
# Flip Left Right - Satisfied
print(np.flip(x,1))