import os
print(os.path.exists('cookies.json'))  # Should return True if in the same folder
print(os.path.exists('/home/opc/Soundboard/cookies.json'))  # Test absolute path