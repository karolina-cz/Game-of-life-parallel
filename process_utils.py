def is_master(id):
  return id == 0

def is_last_process(id, size):
  return id == size - 1