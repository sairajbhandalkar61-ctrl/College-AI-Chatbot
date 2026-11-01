with open('backend/models.py', 'rb') as f:
    data = f.read()

target = b"'is_completed': self.is_completed\r\n        }"
replacement = b"'is_completed': self.is_completed,\r\n            'status': 'Completed' if self.is_completed else 'Pending'\r\n        }"

if target not in data:
    target = b"'is_completed': self.is_completed\n        }"
    replacement = b"'is_completed': self.is_completed,\n            'status': 'Completed' if self.is_completed else 'Pending'\n        }"

assert target in data, "target not found!"
data = data.replace(target, replacement, 1)

with open('backend/models.py', 'wb') as f:
    f.write(data)

print("Successfully patched backend/models.py!")
